from flask import Blueprint, render_template, flash
from app.services.event_service import fetch_events

event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/events', methods=['GET'])
def events_page():
    events = fetch_events()

    if events is None:
        flash('Unable to fetch events at this time.', 'danger')
        events = []

    return render_template('user_dashboard.html', events=events, title='Events')
