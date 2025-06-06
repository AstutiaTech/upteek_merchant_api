from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Service(Base):

    __tablename__ = "services"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    code = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_service(db: Session, name: str = None, code: str = None, status: int = 0, commit: bool=False):
    service = Service(name=name, code=code, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(service)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(service)
    return service

def update_service(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Service).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_service(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Service).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_service(db: Session, id: int=0, commit: bool=False):
    db.query(Service).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_service_by_id(db: Session, id: int=0):
    return db.query(Service).filter_by(id = id).first()

def get_single_service_by_code(db: Session, code: str=None):
    return db.query(Service).filter_by(code = code).first()

def get_services(db: Session):
    return db.query(Service).order_by(desc(Service.created_at))
