create table customers
(
    customer_id    integer PRIMARY KEY,
    customer_name  text,
    customer_email text
);

create table products
(
    product_id   integer primary key,
    product_sku  text,
    product_name text
);

create table orders
(
    order_id        numeric primary key,
    customer_id     integer references customers,
    total_price_usd numeric,
    currency_rate   numeric,
    created_at      timestamp with time zone
);
-- Assuming line_item_id will not not repeat within a single order
create table line_items
(
    line_item_id integer not null,
    order_id     numeric not null references orders,
    product_id   integer references products,
    price        numeric,
    primary key (line_item_id, order_id)
);