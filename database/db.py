from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, mapper
from settings.config import load_env_config
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

config = load_env_config()

# SQLALCHEMY_DATABASE_URL  = "mysql://" + str(config['database_user']) + ":" + str(config['database_pass']) + "@" + str(config['server']) + "/" + str(config['database']) + "?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL  = config['cleardb_database_url']
# SQLALCHEMY_DATABASE_URL  = 'postgresql://ev_tech:gpoaqhqhZN0OQYNIqO1XAk5O2QKB9ceo@dpg-cnc47df79t8c73eq5ibg-a/ev_tech'
# SQLALCHEMY_DATABASE_URL  = "mysql://root:@127.0.0.1/puprplepayapp?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=60)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)

Base = declarative_base()

session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def get_laravel_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# def get_added_laravel_datetime(days=1):
#     begin = date.today()
#     end = begin + timedelta(days=days)
#     return end.strftime("%Y-%m-%d %H:%M:%S")
    
def get_added_laravel_datetime(days=1):
    begin = datetime.today()
    end = begin + timedelta(days=days)
    return str(int(end.timestamp()))

# def compare_laravel_datetime_with_today(datetime_str=None):
#     if datetime_str is None:
#         return False
#     else:
#         com_datetime_str = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
#         dnow = datetime.now()
#         if com_datetime_str.time() > dnow.time():
#             return True
#         else:
#             return False
            
def compare_laravel_datetime_with_today(datetime_str=None):
    if datetime_str is None:
        return False
    else:
        fu_ts = int(datetime_str)
        dnow = int(datetime.now().timestamp())
        if fu_ts > dnow:
            return True
        else:
            return False

def has_uncommitted_changes(db: Session) -> bool:
    return db.dirty or db.new or db.deleted

def is_object_modified(db: Session, obj) -> bool:
    return db.is_modified(obj)

def has_active_transaction(db: Session) -> bool:
    return db.in_transaction()
