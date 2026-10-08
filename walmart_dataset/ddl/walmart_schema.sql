
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100),
    province VARCHAR(100),
    country VARCHAR(100),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active CHAR(1)
);

CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR(255),
    city VARCHAR(100),
    province VARCHAR(100),
    country VARCHAR(100),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active CHAR(1)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    brand VARCHAR(100),
    price NUMERIC(10,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active CHAR(1)
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    store_id INTEGER REFERENCES stores(store_id),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    job_title VARCHAR(100),
    salary NUMERIC(10,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active CHAR(1)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    store_id INTEGER REFERENCES stores(store_id),
    order_timestamp TIMESTAMP,
    payment_method VARCHAR(50),
    order_status VARCHAR(50),
    total_amount NUMERIC(12,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active CHAR(1)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2),
    line_amount NUMERIC(12,2),
    created_timestamp TIMESTAMP,
    updated_timestamp TIMESTAMP,
    is_active CHAR(1)
);

CREATE INDEX idx_employees_store_id ON employees(store_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_store_id ON orders(store_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
