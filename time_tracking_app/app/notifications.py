from flask import flash
from datetime import datetime, timedelta
from app.models import User, WorkSession

def send_idle_alert(user):
    # Implement logic to send an idle alert to the user
    flash(f'{user.username}, you have been idle for too long!')

def send_deadline_alert(user, deadline):
    # Implement logic to send a deadline alert to the user
    flash(f'{user.username}, you have a deadline approaching at {deadline}!')

def check_idle_users():
    users = User.query.all()
    for user in users:
        last_session = WorkSession.query.filter_by(user_id=user.id).order_by(WorkSession.start_time.desc()).first()
        if last_session and not last_session.end_time and (datetime.utcnow() - last_session.start_time > timedelta(minutes=30)):
            send_idle_alert(user)

def check_approaching_deadlines():
    users = User.query.all()
    for user in users:
        # Check if user has approaching deadlines
        # Implement deadline checking logic
        pass
