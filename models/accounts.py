from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Account(Base):

    __tablename__ = "accounts"
     
    id = Column(BigInteger, primary_key=True, index=True)
    account_type_id = Column(BigInteger, default=0)
    user_id = Column(BigInteger, default=0)
    merchant_id = Column(BigInteger, default=0)
    account_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    nuban = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    proviexternal_referenceder = Column(String, nullable=True)
    available_balance = Column(Float, default=0)
    ledger_balance = Column(Float, default=0)
    sms_notification = Column(SmallInteger, default=0)
    email_notification = Column(SmallInteger, default=0)
    is_primary = Column(SmallInteger, default=0)
    manager_id = Column(BigInteger, default=0)
    last_active_at = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(SmallInteger, default=0)
    meta_data = Column(Text, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_account(db: Session, account_type_id: int = 0, user_id: int = 0, merchant_id: int = 0, account_name: str = None, account_number: str = None, nuban: str = None, provider: str = None, proviexternal_referenceder: str = None, available_balance: float = 0, ledger_balance: float = 0, sms_notification: int = 0, email_notification: int = 0, is_primary: int = 0, manager_id: int = 0, last_active_at: str = None, status: int = 0, meta_data: str = None, deleted_at: str = None, commit: bool=False):
    account = Account(account_type_id=account_type_id, user_id=user_id, merchant_id=merchant_id, account_name=account_name, account_number=account_number, nuban=nuban, provider=provider, proviexternal_referenceder=proviexternal_referenceder, available_balance=available_balance, ledger_balance=ledger_balance, sms_notification=sms_notification, email_notification=email_notification, is_primary=is_primary, manager_id=manager_id, last_active_at=last_active_at, status=status, meta_data=meta_data, deleted_at=deleted_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(account)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(account)
    return account

def update_account(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Account).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_account(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Account).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_account(db: Session, id: int=0, commit: bool=False):
    db.query(Account).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_account_by_id(db: Session, id: int=0):
    return db.query(Account).filter_by(id = id).first()

def get_accounts(db: Session, filters: Dict={}):
    query = db.query(Account)
    if 'account_type_id' in filters:
        query = query.filter_by(account_type_id = filters['account_type_id'])
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'account_name' in filters:
        query = query.filter(Account.account_name.like("%" + filters['account_name'] + "%"))
    if 'account_number' in filters:
        query = query.filter(Account.account_number.like("%" + filters['account_number'] + "%"))
    if 'nuban' in filters:
        query = query.filter(Account.nuban.like("%" + filters['nuban'] + "%"))
    if 'provider' in filters:
        query = query.filter(Account.provider.like("%" + filters['provider'] + "%"))
    if 'manager_id' in filters:
        query = query.filter_by(manager_id = filters['manager_id'])
    return query.order_by(desc(Account.created_at))