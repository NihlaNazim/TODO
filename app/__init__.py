import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
from sqlalchemy.exc import OperationalError

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use DATABASE_URL env var; fallback to localhost for local dev if needed
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/TODO-Docker')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    print("Importing routes.main...")
    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        last_exception = None
        for i in range(10):
            try:
                db.create_all()
                print("✅ Database tables created successfully")
                break
            except OperationalError as e:
                last_exception = e
                print(f"❌ DB not ready yet (attempt {i + 1}/10), retrying in 2 seconds...")
                time.sleep(2)
        else:
            print("❌ Failed to connect to DB after multiple attempts.")
            raise last_exception

    return app
