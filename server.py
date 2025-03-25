
from flask import Flask, jsonify, request, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, Employee, Shift, Product, Supplier, Sale
from datetime import datetime
import hashlib
import os

app = Flask(__name__)
engine = create_engine('sqlite:///business.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    session = Session()
    employee = session.query(Employee).filter_by(
        username=data['username']
    ).first()
    
    if employee and employee.password == hash_password(data['password']):
        return jsonify({
            "success": True,
            "user": {
                "id": employee.id,
                "username": employee.username,
                "role": employee.role
            }
        })
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route('/api/employees', methods=['GET', 'POST'])
def manage_employees():
    session = Session()
    if request.method == 'GET':
        employees = session.query(Employee).all()
        return jsonify([{
            'id': e.id,
            'username': e.username,
            'full_name': e.full_name,
            'role': e.role,
            'email': e.email,
            'department': e.department,
            'salary': e.salary
        } for e in employees])
    else:
        data = request.json
        employee = Employee(
            username=data['username'],
            password=hash_password(data['password']),
            full_name=data['full_name'],
            role=data['role'],
            email=data['email'],
            department=data['department'],
            salary=data['salary'],
            hire_date=datetime.now()
        )
        session.add(employee)
        session.commit()
        return jsonify({"success": True, "id": employee.id})

@app.route('/api/shifts', methods=['GET', 'POST'])
def manage_shifts():
    session = Session()
    if request.method == 'GET':
        shifts = session.query(Shift).all()
        return jsonify([{
            'id': s.id,
            'employee_id': s.employee_id,
            'start_time': s.start_time.isoformat(),
            'end_time': s.end_time.isoformat(),
            'status': s.status
        } for s in shifts])
    else:
        data = request.json
        shift = Shift(
            employee_id=data['employee_id'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            status=data['status']
        )
        session.add(shift)
        session.commit()
        return jsonify({"success": True, "id": shift.id})

@app.route('/api/inventory', methods=['GET', 'POST'])
def manage_inventory():
    session = Session()
    if request.method == 'GET':
        products = session.query(Product).all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'quantity': p.quantity,
            'supplier_id': p.supplier_id
        } for p in products])
    else:
        data = request.json
        product = Product(
            name=data['name'],
            price=data['price'],
            quantity=data['quantity'],
            reorder_level=data['reorder_level'],
            supplier_id=data['supplier_id']
        )
        session.add(product)
        session.commit()
        return jsonify({"success": True, "id": product.id})

@app.route('/api/sales', methods=['GET', 'POST'])
def manage_sales():
    session = Session()
    if request.method == 'GET':
        sales = session.query(Sale).all()
        return jsonify([{
            'id': s.id,
            'date': s.date.isoformat(),
            'product_id': s.product_id,
            'quantity': s.quantity,
            'total_amount': s.total_amount
        } for s in sales])
    else:
        data = request.json
        sale = Sale(
            date=datetime.now(),
            product_id=data['product_id'],
            quantity=data['quantity'],
            total_amount=data['total_amount'],
            employee_id=data['employee_id']
        )
        # Update inventory
        product = session.query(Product).get(data['product_id'])
        product.quantity -= data['quantity']
        session.add(sale)
        session.commit()
        return jsonify({"success": True, "id": sale.id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
