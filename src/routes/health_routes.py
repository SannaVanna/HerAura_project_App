from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from src.models import HealthTracker
from src.db import db

health_bp = Blueprint('health_bp', __name__)

#-----------------------------------------------
# Rule-based Menstrual Tracker Function
#-----------------------------------------------
def menstrual_tracker(age, cycle_start_date_str, flow_days, mood):
    """Predicts next period date and gives health feedback based on flow length and mood."""

    # Safely parse cycle_start_date
    if cycle_start_date_str:
        cycle_start_date = datetime.strptime(cycle_start_date_str, "%Y-%m-%d").date()
    else:
        cycle_start_date = date.today()

    cycle_length = 28
    next_period = cycle_start_date + timedelta(days=cycle_length)

    # Normalize mood input
    mood = mood.lower() if mood else ""

    # Convert flow_days to int safely
    try:
        flow_days = int(flow_days)
    except (TypeError, ValueError):
        flow_days = 0

    # Flow analysis and feedback
    if flow_days > 5:
        message = "Your period lasted longer than usual."
        if mood == "sick":
            message += " You feel unwell. Please see a doctor."
        else:
            message += " Monitor for next month."
    elif flow_days < 4:
        message = "Your period seems shorter than normal."
        if mood == "sick":
            message += " You feel unwell. Please see a doctor."
        else:
            message += " Track next month for consistency."
    elif 4 <= flow_days <= 5:
        if mood in ['normal', 'happy']:
            message = "Everything looks normal and healthy."
        elif mood in ["tired", "cramps"]:
            message = "You may be experiencing typical menstrual symptoms. Ensure proper rest and hydration."
        elif mood in ["angry", "depressed"]:
            message = "You might be experiencing hormonal imbalance. Monitor your cycle or consult a doctor if it persists."
        else:
            message = "Cycle looks normal. Keep tracking for consistency."
    else:
        message = "Unable to determine cycle status. Please provide valid flow days and mood."

    return {
        "Predicted Next Period": next_period,
        "Health Feedback": message
    }

#-----------------------------------------------
# Health Tracker Route
#-----------------------------------------------
@health_bp.route('/health', methods=['GET', 'POST'])
@login_required
def health_tracker():
    if request.method == 'POST':
        # Safely parse age and flow_days to avoid TypeError when fields are missing
        age_raw = request.form.get('age')
        try:
            age = int(age_raw) if age_raw and str(age_raw).strip() else 0
        except (TypeError, ValueError):
            age = 0

        cycle_start_date_str = request.form.get('cycle_start_date')

        flow_days_raw = request.form.get('flow_days')
        try:
            flow_days_int = int(flow_days_raw) if flow_days_raw and str(flow_days_raw).strip() else 0
        except (TypeError, ValueError):
            flow_days_int = 0

        mood = request.form.get('mood')
        notes = request.form.get('notes')

        # Run tracker logic (pass the integer flow_days)
        result = menstrual_tracker(age, cycle_start_date_str, flow_days_int, mood)

        # Ensure result contains the expected keys
        predicted = result.get("Predicted Next Period")
        feedback = result.get("Health Feedback")

        # Create HealthTracker record
        new_entry = HealthTracker(
            age=age,
            cycle_start_date=(predicted - timedelta(days=28)) if isinstance(predicted, (datetime, date)) else None,
            cycle_length=28,
            flow_days=flow_days_int,
            mood=mood,
            notes=notes,
            next_period_date=predicted,
            health_message=feedback,
            created_at=datetime.utcnow(),
            user_id=current_user.id
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('health_bp.health_tracker'))

    return render_template('health_tracker.html')
