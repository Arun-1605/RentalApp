from flask import Flask
from dotenv import load_dotenv
import os
from routes import auth_routes, index_routes
from admin import admin_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(index_routes)
app.register_blueprint(admin_routes)

if __name__ == '__main__':
    app.run(debug=True)
