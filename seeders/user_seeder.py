from database.model import create_user_with_relevant_rows
from sqlalchemy.orm import Session

def run_user_seeder(db: Session):
    create_user_with_relevant_rows(db=db, country_id=1, username="superadmin", email="astutiatechnologies@gmail.com", phone_number="+2348086118180", password="secret", user_type=1, role=1, first_name="Super", other_name="Admin", last_name="User", is_merchant=False, merchant_name=None)
    create_user_with_relevant_rows(db=db, country_id=1, username="bankhead", email="kiceej@gmail.com", phone_number="+2349117954219", password="secret", user_type=2, role=1, first_name="Bank", other_name="Head", last_name="User", is_merchant=False, merchant_name=None)
    create_user_with_relevant_rows(db=db, country_id=1, username="merchanthead", email="siscorule@gmail.com", phone_number="+2347063520766", password="secret", user_type=3, role=1, first_name="Merchant", other_name="Head", last_name="User", is_merchant=True, merchant_name="Sisco Inc.")
    create_user_with_relevant_rows(db=db, country_id=1, username="customer", email="jornkalu10@gmail.com", phone_number="+2347072684199", password="secret", user_type=4, role=1, first_name="Customer", other_name="User", last_name="User", is_merchant=False, merchant_name=None)
    return True