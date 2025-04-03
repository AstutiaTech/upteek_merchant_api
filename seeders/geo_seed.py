from sqlalchemy.orm import Session
from database.model import create_country, create_currency, create_country_currency, create_state, create_city, create_lga
from modules.utils.net import get_list_of_nigerian_states_and_cities, get_geocode_info


def run_geo_seeder(db: Session):
    ng_country = create_country(db=db, name='Nigeria', code='NG', code_two='NGA', language='English', area_code='+234', base_timezone='Africa/Lagos', latitude='9.0820', longitude='8.6753', flag='https://flagicons.lipis.dev/flags/4x3/ng.svg', visibility=1, status=1)
    ng_currency = create_currency(db=db, name='Naira', code='NGN', symbol='₦', status=1)
    create_country_currency(db=db, country_id=ng_country.id, currency_id=ng_currency.id, is_main=1)
    resp = get_list_of_nigerian_states_and_cities()
    if resp is not None:
        if resp != {}:
            state_resp = resp['states']
            if len(state_resp) > 0:
                for i in range(len(state_resp)):
                    main_state = state_resp[i]
                    state_name = ""
                    if main_state['state'] != "Federal Capital Territory":
                        state_name = main_state['state'] + " State"
                    else:
                        state_name = main_state['state']
                    state = create_state(db=db, name=state_name, capital=main_state['capital'], country_id=ng_country.id, status=1)
                    state_cities = main_state['cities']
                    if len(state_cities) > 0:
                        for j in range(len(state_cities)):
                            create_city(db=db, name=state_cities[j], state_id=state.id, status=1)
                    state_lgas = main_state['lgas']
                    if len(state_lgas) > 0:
                        for k in range(len(state_lgas)):
                            create_lga(db=db, name=state_lgas[k], state_id=state.id, status=1)
    return True