from src.orders import get_orders
import psycopg2
import pandas as pd

customer_file = '../data/customers.csv'
orders_file = '../data/orders.csv'
product_file = '../data/products.csv'
lineitems_file = '../data/line_items.csv'


def create_csvs(df):
    df_line_items = df[['line_item_id', 'order_id', 'line_item_product_id']]
    df_line_items.to_csv(lineitems_file, index=False, header=False)

    df_products = df[['line_item_product_id', 'line_item_product_sku', 'line_item_product_name', 'line_item_price']]
    df_products = df_products.drop_duplicates(keep='first', inplace=False)
    df_products.to_csv(product_file, index=False, header=False)

    df_customers = df[['customer_id', 'customer_name', 'customer_email']]
    df_customers = df_customers.drop_duplicates(keep='first', inplace=False)
    df_customers.to_csv(customer_file, index=False, header=False)

    df_orders_db = df[['order_id', 'customer_id', 'total_price', 'currency_rate', 'created_at']]
    df_orders_db = df_orders_db.drop_duplicates(keep='first', inplace=False)
    df_orders_db.to_csv(orders_file, index=False, header=False)


def insert_from_csv(file, tbl_name):
    conn = psycopg2.connect("host=localhost dbname=namaste user=postgres")
    cur = conn.cursor()
    with open(file) as csvfile:
        cur.copy_from(csvfile, tbl_name, sep=',')
        conn.commit()
    conn.close()


def get_orders_df():
    input_fields = ['id', 'total_price', 'created_at', 'currency_rate', ['customer', 'name'], ['customer', 'id'], ['customer', 'email']]
    df_fields = {'id': 'order_id', 'customer.id': 'customer_id',
                 'customer.name': 'customer_name', 'customer.email': 'customer_email'}
    df = pd.json_normalize(json_orders, 'line_items', input_fields, record_prefix='line_item_')
    df = df.rename(columns=df_fields)
    return df


json_orders = get_orders()
df_orders = get_orders_df()
create_csvs(df_orders)
insert_from_csv(customer_file, "customers")
insert_from_csv(orders_file, "orders")
insert_from_csv(product_file, "products")
insert_from_csv(lineitems_file, "line_items")
