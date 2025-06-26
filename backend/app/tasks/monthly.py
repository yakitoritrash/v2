import os
from flask import render_template_string
from flask_mail import Message
from datetime import datetime, timedelta
from dotenv import load_dotenv

from app.models import User, Reservation, ParkingLot

load_dotenv()

def register_tasks(celery, db, mail):
    @celery.task(name="app.tasks.monthly.send_monthly_report")
    def send_monthly_report(user_id):
        user = User.query.get(user_id)
        if not user:
            return f"User with ID {user_id} not found"

        one_month_ago = datetime.now() - timedelta(days=30)
        reservations = Reservation.query.filter(
            Reservation.user_id == user_id,
            Reservation.parking_timestamp >= one_month_ago,
            Reservation.leaving_timestamp != None
        ).order_by(Reservation.parking_timestamp.desc()).all()

        if not reservations:
            return f"No reservations to report for user {user.username}"

        total_cost = sum(r.parking_cost for r in reservations if r.parking_cost)
        most_used_lot_id = max(
            set(r.lot_id for r in reservations),
            key=lambda lid: sum(1 for r in reservations if r.lot_id == lid),
            default=None
        )
        most_used_lot = ParkingLot.query.get(most_used_lot_id).prime_location_name if most_used_lot_id else "N/A"

        html_report = render_template_string("""
        <h2>Monthly Parking Report - {{ user.username }}</h2>
        <p>Month: {{ month }}</p>
        <p>Total Reservations: {{ total_reservations }}</p>
        <p>Total Cost: ₹{{ total_cost }}</p>
        <p>Most Used Lot: {{ most_used_lot }}</p>
        <hr>
        <table border="1" cellpadding="6">
            <thead>
                <tr>
                    <th>Lot</th>
                    <th>Start</th>
                    <th>End</th>
                    <th>Cost</th>
                </tr>
            </thead>
            <tbody>
                {% for r in reservations %}
                <tr>
                    <td>{{ r.lot_name }}</td>
                    <td>{{ r.start }}</td>
                    <td>{{ r.end }}</td>
                    <td>₹{{ r.cost }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        """, user=user,
           month=datetime.now().strftime("%B %Y"),
           total_reservations=len(reservations),
           total_cost=round(total_cost, 2),
           most_used_lot=most_used_lot,
           reservations=[{
               "lot_name": ParkingLot.query.get(r.lot_id).prime_location_name if ParkingLot.query.get(r.lot_id) else "N/A",
               "start": r.parking_timestamp.strftime("%Y-%m-%d %H:%M"),
               "end": r.leaving_timestamp.strftime("%Y-%m-%d %H:%M"),
               "cost": round(r.parking_cost or 0, 2)
           } for r in reservations]
        )

        msg = Message(
            subject="Your Monthly Parking Report",
            sender=os.getenv("SMTP_USERNAME"),
            recipients=[user.email],
            html=html_report
        )

        mail.send(msg)
        return f"Monthly report sent to {user.email}"

