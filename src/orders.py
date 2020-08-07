import json
from src.exchange import get_rate_for_date


def load_json():
    with open('../data/orders.json') as input_file:
        orders = json.load(input_file)
    return orders


def get_rates_json(orders):
    rates = {}
    dates = set(order["created_at"][:10] for order in orders)
    print(dates)
    for date in dates:
        rates[date] = get_rate_for_date(date)
    for order in orders:
        odate = order["created_at"][:10]
        order["currency_rate"] = rates[odate]


def create_json_curr(orders):
    with open('../data/orders_with_curr.json', 'w') as output_file:
        json.dump(orders, output_file)


def load_orders_data():
    orders = load_json()
    get_rates_json(orders)
    create_json_curr(orders)


def get_orders():
    with open('../data/orders_with_curr.json') as input_file:
        json_orders = json.load(input_file)
    return json_orders


load_orders_data()
