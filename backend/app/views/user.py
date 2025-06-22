from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import ParkingLot, ParkingSpot, Reservation, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/lots', methods=['GET'])
@jwt_required()
def view_parking_lots():
    lots = ParkingLot.query.all()
    output = []
    for lot in lots:
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        output.append({
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'price': lot.price,
            'address': lot.address,
            'pincode': lot.pincode,
            'available_spots': available
        })
    return jsonify({'parking_lots': output}), 200

@user_bp.route('/my-reservation', methods=['GET'])
@jwt_required()
def my_reservation():
    user_id = get_jwt_identity()
    reservation = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).first()

    if not reservation:
        return jsonify({'message': 'No active reservation found'}), 404

    lot = ParkingLot.query.get(reservation.lot_id)
    return jsonify({
        'reservation_id': reservation.id,
        'spot_id': reservation.spot_id,
        'lot': lot.prime_location_name,
        'start_time': reservation.parking_timestamp.isoformat()
        }), 200

