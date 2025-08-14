-- =========================================
-- Product Catalog - Initial Schema & Data
-- =========================================

-- Create product table if it doesn't exist
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    brand VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create admin table if it doesn't exist
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert example product (only if it doesn't already exist)
INSERT INTO product (sku, name, price, brand)
SELECT 'SKU123', 'Example Product', 19.99, 'Brand A'
WHERE NOT EXISTS (
    SELECT 1 FROM product WHERE sku = 'SKU123'
);

-- Insert example admin (only if it doesn't already exist)
INSERT INTO admin (username, password, email, created_at)
SELECT 'admin',
       '$2b$12$XrslPzR65zHkUe5g3KMq1u2i1w1s7Y2c3oDWvKhEwO2R2Z0MQAay6',
       'admin@zebrands.com',
       NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM admin WHERE username = 'admin'
);
