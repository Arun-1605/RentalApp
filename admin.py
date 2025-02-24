from flask import Blueprint, render_template, request, redirect, flash, url_for
import pymysql
from db import get_db_connection

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin')
def getadmin():
    # Fetch all bikes for the master page
    # connection = get_db_connection()
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM bikes")
    # bikes = cursor.fetchall()
    # cursor.close()
    # connection.close()
    return render_template('admin.html')

@admin_routes.route('/bike-form', methods=['GET'])
@admin_routes.route('/bike-form/<int:bike_id>', methods=['GET'])
def get_bike_form(bike_id=None):
    # Fetch bike details if updating, otherwise show empty form
    connection = get_db_connection()
    cursor = connection.cursor()

    if bike_id:
        cursor.execute("SELECT * FROM bikes WHERE id = %s", (bike_id,))
        bike = cursor.fetchone()
        return render_template('upsertbike.html',bike=bike)

    else:
        cursor.execute("SELECT * FROM bikes")
        bike = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('master.html', bikes=bike)

@admin_routes.route('/bike-form', methods=['POST'])
@admin_routes.route('/bike-form/<int:bike_id>', methods=['POST'])
def post_bike_form(bike_id=None):
    # Handle form submission for adding/updating bikes
    connection = get_db_connection()
    cursor = connection.cursor()

    # Extract form data
    bikename = request.form['bikename']
    model = request.form['model']
    price = request.form['price']
    km = request.form['km']
    isavailable = request.form['Isavailable']

    if bike_id:
        # Update existing bike details
        try:
            cursor.execute("""
                UPDATE bikes 
                SET bikename = %s, model = %s, price = %s, km = %s, isavailable = %s
                WHERE id = %s
            """, (bikename, model, price, km, isavailable, bike_id))
            connection.commit()
            flash('Bike details updated successfully!', 'success')
        except Exception as e:
            flash(f"Error: {e}", 'danger')
            connection.rollback()
    else:
        # Insert new bike details
        try:
            cursor.execute("""
                INSERT INTO bikes (bikename, model, price, km, isavailable)
                VALUES (%s, %s, %s, %s, %s)
            """, (bikename, model, price, km, isavailable))
            connection.commit()
            flash('Bike added successfully!', 'success')
        except Exception as e:
            flash(f"Error: {e}", 'danger')
            connection.rollback()

    cursor.close()
    connection.close()

    return redirect(url_for('admin_routes.getadmin'))
