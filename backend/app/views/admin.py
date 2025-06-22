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

@admin_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
def get_parking_lots():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    try:
        lots = ParkingLot.query.all()
        output = []
        for lot in lots:
            output.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pincode': lot.pincode,
                'number_of_spots': lot.number_of_spots
                })
        return jsonify({'parking_lots': output}), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching parking lots', 'error': str(e)}), 500

@admin_bp.route('/parking-lot/<int:lot_id>/spots', methods=['GET'])
@jwt_required()
def get_parking_spots(lot_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403

    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    data = [{'id': spot.id, 'status': spot.status} for spot in spots]
    return jsonify({'parking_spots': data}), 200

@admin_bp.route('/parking-lot/<int:lot_id>', methods=['PUT'])
@jwt_required()
def update_parking_lot(lot_id):
    user = User.query.get(get_jwt_identity())
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403

    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    try:
        lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
        lot.price = data.get('price', lot.price)
        lot.address = data.get('address', lot.address)
        lot.pincode = data.get('pincode', lot.pincode)

        db.session.commit()
        return jsonify({'message': 'Parking lot updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating lot', 'error': str(e)}), 500

@admin_bp.route('/parking-lot/<int:lot_id>', methods=['DELETE'])
@jwt_required()
def delete_parking_lot(lot_id):
    user = User.query.get(get_jwt_identity())
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403

    lot = ParkingLot.query.get_or_404(lot_id)

    if any(spot.status == 'O' for spot in lot.spots):
        return jsonify({"message": "Cannot delete lot. One or more spots are still occupied."}), 400

    try:
        db.session.delete(lot)
        db.session.commit()
        return jsonify({'message': "Parking lot deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting lot', 'error': str(e)}), 500

@admin_bp.route('/users', methods = ['GET'])
@jwt_required()
def view_user():
    user = User.query.get(get_jwt_identity())
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    users = User.query.filter_by(role='user').all()
    data = [{'id': u.id, 'username': u.username } for u in users]
    return jsonify({'users': data}), 200
