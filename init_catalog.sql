-- =========================================
-- Product Catalog - Initial Schema & Data
-- =========================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS admin;

-- Create admin table if it doesn't exist
CREATE TABLE IF NOT EXISTS admin (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert example admin (only if it doesn't already exist)
INSERT INTO admin (username, password, email, created_at)
SELECT 'admin',
       '$2b$12$IUi2dfK46TaO6.jSF5yVUu2DHIL4QmShxCcmIm9QSUgI7kZx4cUA2',
       'admin@zebrands.com',
       NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM admin WHERE username = 'admin'
);

-- Drop existing tables if they exist
DROP TABLE IF EXISTS product;

-- Create product table if it doesn't exist
CREATE TABLE IF NOT EXISTS product (
    id INT NOT NULL AUTO_INCREMENT,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    brand VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert example product (only if it doesn't already exist)
INSERT INTO product (sku, name, price, brand)
SELECT 'SKU123', 'Example Product', 19.99, 'Brand A'
WHERE NOT EXISTS (
    SELECT 1 FROM product WHERE sku = 'SKU123'
);