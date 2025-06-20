from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models import ParkingLot, ParkingSpot, Reservation, User 
from app import db

parking_bp = Blueprint('parking', __name__, url_prefix='/parking')

@parking_bp.route('/reserve', methods=['POST'])
@jwt_required()
def reserve_spot():
    user_id = get_jwt_identity()
    data = request.get_json()
    lot_id = data.get('lot_id')

    if not lot_id:
        return jsonify({'message': 'lot_id is required'}), 400
    
    user = User.query.get(user_id)

    active_res = Reservation.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
    if active_res:
        return jsonify({'message': 'You already have an active reservation'}), 400

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({'message': 'No available spots in this lot'}), 404

    try:
        reservation = Reservation(
                user_id=user_id,
                lot_id=lot_id,
                spot_id=spot.id,
                parking_timestamp=datetime.now()
                )
        spot.status = 'O'

        db.session.add(reservation)
        db.session.commit()

        return jsonify({
            'message': 'Reservation successful',
            'reservation_id': reservation.id,
            'spot_id': spot.id,
            'lot_id': lot_id,
            'parking_time': reservation.parking_timestamp.isoformat()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Reservation failed', 'error': str(e)}), 500
