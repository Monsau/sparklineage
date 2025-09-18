-- Tables target (agrégées)
USE target_db;

-- Table des ventes par client (agrégation)
CREATE TABLE IF NOT EXISTS customer_sales_summary (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
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

SELECT 'Tables target créées avec succès' as status;