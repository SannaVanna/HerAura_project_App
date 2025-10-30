from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from openai import OpenAI
from src.models import AIChat
from src.db import db
import random
import os
from dotenv import load_dotenv

ai_bp = Blueprint('ai_bp', __name__)

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@ai_bp.route('/ai', methods=['GET', 'POST'])
@login_required
def ai_chat():
    return render_template('ai_chat.html')

@ai_bp.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message', '').lower()

    # Define “sensitive” or deep topics
    mentor_keywords = ["career", "relationship", "mental", "stress", "health", "personal", "family"]

    # Example mentors (you can later fetch from DB)
    mentors = [
        {"name": "Ada Johnson", "specialty": "Career Development", "link": "https://linkedin.com/in/adajohnson"},
        {"name": "Lara Yusuf", "specialty": "Mental Health & Self-care", "link": "https://linkedin.com/in/larayusuf"},
        {"name": "Chiamaka Obi", "specialty": "Personal Growth & Mindset", "link": "https://linkedin.com/in/chiamakaobi"}
    ]

    # If the message contains sensitive keywords
    if any(word in user_message for word in mentor_keywords):
        suggested = random.sample(mentors, 2)
        response = (
            "That’s a really thoughtful question 💭.\n\n"
            "I can only give simple guidance on this, but it's best to talk to a mentor for deeper clarity.\n\n"
            f"You could reach out to:\n"
            f"🌸 {suggested[0]['name']} — {suggested[0]['specialty']}\n"
            f"🔗 {suggested[0]['link']}\n\n"
            f"🌼 {suggested[1]['name']} — {suggested[1]['specialty']}\n"
            f"🔗 {suggested[1]['link']}\n\n"
            "Would you like me to connect you directly in the app?"
        )
        return jsonify({'response': response})

    # Otherwise use OpenAI to generate a general response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Aura, a friendly and supportive AI for girls learning, growth, and wellness. Respond kindly and simply."},
            {"role": "user", "content": user_message}
        ]
    )

    ai_reply = completion.choices[0].message.content
    return jsonify({'response': ai_reply})