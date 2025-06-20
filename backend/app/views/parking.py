from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
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


@parking_bp.route('/leave', methods=['POST'])
@jwt_required()
def leave_parking():
    current_user_id = get_jwt_identity()

    reservation = Reservation.query.filter_by(user_id=current_user_id, leaving_timestamp=None).first()
    if not reservation:
        return jsonify({'message': 'No active reservation found'}), 400

    reservation.leaving_timestamp = datetime.now()

    parked_seconds = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds()
    parked_hours = parked_seconds / 3600

    lot = ParkingLot.query.get(reservation.lot_id)
    rate = lot.price if lot else 0
    reservation.parking_cost = round(parked_hours * rate, 2)
    
    spot = ParkingSpot.query.get(reservation.spot_id)
    if spot:
        spot.status = 'A'

    db.session.commit()
    return jsonify({
        'message': 'Spot released successfully',
        'duration_hours': round(parked_hours, 2),
        'total_cost': reservation.parking_cost
        })
