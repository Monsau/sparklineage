-- =====================================================================
-- CRÉATION DE TABLES SUPPLÉMENTAIRES POUR LINEAGE SPARK COMPLEXE
-- =====================================================================

-- Base source : Nouvelles tables
USE source_db;

-- Table produits
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table commandes
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Table détails commandes
CREATE TABLE IF NOT EXISTS order_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insertion données produits
INSERT INTO products (product_id, product_name, category, price, stock_quantity) VALUES
(1, 'Laptop Dell XPS', 'Electronics', 1299.99, 15),
(2, 'iPhone 15 Pro', 'Electronics', 999.99, 25),
(3, 'Desk Chair', 'Furniture', 299.99, 40),
(4, 'Coffee Machine', 'Appliances', 149.99, 30),
(5, 'Notebook Set', 'Stationery', 19.99, 100);

-- Insertion données commandes
INSERT INTO orders (order_id, customer_id, order_date, total_amount, status) VALUES
(1001, 1, '2024-01-15', 1319.98, 'Completed'),
(1002, 2, '2024-01-16', 999.99, 'Shipped'),
(1003, 3, '2024-01-17', 319.98, 'Processing'),
(1004, 4, '2024-01-18', 169.98, 'Completed'),
(1005, 5, '2024-01-19', 39.98, 'Shipped');

-- Insertion données détails commandes
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1001, 1, 1, 1299.99),
(1001, 5, 1, 19.99),
(1002, 2, 1, 999.99),
(1003, 3, 1, 299.99),
(1003, 5, 1, 19.99),
(1004, 4, 1, 149.99),
(1004, 5, 1, 19.99),
(1005, 5, 2, 19.99);

-- Base target : Tables agrégées pour le data warehouse
USE target_db;

-- Table des ventes par client (agrégation)
CREATE TABLE IF NOT EXISTS customer_sales_summary (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),
    total_orders INT,
    total_amount DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    last_order_date DATE,
    customer_tier VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des ventes par produit (agrégation)
CREATE TABLE IF NOT EXISTS product_sales_summary (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    total_sold INT,
    total_revenue DECIMAL(12,2),
    avg_price DECIMAL(10,2),
    stock_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des métriques business (agrégation complexe)
CREATE TABLE IF NOT EXISTS business_metrics (
    metric_id INT PRIMARY KEY AUTO_INCREMENT,
    metric_date DATE,
    total_customers INT,
    total_orders INT,
    total_revenue DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    top_category VARCHAR(50),
    top_product VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT 'Tables créées avec succès pour le lineage Spark complexe' as status;