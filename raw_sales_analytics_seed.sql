-- Raw MySQL seed data for pipeline_mysql_dump.py
-- Import this file into MySQL, then run:
--   python pipeline_mysql_dump.py
--
-- Source database/table expected by .env:
--   MYSQL_DATABASE=sales_analytics
--   MYSQL_TABLE=customers
--
-- The rows intentionally include duplicates, invalid dates, nulls,
-- zero/negative values, and numeric strings so transform.py has
-- realistic cleanup work to do.

DROP DATABASE IF EXISTS `sales_analytics`;
CREATE DATABASE `sales_analytics`;
USE `sales_analytics`;

DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
    `ID` INT NULL,
    `Order Date` VARCHAR(40) NULL,
    `Customer ID` VARCHAR(20) NULL,
    `Customer Name` VARCHAR(100) NULL,
    `Product-Category` VARCHAR(60) NULL,
    `Product Name` VARCHAR(100) NULL,
    `Quantity` VARCHAR(20) NULL,
    `Unit Price` VARCHAR(20) NULL,
    `Amount` VARCHAR(20) NULL,
    `Created At` VARCHAR(40) NULL,
    `Region` VARCHAR(40) NULL,
    `Payment Method` VARCHAR(40) NULL
);

INSERT INTO `customers`
    (
        `ID`,
        `Order Date`,
        `Customer ID`,
        `Customer Name`,
        `Product-Category`,
        `Product Name`,
        `Quantity`,
        `Unit Price`,
        `Amount`,
        `Created At`,
        `Region`,
        `Payment Method`
    )
VALUES
    -- Kept: valid row. total_amount becomes 1499.98.
    (1, '2026-05-01', 'CUST-001', 'Aarav Sharma', 'Electronics', 'Wireless Mouse', '2', '749.99', '1499.98', '2026-05-01 10:15:00', 'North', 'UPI'),

    -- Kept: valid row. total_amount becomes 2599.00.
    (2, '2026-05-03', 'CUST-002', 'Meera Iyer', 'Home Office', 'Desk Lamp', '1', '2599.00', '2599.00', '2026-05-03 12:35:00', 'South', 'Card'),

    -- Kept: valid row. total_amount becomes 5697.00.
    (3, '2026-05-06', 'CUST-003', 'Rohan Patel', 'Electronics', 'Bluetooth Speaker', '3', '1899.00', '5697.00', '2026-05-06 09:20:00', 'West', 'Net Banking'),

    -- Dropped by duplicate id logic: duplicate ID 3 appears after the first ID 3 row.
    (3, '2026-05-07', 'CUST-003', 'Rohan Patel', 'Electronics', 'Bluetooth Speaker', '4', '1899.00', '7596.00', '2026-05-07 09:20:00', 'West', 'Net Banking'),

    -- Dropped: missing critical field customer_id.
    (4, '2026-05-08', NULL, 'Nisha Verma', 'Kitchen', 'Air Fryer', '1', '6499.00', '6499.00', '2026-05-08 14:05:00', 'East', 'UPI'),

    -- Dropped: invalid order_date is coerced to null.
    (5, 'not-a-date', 'CUST-005', 'Kabir Khan', 'Sports', 'Yoga Mat', '2', '899.50', '1799.00', '2026-05-09 08:45:00', 'North', 'Cash'),

    -- Dropped: quantity must be greater than zero.
    (6, '2026-05-10', 'CUST-006', 'Ananya Rao', 'Books', 'Python ETL Handbook', '0', '1299.00', '0.00', '2026-05-10 16:10:00', 'South', 'Card'),

    -- Dropped: amount must be non-negative.
    (7, '2026-05-11', 'CUST-007', 'Dev Singh', 'Apparel', 'Running Shoes', '1', '3499.00', '-3499.00', '2026-05-11 18:30:00', 'West', 'UPI'),

    -- Kept: quantity and price are numeric strings; transform.py converts them.
    (8, '2026-05-12', 'CUST-008', 'Sara Thomas', 'Kitchen', 'Coffee Grinder', '5', '1199.40', '5997.00', '2026-05-12 07:55:00', 'East', 'Wallet'),

    -- Kept: amount is valid, but total_amount is recalculated from quantity * unit_price.
    (9, '2026-05-13', 'CUST-009', 'Vikram Das', 'Home Office', 'Notebook Pack', '10', '149.99', '1500.00', '2026-05-13 11:25:00', 'North', 'UPI'),

    -- Dropped: null id is a critical field.
    (NULL, '2026-05-14', 'CUST-010', 'Priya Menon', 'Electronics', 'USB-C Cable', '2', '399.00', '798.00', '2026-05-14 13:40:00', 'South', 'Card'),

    -- Kept: extra whitespace in names/categories remains available for downstream analysis.
    (10, '2026-05-15', 'CUST-011', '  Ishan Gupta  ', '  Accessories  ', 'Laptop Stand', '1', '2199.00', '2199.00', '2026-05-15 17:05:00', 'West', 'Net Banking');
