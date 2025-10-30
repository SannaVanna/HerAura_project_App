from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import timedelta, date
from src.models import HealthTracker
from src.db import db

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET', 'POST'])
@login_required
def health_tracker():
    if request.method == 'POST':
        cycle_start_date = request.form.get('cycle_start_date')
        cycle_length = int(request.form.get('cycle_length'))
        symptoms = request.form.get('symptoms')
        notes = request.form.get('notes')
        # Ensure we always have a valid start date because the DB column is NOT NULL.
        # If the form didn't include a date, default to today.
        from datetime import datetime
        if cycle_start_date:
            start_dt = datetime.strptime(cycle_start_date, "%Y-%m-%d").date()
        else:
            start_dt = date.today()

        next_date = start_dt + timedelta(days=cycle_length)
        log = HealthTracker(
            cycle_start_date=start_dt,
            cycle_length=cycle_length,
            symptoms=symptoms,
            notes=notes,
            next_period_date=next_date,
            user_id=current_user.id
        )
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('health_bp.health_tracker'))

    records = HealthTracker.query.filter_by(user_id=current_user.id).order_by(HealthTracker.id.desc()).all()
    return render_template('health_tracker.html', records=records)