from flask import Blueprint, render_template, request, redirect, flash, session, url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

auth_routes = Blueprint('auth_routes', __name__)
index_routes = Blueprint('index_routes', __name__)

# Function to connect to the database
def get_db_connection():
    connection = pymysql.connect(
        charset="utf8mb4",
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection




# Index route
@index_routes.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM bikes')
    tours = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', tours=tours)

# Signup route
@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Password validation
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('auth_routes.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            connection.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('auth_routes.login'))  # Redirect to login after successful signup
        except pymysql.MySQLError as e:
            flash(f"Error: {e}", "error")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    return render_template('signup.html')


# Login route
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email and password are not empty
        if not email or not password:
            flash('Please enter both email and password', 'danger')
            return redirect(url_for('auth_routes.login'))

        # Check if the user exists in the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            # Compare the password (Assuming passwords are hashed in the DB)
            if check_password_hash(user['password'], password):
                
                  # Use check_password_hash to compare
                # If the password matches, redirect to profile
                return redirect(url_for('auth_routes.profile', id=user['id']))
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('User not found', 'danger')

        # If login fails, redirect back to login page
        return redirect(url_for('login'))

    return render_template('login.html')


@auth_routes.route('/logout')
def logout():
    # Remove the user session or perform other cleanup tasks
    session.pop('user_id', None)  # You can store user info in the session
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth_routes.login'))


@auth_routes.route('/profile/<id>')
def profile(id):
    # Fetch user profile data from DB
    connection = get_db_connection()
    cursor = connection.cursor()

    # Call stored procedure to fetch user bookings with bike details
    cursor.callproc('GetUserBookingsWithBikeDetails', (id))
    
    bookings = cursor.fetchall()

    cursor.close()
    connection.close()

    if bookings:
        return render_template('profile.html', bookings=bookings)
    else:
        flash('No bookings found', 'danger')
        return redirect(url_for('auth_routes.login'))
