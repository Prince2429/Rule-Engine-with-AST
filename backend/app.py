from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, Rule
from rule_engine import create_ast, combine_asts, evaluate_ast
import json

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

@app.route('/api/create-rule', methods=['POST'])
def create_rule():
    try:
        data = request.json
        rule_string = data.get('rule_string')
        
        if not rule_string:
            return jsonify({'message': 'Rule string is required'}), 400
        
        # Parse rule string into AST
        ast = create_ast(rule_string)
        
        # Save rule to database
        rule = Rule(rule_string=rule_string, ast=json.dumps(ast))
        rule.save()
        
        return jsonify({
            'message': f'Rule created successfully with ID: {rule.id}',
            'rule_id': rule.id
        }), 201
    except Exception as e:
        return jsonify({'message': f'Error creating rule: {str(e)}'}), 400

@app.route('/api/combine-rules', methods=['POST'])
def combine_rules():
    try:
        data = request.json
        rule_ids = data.get('rule_ids', [])
        
        if not rule_ids:
            return jsonify({'message': 'Rule IDs are required'}), 400
        
        # Get rules from database
        rules = Rule.get_multiple(rule_ids)
        if not rules:
            return jsonify({'message': 'No rules found'}), 404
        
        # Combine ASTs
        asts = [json.loads(rule.ast) for rule in rules]
        combined_ast = combine_asts(asts)
        
        combined_rule_name = f"Combined_rule-{'_'.join(map(str, rule_ids))}"
        # Save combined rule
        combined_rule = Rule(
            rule_string=combined_rule_name,
            ast=json.dumps(combined_ast)
        )
        combined_rule.save()
        
        return jsonify({
            'message': f'Rules combined successfully with ID: {combined_rule.id}',
            'rule_id': combined_rule.id
        }), 201
    except Exception as e:
        return jsonify({'message': f'Error combining rules: {str(e)}'}), 400

@app.route('/api/evaluate-rule', methods=['POST'])
def evaluate_rule():
    try:
        data = request.json
        rule_data = data.get('data', {})
        
        if not rule_data:
            return jsonify({'message': 'Evaluation data is required'}), 400
        
        # Get the latest rule from database
        rule = Rule.get_latest()
        if not rule:
            return jsonify({'message': 'No rules found'}), 404
        
        # Evaluate AST
        ast = json.loads(rule.ast)
        result = evaluate_ast(ast, rule_data)
        
        return jsonify({
            'message': 'Rule evaluated successfully',
            'result': result
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error evaluating rule: {str(e)}'}), 400

@app.route('/api/modify-rule', methods=['PUT'])
def modify_rule():
    try:
        data = request.json
        rule_id = data.get('rule_id')
        new_rule_string = data.get('new_rule_string')
        
        if not rule_id or not new_rule_string:
            return jsonify({'message': 'Rule ID and new rule string are required'}), 400
        
        # Parse new rule string into AST
        new_ast = create_ast(new_rule_string)
        
        # Update rule in database
        rule = Rule.get(rule_id)
        if not rule:
            return jsonify({'message': 'Rule not found'}), 404
        
        rule.update(rule_string=new_rule_string, ast=json.dumps(new_ast))
        
        return jsonify({'message': 'Rule modified successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error modifying rule: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)