from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import ParkingLot, ParkingSpot, User
from app import db

admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/parking-lot', methods=['POST'])
@jwt_required()
def create_parking_lot():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    try: 
        lot = ParkingLot(
                prime_location_name=data['prime_location_name'],
                price=data['price'],
                address=data['address'],
                pincode=data['pincode'],
                number_of_spots=data['number_of_spots']
                )
        db.session.add(lot)
        db.session.commit()

        for _ in range(data['number_of_spots']):
            spot = ParkingSpot(lot_id=lot.id, status='A')
            db.session.add(spot)
        db.session.commit()

        return jsonify({'message': 'Parking lot created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating parking lot', 'error': str(e)}), 500
