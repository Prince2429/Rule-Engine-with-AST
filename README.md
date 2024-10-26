# Rule Engine with AST

A modern rule engine application that uses Abstract Syntax Trees (AST) to represent and evaluate conditional rules. The system allows for dynamic creation, combination, and modification of rules based on user attributes.

## Features

- Create rules using a simple string syntax
- Combine multiple rules into a single rule
- Evaluate rules against user data
- Modify existing rules
- Visual representation of rules
- Error handling and validation
- Support for complex logical operations

## Tech Stack

### Frontend
- React
- TypeScript
- Tailwind CSS
- Lucide Icons

### Backend
- Flask
- MySQL
### Backend Setup

1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the MySQL database:
   - Create a database named `rule_engine`
   - Create the following tables:
     ```sql
     create database rule_engine;
     USE rule_engine;

     CREATE TABLE IF NOT EXISTS rules (
     id INT AUTO_INCREMENT PRIMARY KEY,
     rule_string TEXT NOT NULL,
     ast TEXT NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
     );

     select * from rules;

     DELETE FROM rules WHERE rule_string = 'Combined Rule';
     for more refer mysqldatabase.db file in backend folder 
     ```

5. Start the Flask server:
   ```
   python app.py
   ```

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install --force
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Rule Syntax

Rules should be written in the following format:
```
age > 30 AND department = 'Sales' OR (age < 25 AND department = 'Marketing') AND (salary > 50000 OR experience > 5)
```

## API Endpoints

- POST /api/rules/create - Create a new rule
- POST /api/rules/combine - Combine multiple rules
- POST /api/rules/evaluate - Evaluate a rule against data
- PUT /api/rules/:id - Modify an existing rule

## Application Images
![image](https://github.com/user-attachments/assets/b47515b3-61f2-4cba-96c3-9e76323b93ef)
![image](https://github.com/user-attachments/assets/77360dc2-13a1-43c7-b797-4f61649e0086)


