import requests
import os


EXCHANGE_SOURCE = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
GA_MEASUREMENT_PROTOCOL_ENDPOINT = 'https://www.google-analytics.com/mp/collect'
EVENT_NAME = 'purchase'


def get_price():
    excange_rates = requests.get(EXCHANGE_SOURCE).json()
    usd_rate = filter(lambda rate: rate['cc'] == 'USD', excange_rates)

    usd_rate = list(usd_rate)[0]['rate']
    return usd_rate


def send_event(event, measurement_id, measurement_secret, current_stamp):
    price = get_price()
    client_id = event['client_id']
    # Send the event to the GA4 property
    url = f'{GA_MEASUREMENT_PROTOCOL_ENDPOINT}?measurement_id={measurement_id}&api_secret={measurement_secret}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'client_id': client_id,
        'non_personalized_ads': True,
        'events': [{
            'name': 'exchange_rate',
            'params': {
                'session_id': current_stamp,
                'currency': 'USD',
                'price': price
            }
        }]
    }

    requests.post(url, headers=headers, json=data, verify=True)
    return price


def handle_event(event, current_stamp):
    """Handle the event sent from the client-side JavaScript code."""
    # Get config from environment variables
    measurement_id = os.getenv('GA_PROPERTY_ID')
    measurement_secret = os.getenv('GA_MEASUREMENT_SECRET')

    return send_event(event, measurement_id, measurement_secret, current_stamp)
