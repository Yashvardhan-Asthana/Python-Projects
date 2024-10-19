import re
from flask import Flask, request, jsonify

app = Flask(__name__)  

# Simulated in-memory database to store the rules
database = {}

# Node structure for rules
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):  # Corrected
        self.type = node_type  # "operator" or "operand"
        self.value = value      # For "operand" nodes (conditions)
        self.left = left        # Left child (for "operator" nodes)
        self.right = right      # Right child (for "operator" nodes)

    def to_dict(self):
        # Convert the Node to a dictionary to return in the response
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

# Helper to evaluate a rule based on data
def evaluate(node, data):
    if node.type == "operand":
        # Evaluate the operand node (e.g., "age > 18")
        # Ensure the expression is in the correct Python format
        return eval(node.value, {"__builtins__": None}, data)
    elif node.type == "operator":
        if node.value == "AND":
            return evaluate(node.left, data) and evaluate(node.right, data)
        elif node.value == "OR":
            return evaluate(node.left, data) or evaluate(node.right, data)
    return False

# Tokenizer
def tokenize_rule(rule_str):
    # Tokenizer to extract tokens for the expression
    token_pattern = re.compile(r"\(|\)|\band\b|\bor\b|>|<|=|!=|[a-zA-Z_]+|'[^']*'|\d+")
    tokens = token_pattern.findall(rule_str)
    return [token.upper() if token.lower() in ['and', 'or'] else token for token in tokens]

# Recursive parser to build AST
def parse_tokens(tokens):
    def parse_expression(index):
        if tokens[index] == '(':
            left_node, index = parse_expression(index + 1)
            operator = tokens[index]
            right_node, index = parse_expression(index + 1)
            assert tokens[index] == ')', "Mismatched parentheses"
            return Node(node_type="operator", value=operator, left=left_node, right=right_node), index + 1
        else:
            # This is an operand node (e.g., age > 30)
            expr = []
            while index < len(tokens) and tokens[index] not in [')', 'AND', 'OR']:
                expr.append(tokens[index])
                index += 1
            operand_str = ' '.join(expr).replace('=', '==')  # Ensure '=' becomes '=='
            return Node(node_type="operand", value=operand_str), index
    
    root_node, _ = parse_expression(0)
    return root_node

# API to create a rule from a string expression
@app.route('/create_rule', methods=['POST'])
def create_rule():
    data = request.json
    rule_name = data['rule_name']
    rule_expression = data['rule_expression']

    # Tokenize and parse the rule expression into an AST
    tokens = tokenize_rule(rule_expression)
    ast_root = parse_tokens(tokens)

    # Store the rule in the database
    database[rule_name] = ast_root

    return jsonify({
        "message": f"Rule {rule_name} is created",
        "node": ast_root.to_dict()
    })

# API to combine two rules
@app.route('/combine_rule', methods=['POST'])
def combine_rule():
    data = request.json
    rule_name1 = data['rule_name1']
    rule_name2 = data['rule_name2']
    operator = data['operator']  # AND / OR
    combined_rule_name = data['combined_rule_name']

    # Check if both rules exist
    if rule_name1 not in database or rule_name2 not in database:
        return jsonify({"error": "One or both rules do not exist"}), 400

    # Fetch the two rules
    rule1 = database[rule_name1]
    rule2 = database[rule_name2]

    # Combine the rules with the operator
    combined_rule = Node(node_type="operator", value=operator, left=rule1, right=rule2)

    # Check if the combined rule already exists
    if combined_rule_name in database:
        return jsonify({
            "message": f"Combined rule {rule_name1} and {rule_name2} already exists as {combined_rule_name}",
            "node": database[combined_rule_name].to_dict()
        })

    # Store the combined rule
    database[combined_rule_name] = combined_rule

    return jsonify({
        "message": f"Combined {rule_name1} and {rule_name2} as {combined_rule_name}",
        "node": combined_rule.to_dict()
    })

# Example evaluate rule API
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    request_data = request.json
    rule_name = request_data.get('rule_name')
    data = request_data.get('data')

    # Fetch the rule from the database
    rule = database.get(rule_name)
    if not rule:
        return jsonify({"error": f"Rule {rule_name} not found"}), 404

    # Evaluate the rule AST recursively based on the provided data
    result = evaluate(rule, data)

    return jsonify({"result": result, "message": f"Evaluated rule {rule_name}"}), 200

if __name__ == '__main__':  
    app.run(debug=True)
