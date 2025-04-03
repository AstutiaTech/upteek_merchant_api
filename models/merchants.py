from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Merchant(Base):

    __tablename__ = "merchants"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    category_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    trading_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    email = Column(String, nullable=True)
    phone_number_one = Column(String, nullable=True)
    phone_number_two = Column(String, nullable=True)
    opening_hours = Column(String, nullable=True)
    closing_hours = Column(String, nullable=True)
    logo = Column(Text, nullable=True)
    thumbnail = Column(Text, nullable=True)
    certificate = Column(Text, nullable=True)
    memorandum = Column(Text, nullable=True)
    utility_bill = Column(Text, nullable=True)
    building = Column(Text, nullable=True)
    compliance_status = Column(SmallInteger, default=0)
    compliance_approved_by = Column(BigInteger, default=0)
    compliance_approved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    compliance_rejected_by = Column(BigInteger, default=0)
    compliance_rejected_at = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_merchant(db: Session, user_id: int = 0, category_id: int = 0, name: str = None, trading_name: str = None, description: str = None, email: str = None, phone_number_one: str = None, phone_number_two: str = None, opening_hours: str = None, closing_hours: str = None, logo: str = None, thumbnail: str = None, certificate: str = None, memorandum: str = None, utility_bill: str = None, building: str = None, compliance_status: int = 0, compliance_approved_by: int = 0, compliance_approved_at: str = None, compliance_rejected_by: int = 0, compliance_rejected_at: str = None, status: int = 0, commit: bool=False):
    merchant = Merchant(user_id=user_id, category_id=category_id, name=name, trading_name=trading_name, description=description, email=email, phone_number_one=phone_number_one, phone_number_two=phone_number_two, opening_hours=opening_hours, closing_hours=closing_hours, logo=logo, thumbnail=thumbnail, certificate=certificate, memorandum=memorandum, utility_bill=utility_bill, building=building, compliance_status=compliance_status, compliance_approved_by=compliance_approved_by, compliance_approved_at=compliance_approved_at,compliance_rejected_by=compliance_rejected_by, compliance_rejected_at=compliance_rejected_at, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(merchant)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(merchant)
    return merchant

def update_merchant(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Merchant).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_merchant(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Merchant).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_merchant(db: Session, id: int=0, commit: bool=False):
    db.query(Merchant).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_merchant_by_id(db: Session, id: int=0):
    return db.query(Merchant).filter_by(id = id).first()

def get_single_merchant_by_user_id(db: Session, user_id: int=0):
    return db.query(Merchant).filter_by(user_id = user_id).first()

def get_merchants(db: Session):
    return db.query(Merchant).filter(Merchant.deleted_at == None).order_by(desc(Merchant.id))

def get_merchants_by_category_id(db: Session, category_id: int=0):
    return db.query(Merchant).filter_by(category_id = category_id).filter(Merchant.deleted_at == None).order_by(desc(Merchant.id))