from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Transaction(Base):

    __tablename__ = "transactions"
     
    id = Column(BigInteger, primary_key=True, index=True)
    country_id = Column(BigInteger, default=0)
    currency_id = Column(BigInteger, default=0)
    user_id = Column(BigInteger, default=0)
    merchant_id = Column(BigInteger, default=0)
    gl_id = Column(BigInteger, default=0)
    account_id = Column(BigInteger, default=0)
    type_id = Column(BigInteger, default=0)
    order_id = Column(BigInteger, default=0)
    loan_id = Column(BigInteger, default=0)
    collection_id = Column(BigInteger, default=0)
    card_id = Column(BigInteger, default=0)
    institution_id = Column(BigInteger, default=0)
    bill_id = Column(BigInteger, default=0)
    beneficiary_id = Column(BigInteger, default=0)
    reference = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    narration = Column(Text, nullable=True)
    amount = Column(Float, default=0)
    previous_balance = Column(Float, default=0)
    new_balance = Column(Float, default=0)
    external_session_id = Column(String, nullable=True)
    external_account_name = Column(String, nullable=True)
    external_account_number = Column(String, nullable=True)
    external_bvn = Column(String, nullable=True)
    external_account_type = Column(String, nullable=True)
    external_bank_code = Column(String, nullable=True)
    external_location = Column(String, nullable=True)
    biller_name = Column(String, nullable=True)
    biller_customer_id = Column(String, nullable=True)
    value_date = Column(String, nullable=True)
    meta_data = Column(Text, nullable=True)
    extra_meta_data = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    authorized_by = Column(BigInteger, default=0)
    authorized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

def create_transaction(db: Session, country_id: int = 0, currency_id: int = 0, user_id: int = 0, merchant_id: int = 0, gl_id: int = 0, account_id: int = 0, type_id: int = 0, order_id: int = 0, loan_id: int = 0, collection_id: int = 0, card_id: int = 0, institution_id: int = 0, bill_id: int = 0, beneficiary_id: int = 0, reference: str = None, external_reference: str = None, description: str = None, narration: str = None, amount: float = 0, previous_balance: float = 0, new_balance: float = 0, external_session_id: str = None, external_account_name: str = None, external_account_number: str = None, external_bvn: str = None, external_account_type: str = None, external_bank_code: str = None, external_location: str = None, biller_name: str = None, biller_customer_id: str = None, value_date: str = None, meta_data: str = None, extra_meta_data: str = None, status: int = 0, created_by: int = 0, authorized_by: int = 0, authorized_at: str = None, commit: bool=False):
    trans = Transaction(country_id=country_id, currency_id=currency_id, user_id=user_id, merchant_id=merchant_id, gl_id=gl_id, account_id=account_id, type_id=type_id, order_id=order_id, loan_id=loan_id, collection_id=collection_id, card_id=card_id, institution_id=institution_id, bill_id=bill_id, beneficiary_id=beneficiary_id, reference=reference, external_reference=external_reference, description=description, narration=narration, amount=amount, previous_balance=previous_balance, new_balance=new_balance, external_session_id=external_session_id, external_account_name=external_account_name, external_account_number=external_account_number, external_bvn=external_bvn, external_account_type=external_account_type, external_bank_code=external_bank_code, external_location=external_location, biller_name=biller_name, biller_customer_id=biller_customer_id, value_date=value_date, meta_data=meta_data, extra_meta_data=extra_meta_data, status=status, created_by=created_by, authorized_by=authorized_by, authorized_at=authorized_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(trans)
    if commit == False:
        db.flush()
    else:
        db.commit()
        db.refresh(trans)
    return trans

def update_transaction(db: Session, id: int=0, values: Dict={}, commit: bool=False):
    values['updated_at'] = get_laravel_datetime()
    db.query(Transaction).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def delete_transaction(db: Session, id: int=0, commit: bool=False):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Transaction).filter_by(id = id).update(values)
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def force_delete_transaction(db: Session, id: int=0, commit: bool=False):
    db.query(Transaction).filter_by(id = id).delete()
    if commit == False:
        db.flush()
    else:
        db.commit()
    return True

def get_single_transaction_by_id(db: Session, id: int=0):
    return db.query(Transaction).filter_by(id = id).first()

def get_transactions(db: Session, filters: Dict={}):
    query = db.query(Transaction)
    if 'country_id' in filters:
        query = query.filter_by(country_id = filters['country_id'])
    if 'currency_id' in filters:
        query = query.filter_by(currency_id = filters['currency_id'])
    if 'user_id' in filters:
        query = query.filter_by(user_id = filters['user_id'])
    if 'merchant_id' in filters:
        query = query.filter_by(merchant_id = filters['merchant_id'])
    if 'gl_id' in filters:
        query = query.filter_by(gl_id = filters['gl_id'])
    if 'account_id' in filters:
        query = query.filter_by(account_id = filters['account_id'])
    if 'type_id' in filters:
        query = query.filter_by(type_id = filters['type_id'])
    if 'order_id' in filters:
        query = query.filter_by(order_id = filters['order_id'])
    if 'loan_id' in filters:
        query = query.filter_by(loan_id = filters['loan_id'])
    if 'collection_id' in filters:
        query = query.filter_by(collection_id = filters['collection_id'])
    if 'card_id' in filters:
        query = query.filter_by(card_id = filters['card_id'])
    if 'institution_id' in filters:
        query = query.filter_by(institution_id = filters['institution_id'])
    if 'bill_id' in filters:
        query = query.filter_by(bill_id = filters['bill_id'])
    if 'beneficiary_id' in filters:
        query = query.filter_by(beneficiary_id = filters['beneficiary_id'])
    if 'reference' in filters:
        query = query.filter(Transaction.reference.like('%' + filters['reference'] + '%'))
    if 'external_reference' in filters:
        query = query.filter(Transaction.external_reference.like('%' + filters['external_reference'] + '%'))
    if 'status' in filters:
        query = query.filter_by(status = filters['status'])
    return query.order_by(desc(Transaction.created_at))