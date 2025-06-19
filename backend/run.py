from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
                username="admin",
                password=generate_password_hash("admin123"),
                role="admin"
                )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created username='admin', password='admin123'")
    else:
        print("Admin user already exists.")

if __name__ == "__main__":
    app.run(debug=True)
