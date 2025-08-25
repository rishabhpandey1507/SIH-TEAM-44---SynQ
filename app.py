import os
from flask import Flask
from config import Config
from database import db
from blueprints.user_routes import user_bp
from blueprints.admin_routes import admin_bp

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # Load configuration from the Config class
    app.config.from_object(Config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database with the app
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp) # Removed url_prefix='/' for the main blueprint
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Define a custom CLI command to initialize the database
    @app.cli.command("init-db")
    def init_db_command():
        """Clear existing data and create new tables."""
        db.create_all()
        print("Initialized the database.")

    return app

# This entry point is still useful for some deployment methods
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)