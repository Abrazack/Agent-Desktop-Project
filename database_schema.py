
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(256))
    full_name = Column(String(100))
    role = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    department = Column(String(50))
    job_title = Column(String(50))
    salary = Column(Float)
    hire_date = Column(DateTime)
    shifts = relationship("Shift", back_populates="employee")

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(20))  # scheduled, completed, absent
    employee = relationship("Employee", back_populates="shifts")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Float)
    quantity = Column(Integer)
    reorder_level = Column(Integer)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    supplier = relationship("Supplier", back_populates="products")

class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    contact = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    products = relationship("Product", back_populates="supplier")

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    total_amount = Column(Float)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    product = relationship("Product")
    employee = relationship("Employee")
