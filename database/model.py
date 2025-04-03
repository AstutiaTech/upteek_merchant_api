from typing import Dict
from sqlalchemy.orm import Session
from models.account_types import AccountType, create_account_type, update_account_type, delete_account_type, force_delete_account_type, get_single_account_type_by_id, get_account_types
from models.accounts import Account, create_account, update_account, delete_account, force_delete_account, get_single_account_by_id, get_accounts
from models.addresses import Address, create_address, update_address, delete_address, force_delete_address, get_single_address_by_id, get_addresses, get_addresses_by_addressable_type, get_addressable
from models.auth_tokens import AuthToken, create_auth_token, update_auth_token, update_user_auth_token, delete_auth_token, force_delete_auth_token, get_single_auth_token_by_id, get_auth_tokens, get_auth_tokens_by_user_id, get_latest_user_auth_token
from models.beneficiaries import Beneficiary, create_beneficiary, update_beneficiary, delete_beneficiary, force_delete_beneficiary, get_single_beneficiary_by_id, get_beneficiaries
from models.bill_categories import BillCategory, create_bill_category, update_bill_category, delete_bill_category, force_delete_bill_category, get_single_bill_category_by_id, get_bill_categories
from models.bills import Bill, create_bill, update_bill, delete_bill, force_delete_bill, get_single_bill_by_id, get_bills
from models.cards import Card, create_card, update_card, delete_card, force_delete_card, get_single_card_by_id, get_cards
from models.categories import Category, create_category, update_category, delete_category, force_delete_category, get_single_category_by_id, get_categories
from models.cities import City, create_city, update_city, delete_city, force_delete_city, get_single_city_by_id, get_capital_city, get_cities, get_cities_by_state_id
from models.collections import Collection, create_collection, update_collection, delete_collection, force_delete_collection, get_single_collection_by_id, get_collections
from models.countries_currencies import CountryCurrency, create_country_currency, update_country_currency, delete_country_currency, force_delete_country_currency, get_single_country_currency_by_id, get_countries_currencies, get_countries_currencies_by_country_id, get_countries_currencies_by_currency_id
from models.countries import Country, create_country, update_country, delete_country, force_delete_country, get_single_country_by_id
from models.currencies import Currency, create_currency, update_currency, delete_currency, force_delete_currency, get_single_currency_by_id, get_single_currency_by_code, get_currencies
from models.deposits import Deposit, create_deposit, update_deposit, delete_deposit, force_delete_deposit, get_single_deposit_by_id, get_deposits
from models.financial_institutions import FinancialInstitution, create_financial_institution, update_financial_institution, delete_financial_institution, force_delete_financial_institution, get_single_financial_institution_by_id, get_financial_institutions
from models.financial_products import FinancialProduct, create_financial_product, update_financial_product, delete_financial_product, force_delete_financial_product, get_single_financial_product_by_id, get_financial_products
from models.general_ledger_account_types import GeneralLedgerAccountType, create_general_ledger_account_type, update_general_ledger_account_type, delete_general_ledger_account_type, force_delete_general_ledger_account_type, get_single_general_ledger_account_type_by_id, get_general_ledger_account_types
from models.general_ledger_accounts import GeneralLedgerAccount, create_general_ledger_account, update_general_ledger_account, delete_general_ledger_account, force_delete_general_ledger_account, get_single_general_ledger_account_by_id, get_general_ledger_accounts
from models.l_g_a_s import LGA, create_lga, update_lga, delete_lga, force_delete_lga, get_single_lga_by_id, get_lgas, get_lgas_by_state_id
from models.loan_applications import LoanApplication, create_loan_application, update_loan_application, delete_loan_application, force_delete_loan_application, get_single_loan_application_by_id
from models.loans import Loan, create_loan, update_loan, delete_loan, force_delete_loan, get_single_loan_by_id, get_loans
from models.media import Medium, create_medium, update_medium, delete_medium, force_delete_medium, get_single_medium_by_id, get_media, get_media_by_mediumable_type, get_mediumable
from models.merchant_categories import MerchantCategory, create_merchant_category, update_merchant_category, delete_merchant_category, force_delete_merchant_category, get_single_merchant_category_by_id, get_merchant_categories, get_merchant_categories_by_industry_id
from models.merchant_industries import MerchantIndustry, create_merchant_industry, update_merchant_industry, delete_merchant_industry, force_delete_merchant_industry, get_single_merchant_industry_by_id, get_merchant_industries
from models.merchants import Merchant, create_merchant, update_merchant, delete_merchant, force_delete_merchant, get_single_merchant_by_id, get_single_merchant_by_user_id, get_merchants, get_merchants_by_category_id
from models.messages import Message, create_message, update_message, delete_message, force_delete_message, get_all_messages
from models.notifications import Notification, create_notification, update_notification, delete_notification, force_delete_notification, get_all_notifications
from models.operators import Operator, create_operator, update_operator, delete_operator, force_delete_operator, get_single_operator_by_id, get_operators
from models.orders_products import OrderProduct, create_order_product, update_order_product, delete_order_product, force_delete_order_product, get_all_orders_products
from models.orders import Order, create_order, update_order, delete_order, force_delete_order, get_single_order_by_id, get_orders
from models.people import Person, create_person, update_person, delete_person, force_delete_person, get_single_person_by_id, get_people, get_people_by_personable_type, get_personable
from models.products_categories import ProductCategory, create_product_category, update_product_category, delete_product_category, force_delete_product_category, get_all_products_categories
from models.products import Product, create_product, update_product, delete_product, force_delete_product, get_single_product_by_id, get_products
from models.profiles import Profile, create_profile, update_profile, update_profile_by_user_id, delete_profile, force_delete_profile, get_single_profile_by_id, get_single_profile_by_user_id
from models.providers import Provider, create_provider, update_provider, delete_provider, force_delete_provider, get_single_provider_by_id, get_single_provider_by_code, get_providers
from models.services import Service, create_service, update_service, delete_service, force_delete_service, get_single_service_by_id, get_single_service_by_code, get_services
from models.settings import Setting, create_setting, update_setting, update_setting_by_user_id, delete_setting, force_delete_setting, get_single_setting_by_id, get_single_setting_by_user_id
from models.states import State, create_state, update_state, delete_state, force_delete_state, get_single_state_by_id, get_states, get_states_by_country_id
from models.system_configurations import SystemConfiguration, create_system_configuration, update_system_configuration, delete_system_configuration, force_delete_system_configuration, get_single_system_configuration_by_id, get_single_system_configuration_by_name, get_system_configurations
from models.tokens import Token, create_token, update_token, update_token_by_user_id, update_token_by_user_id_and_token_type, update_token_email, delete_token, force_delete_token, get_single_token_by_id, get_tokens, get_tokens_by_user_id, get_latest_user_token, get_latest_user_token_by_type, get_latest_user_token_by_type_and_status
from models.transaction_fees import TransactionFee, create_transaction_fee, update_transaction_fee, delete_transaction_fee, force_delete_transaction_fee, get_all_transaction_fees
from models.transaction_types import TransactionType, create_transaction_type, update_transaction_type, delete_transaction_type, force_delete_transaction_type, get_single_transaction_type_by_id, get_transaction_types
from models.transactions import Transaction, create_transaction, update_transaction, delete_transaction, force_delete_transaction, get_single_transaction_by_id, get_transactions
from models.user_device_logs import UserDeviceLog, create_user_device_log, update_user_device_log, delete_user_device_log, force_delete_user_device_log, get_single_user_device_log_by_id, get_user_devices_logs, get_user_device_logs_by_user_device_id
from models.user_devices import UserDevice, create_user_device, update_user_device, delete_user_device, force_delete_user_device, get_single_user_device_by_id, get_user_devices, get_user_devices_by_user_id
from models.users import User, create_user, update_user, delete_user, force_delete_user, get_single_user_by_id, get_single_user_by_email, get_single_user_by_email_and_user_type, get_single_user_by_phone_number, get_single_user_by_phone_number_and_user_type, get_single_user_by_username, get_single_user_by_username_user_type, get_single_user_by_any_main_details, get_users, get_users_by_country_id, get_users_by_merchant_id, get_users_by_user_type, get_users_by_role, get_users_by_user_type_and_role
import string
import random
from database.db import get_laravel_datetime
from modules.utils.auth import AuthHandler

auth = AuthHandler()

def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_user_with_relevant_rows(db: Session, country_id: int = 0, username: str = None, email: str = None, phone_number: str = None, password: str = None, device_token: str = None, external_provider: str = None, external_reference: str = None, user_type: int = 0, role: int = 0, first_name: str = None, other_name: str = None, last_name: str = None, is_merchant: bool=False, merchant_name: str = None):
    hashed_password = None
    if password is not None:
        hashed_password = auth.get_password_hash(password=password)
    user = create_user(db=db, country_id=country_id, username=username, email=email, phone_number=phone_number, password=hashed_password, device_token=device_token, external_provider=external_provider, external_reference=external_reference, user_type=user_type, role=role, status=1)
    create_profile(db=db, user_id=user.id, first_name=first_name, other_name=other_name, last_name=last_name, level_one_approved_by=1, level_one_approved_at=get_laravel_datetime())
    create_setting(db=db, user_id=user.id)
    if is_merchant == True:
        merchant = create_merchant(db=db, user_id=user.id, name=merchant_name)
        update_user(db=db, id=user.id, values={'merchant_id': merchant.id})
    return True