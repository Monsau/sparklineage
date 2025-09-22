-- Create source database schema
CREATE DATABASE IF NOT EXISTS source_db;
USE source_db;

-- Create sample data tables following OpenMetadata lineage example
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Insert sample data
INSERT INTO customers VALUES 
(1, 'John Smith', 'john@email.com', 'New York', 'USA', NOW()),
(2, 'Jane Doe', 'jane@email.com', 'London', 'UK', NOW()),
(3, 'Mike Johnson', 'mike@email.com', 'Paris', 'France', NOW()),
(4, 'Sarah Wilson', 'sarah@email.com', 'Tokyo', 'Japan', NOW()),
(5, 'David Brown', 'david@email.com', 'Sydney', 'Australia', NOW());

INSERT INTO orders VALUES 
(101, 1, '2025-01-15', 250.00, 'completed'),
(102, 2, '2025-01-16', 150.75, 'completed'),
(103, 1, '2025-01-17', 89.99, 'pending'),
(104, 3, '2025-01-18', 320.50, 'completed'),
(105, 4, '2025-01-19', 75.25, 'shipped'),
(106, 5, '2025-01-20', 199.99, 'completed'),
(107, 2, '2025-01-21', 45.00, 'pending');
