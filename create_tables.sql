CREATE TABLE IF NOT EXISTS categories (
    categoryid INTEGER PRIMARY KEY,
    categoryname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS regions (
    regionid INTEGER PRIMARY KEY,
    regionname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payment_methods (
    methodid INTEGER PRIMARY KEY,
    methodname TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    productid INTEGER PRIMARY KEY,
    productname TEXT NOT NULL,
    unitprice FLOAT NOT NULL,
    category INTEGER,
    FOREIGN KEY (category) REFERENCES categories (categoryid)
);

CREATE TABLE IF NOT EXISTS customers (
    customerid INTEGER PRIMARY KEY,
    customername TEXT NOT NULL,
    customeremail TEXT NOT NULL,
    customeraddress TEXT NOT NULL,
    customerregion INTEGER,
    FOREIGN KEY (customerregion) REFERENCES regions (regionid)
);

CREATE TABLE IF NOT EXISTS orders (
    orderid INTEGER PRIMARY KEY,
    productid INTEGER NOT NULL,
    customerid INTEGER NOT NULL,
    orderdate DATE NOT NULL,
    quantitysold INTEGER NOT NULL,
    discount FLOAT DEFAULT 0,
    shipping FLOAT DEFAULT 0,
    paymentmethod INTEGER,
    FOREIGN KEY (productid) REFERENCES products (productid),
    FOREIGN KEY (customerid) REFERENCES customers (customerid),
    FOREIGN KEY (paymentmethod) REFERENCES payment_methods (methodid)
);