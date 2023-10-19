CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

INSERT INTO employees (first_name, last_name, email) VALUES ('John', 'Doe', 'johndoe@example.com');
INSERT INTO employees (first_name, last_name, email) VALUES ('Jane', 'Smith', 'janesmith@example.com');
INSERT INTO employees (first_name, last_name, email) VALUES ('Bob', 'Johnson', 'bobjohnson@example.com');

SELECT * FROM employees;
