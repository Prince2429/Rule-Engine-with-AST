import re
from typing import Dict, List, Union, Any

class Node:
    def __init__(self, type: str, value: Any = None, left: 'Node' = None, right: 'Node' = None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

def create_ast(rule_string: str) -> Dict:
    """Parse rule string and create AST"""
    tokens = tokenize(rule_string)
    ast = parse(tokens)
    return ast.to_dict()

def tokenize(rule_string: str) -> List[str]:
    """Convert rule string into tokens"""
    # Add spaces around operators and parentheses
    rule_string = re.sub(r'([()><=!&|])', r' \1 ', rule_string)
    # Handle AND/OR keywords
    rule_string = rule_string.replace(' AND ', ' && ').replace(' OR ', ' || ')
    return [token for token in rule_string.split() if token.strip()]

def parse(tokens: List[str]) -> Node:
    """Parse tokens into AST"""
    def parse_expression(tokens: List[str], precedence: int = 0) -> Node:
        if not tokens:
            raise ValueError("Empty expression")

        left = parse_term(tokens)

        while tokens and is_operator(tokens[0]):
            op = tokens.pop(0)
            op_precedence = get_operator_precedence(op)
            
            if op_precedence < precedence:
                tokens.insert(0, op)
                return left

            right = parse_expression(tokens, op_precedence)
            left = Node('operator', op, left, right)

        return left

    def parse_term(tokens: List[str]) -> Node:
        token = tokens.pop(0)

        if token == '(':
            expr = parse_expression(tokens)
            if not tokens or tokens.pop(0) != ')':
                raise ValueError("Missing closing parenthesis")
            return expr

        if is_value(token):
            return Node('operand', token)

        raise ValueError(f"Unexpected token: {token}")

    return parse_expression(tokens)

def is_operator(token: str) -> bool:
    """Check if token is an operator"""
    return token in ['&&', '||', '>', '<', '>=', '<=', '==', '!=']

def get_operator_precedence(op: str) -> int:
    """Get operator precedence"""
    precedences = {
        '&&': 1,
        '||': 1,
        '>': 2,
        '<': 2,
        '>=': 2,
        '<=': 2,
        '==': 2,
        '!=': 2
    }
    return precedences.get(op, 0)

def is_value(token: str) -> bool:
    """Check if token is a value"""
    return bool(re.match(r'^[a-zA-Z0-9_\'".]+$', token))

def combine_asts(asts: List[Dict]) -> Dict:
    """Combine multiple ASTs into a single AST"""
    if not asts:
        raise ValueError("No ASTs to combine")
    if len(asts) == 1:
        return asts[0]

    # Combine ASTs with AND operator
    combined = asts[0]
    for ast in asts[1:]:
        combined = {
            'type': 'operator',
            'value': '&&',
            'left': combined,
            'right': ast
        }
    return combined

def evaluate_ast(ast: Dict, data: Dict) -> bool:
    """Evaluate AST with given data"""
    def evaluate_node(node: Dict) -> Any:
        if not node:
            return True

        if node['type'] == 'operand':
            # Handle attribute references and literals
            value = node['value']
            if value.startswith('"') or value.startswith("'"):
                return value.strip('"\'')
            if value.isdigit():
                return int(value)
            return data.get(value)

        if node['type'] == 'operator':
            left = evaluate_node(node['left'])
            right = evaluate_node(node['right'])
            
            op = node['value']
            if op == '&&':
                return left and right
            if op == '||':
                return left or right
            if op == '>':
                return left > right
            if op == '<':
                return left < right
            if op == '>=':
                return left >= right
            if op == '<=':
                return left <= right
            if op == '==':
                return left == right
            if op == '!=':
                return left != right

        raise ValueError(f"Invalid node type: {node['type']}")

    return evaluate_node(ast)