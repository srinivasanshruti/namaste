import json
from src.exchange import get_rate_for_date


def load_json():
    with open('../data/orders.json') as input_file:
        orders = json.load(input_file)
    return orders


# gets exchange rate for each unique order date and adds the currency_rate property to each order
def get_rates_json(orders):
    rates = {}
    dates = set(order["created_at"][:10] for order in orders)
    for date in dates:
        rates[date] = get_rate_for_date(date)
    for order in orders:
        odate = order["created_at"][:10]
        order["currency_rate"] = rates[odate]


# writes orders with currency rate to a new json
def create_json_curr(orders):
    with open('../data/orders_with_curr.json', 'w') as output_file:
        json.dump(orders, output_file)


def load_orders_data():
    orders = load_json()
    get_rates_json(orders)
    create_json_curr(orders)


# returns the extended orders json file
def get_orders():
    with open('../data/orders_with_curr.json') as input_file:
        json_orders = json.load(input_file)
    return json_orders


if __name__ == "__main__":
    load_orders_data()
