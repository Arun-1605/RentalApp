from flask import Flask
from config import Config
from routes import auth_routes, index_routes

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(index_routes)

if __name__ == '__main__':
    app.run(debug=True)
