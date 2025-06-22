import csv
import os
from datetime import datetime
from flask import current_app
from app import db
from app.models import Reservation, ParkingLot, User

# This will be assigned in register_tasks()
export_user_csv = None

def register_tasks(celery):
    @celery.task(name="export_user_csv")
    def _export_user_csv(user_id):
        with current_app.app_context():
            user = User.query.get(user_id)
            reservations = Reservation.query.filter_by(user_id=user_id).all()

            if not reservations:
                return "No reservations found"

            filename = f"user_{user_id}_reservations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)

            with open(filepath, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Reservation ID", "Lot", "Spot", "Start Time", "End Time", "Cost"])

                for res in reservations:
                    lot = ParkingLot.query.get(res.lot_id)
                    writer.writerow([
                        res.id,
                        lot.prime_location_name if lot else "Unknown",
                        res.spot_id,
                        res.parking_timestamp,
                        res.leaving_timestamp or "Still Parked",
                        res.parking_cost or 0
                    ])

            return f"CSV exported to {filepath}"

    global export_user_csv
    export_user_csv = _export_user_csv

