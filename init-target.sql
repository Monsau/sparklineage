-- Create target database schema
CREATE DATABASE IF NOT EXISTS target_db;
USE target_db;

-- Create data warehouse tables for transformed data
CREATE TABLE customer_summary (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    total_orders INT DEFAULT 0,
    total_spent DECIMAL(12,2) DEFAULT 0.00,
    last_order_date DATE,
    customer_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE order_analytics (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    amount_category VARCHAR(20),
    days_since_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
