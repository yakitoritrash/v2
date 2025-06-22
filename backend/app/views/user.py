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
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A')
        output.append({
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'price': lot.price,
            'address': lot.address,
            'pincode': lot.pincode,
            'available_spots': available
            })
    return jsonify({'parking_lots': output}), 200

