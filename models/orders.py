from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Order(Base):

    __tablename__ = "orders"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    merchant_id = Column(BigInteger, default=0)
    currency_id = Column(BigInteger, default=0)
    card_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    financial_product_id = Column(BigInteger, default=0)
    order_type = Column(Integer, default=0)
    sub_total = Column(Float, default=0)
    delivery_fee = Column(Float, default=0)
    VAT = Column(Float, default=0)
    discount = Column(Float, default=0)
    total_amount = Column(Float, default=0)
    estimated_delivery_time = Column(String, nullable=True)
    payment_type = Column(Integer, default=0)
    order_detail = Column(Text, nullable=True)
    pick_up_pin = Column(String, nullable=True)
    delivery_pin = Column(String, nullable=True)
    is_gift = Column(SmallInteger, default=0)
    receiver_phone_number = Column(String, nullable=True)
    receiver_house_number = Column(String, nullable=True)
    receiver_street = Column(String, nullable=True)
    receiver_nearest_bus_stop = Column(String, nullable=True)
    receiver_city = Column(String, nullable=True)
    receiver_state = Column(String, nullable=True)
    receiver_country = Column(String, nullable=True)
    receiver_latitude = Column(String, nullable=True)
    receiver_longitude = Column(String, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    is_scheduled = Column(SmallInteger, default=0)
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    preparation_at = Column(TIMESTAMP(timezone=True), nullable=True)
    ready_at = Column(TIMESTAMP(timezone=True), nullable=True)
    picked_up_at = Column(TIMESTAMP(timezone=True), nullable=True)
    delivered_at = Column(TIMESTAMP(timezone=True), nullable=True)
    rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    cancelled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_order(db: Session, user_id: int = 0, merchant_id: int = 0, currency_id: int = 0, card_id: int = 0, account_id: int = 0, financial_product_id: int = 0, order_type: int = 0, sub_total: float = 0, delivery_fee: float = 0, VAT: float = 0, discount: float = 0, total_amount: float = 0, estimated_delivery_time: str = None, payment_type: int = 0, order_detail: str = None, pick_up_pin: str = None, delivery_pin: str = None, is_gift: int = 0, receiver_phone_number: str = None, receiver_house_number: str = None, receiver_street: str = None, receiver_nearest_bus_stop: str = None, receiver_city: str = None, receiver_state: str = None, receiver_country: str = None, receiver_latitude: str = None, receiver_longitude: str = None, rejection_reason: str = None, cancellation_reason: str = None, is_scheduled: int = 0, scheduled_at: str = None, preparation_at: str = None, ready_at: str = None, picked_up_at: str = None, delivered_at: str = None, rejected_at: str = None, cancelled_at: str = None, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    order = Order(user_id=user_id, merchant_id=merchant_id, currency_id=currency_id, card_id=card_id, account_id=account_id, financial_product_id=financial_product_id, order_type=order_type, sub_total=sub_total, delivery_fee=delivery_fee, VAT=VAT, discount=discount, total_amount=total_amount, estimated_delivery_time=estimated_delivery_time, payment_type=payment_type, order_detail=order_detail, pick_up_pin=pick_up_pin, delivery_pin=delivery_pin, is_gift=is_gift, receiver_phone_number=receiver_phone_number, receiver_house_number=receiver_house_number, receiver_street=receiver_street, receiver_nearest_bus_stop=receiver_nearest_bus_stop, receiver_city=receiver_city, receiver_state=receiver_state, receiver_country=receiver_country, receiver_latitude=receiver_latitude, receiver_longitude=receiver_longitude, rejection_reason=rejection_reason, cancellation_reason=cancellation_reason, is_scheduled=is_scheduled, scheduled_at=scheduled_at, preparation_at=preparation_at, ready_at=ready_at, picked_up_at=picked_up_at, delivered_at=delivered_at, rejected_at=rejected_at, cancelled_at=cancelled_at, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(order)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(order)
    return order

def update_order(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Order).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_order(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Order).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_order(db: Session, id: int=0, commit: bool=False):
    db.query(Order).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_order_by_id(db: Session, id: int=0):
    return db.query(Order).filter_by(id = id).first()

def get_orders(db: Session, filters: Dict={}):
    query = db.query(Order)
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'card_id' in filters:
        query = query.filter_by(card_id = filters['card_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'financial_product_id' in filters:
        query = query.filter_by(financial_product_id = filters['financial_product_id'])
    if 'order_type' in filters:
        query = query.filter_by(order_type = filters['order_type'])
    if 'payment_type' in filters:
        query = query.filter_by(payment_type = filters['payment_type'])
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    if 'is_gift' in filters:
        query = query.filter_by(is_gift = filters['is_gift'])
    if 'is_scheduled' in filters:
        query = query.filter_by(is_scheduled = filters['is_scheduled'])
    return query.order_by(desc(Order.created_at))