from flask import render_template
from app import app
from models import User
from datetime import datetime, timedelta


@app.route('/online-users')
def online_users():
    # Users are considered online if they were active the 5mins 
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    users = User.query.all()
    online_users = User.query.filter(User.last_seen >= five_minutes_ago).all() #currently online

    return render_template('community.html', users=users, online_users=online_users, current_user=current_user)