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
