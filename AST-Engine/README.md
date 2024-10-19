# AST Engine Project

## What This Project Is About

The AST Engine project is a Flask-based web application designed to create, combine, and evaluate logical rules using an Abstract Syntax Tree (AST). The project features a simulated in-memory database to store rules and provides APIs for rule creation, combination, and evaluation. Users can define rules using string expressions, which are tokenized and parsed into an AST structure for processing.

## Explaining Structure of the Python Code

The main components of the Python code include:

- **Flask App Initialization**: The Flask framework is initialized to handle HTTP requests.
- **Node Class**: Represents each node in the AST, with properties for type (operator or operand), value, and child nodes.
- **Database**: A simulated in-memory database (dictionary) to store the defined rules.
- **Tokenization and Parsing**: Functions to tokenize rule strings and parse them into an AST.
- **Evaluation Logic**: A recursive function that evaluates the rules against provided data.
- **API Endpoints**: 
  - `/create_rule`: For creating a new rule from a string expression.
  - `/combine_rule`: For combining two existing rules with logical operators (AND/OR).
  - `/evaluate_rule`: For evaluating a rule against given data.

## What All Libraries or Software Needs to Be Installed to Run the Project

To run the project, ensure the following libraries and software are installed:

- **Python**: Version 3.x
- **Flask**: Install using pip:
  
  ```bash
  pip install Flask
- **Postman**: A tool for testing APIs.

## How to execute the project

1. Clone the project in your system.
2. Make sure all the required libraries, modules and software such as Python and Postman is installed.
3. Run the python file.
4. If your code runs successfully then your editor will give you the url on which the code is running. The default port is 5000 so your url would probably look like: `http://127.0.0.1:5000/{API_Endpoint}` where the API_Endpoint would be 'create_rule' for rule creation, 'combine_rule' for rule combination, and 'evaluate_rule' for rule evaluation.

5. For rule creation, use the POST method, and your URL would probably look like `http://127.0.0.1:5000/create_rule` with the request body as:

   ```json
   {
       "rule_name": "rule1",
       "rule_expression": "age > 18"
   }
   ```

   ```json
   {
       "rule_name": "rule1",
       "rule_expression": "(age > 18 AND salary > 20000)"
   }
   ```

   ```json
   {
       "rule_name": "rule1",
       "rule_expression": "((age > 21 AND salary > 30000) OR experience > 5)"
   }
   ```

   ```json
   {
       "rule_name": "rule1",
       "rule_expression": "((age > 21 AND salary > 30000) OR (experience > 5 AND rating > 4))"
   }
   ```


    ```json
   {
       "rule_name": "rule1",
       "rule_expression": "(((age > 21 AND salary > 30000) OR (experience > 5 AND rating > 4)) AND education == 'Bachelor')"
   }
    ```


    ```json
   {
       "rule_name": "rule1",
       "rule_expression": "(((age > 21 AND salary > 30000) OR (experience > 5 AND rating > 4)) AND (education == 'Bachelor' OR degree == 'Master'))"
   }
    ```


The response body would be the AST Node of the newly created rule (i.e, AST node of rule1 in this case).

**Note:** Please be very careful when placing parentheses while creating the rule expression. If there is no operator and only an operand, do not place parentheses. In simple words, parentheses will be used only if your rule expression has operator involved in between the two operands. Don't use parentheses if there is only one operand. Incorrect placement of parentheses won't be processed by the parse_tokens function correctly which will cause IndexError or ValueError. You can refer the above provided json code to create expressions easily.

6. For rule combination, use the POST method, and your URL would probably look like `http://127.0.0.1:5000/combine_rule` with the request body as:

   ```json
   {
       "rule_name1": "rule1",
       "rule_name2": "rule2",
       "operator": "AND", 
       "combined_rule_name": "rule3"
   }
   ```

if you want to perform AND operation between "rule1" and "rule2" and rename the newly combined rule as "rule3"

The response body would be the AST Node of the newly combined rule (i.e, AST node of rule3 in this case).

7. For rule evaluation, use the POST method and your URL would probably look like `http://127.0.0.1:5000/evaluate_rule` with the request body as:

   ```json
   {
       "rule_name": "rule3",
       "data": {
           "age": 35,
           "department": "Sales",
           "salary": 60000,
           "experience": 6
       }
   }
   ```

if you want to evaluate rule3 for the input data: data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 6}

The response body would be either "True" or "False" with the rule name which has been evaluated.

**Note:** We have not stored the created or combined rules in any database or permanent storage in order to reduce code complexity, as this was not required in the assignment anyways. Therefore, all rules are stored temporarily and will be lost once the program execution stops.

---
