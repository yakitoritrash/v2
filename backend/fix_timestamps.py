# fix_timestamps.py

from app import create_app, db
from app.models import Reservation

app = create_app()

with app.app_context():
    updated_parking = 0
    updated_leaving = 0
    reservations = Reservation.query.all()
    for res in reservations:
        if res.parking_timestamp and res.parking_timestamp.tzinfo is not None:
            res.parking_timestamp = res.parking_timestamp.replace(tzinfo=None)
            updated_parking += 1
        if res.leaving_timestamp and res.leaving_timestamp.tzinfo is not None:
            res.leaving_timestamp = res.leaving_timestamp.replace(tzinfo=None)
            updated_leaving += 1
    db.session.commit()
    print(f"✔️ Stripped timezone from {updated_parking} parking_timestamp values.")
    print(f"✔️ Stripped timezone from {updated_leaving} leaving_timestamp values.")

