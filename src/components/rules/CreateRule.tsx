import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { TextArea } from '../ui/TextArea';
import { Button } from '../ui/Button';

interface CreateRuleProps {
  onResult: (result: { success: boolean; message: string }) => void;
}

export function CreateRule({ onResult }: CreateRuleProps) {
  const [ruleString, setRuleString] = useState('');

  const handleCreateRule = async () => {
    if (!ruleString.trim()) {
      onResult({ success: false, message: 'Rule string cannot be empty' });
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/create-rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_string: ruleString }),
      });
      const data = await response.json();
      onResult({ success: response.ok, message: data.message });
      if (response.ok) setRuleString('');
    } catch (error) {
      onResult({ success: false, message: 'Failed to create rule' });
    }
  };

  return (
    <Card title="Create Rule">
      <TextArea
        value={ruleString}
        onChange={(e) => setRuleString(e.target.value)}
        placeholder="Enter rule string (e.g., age > 30 AND department = 'Sales')"
      />
      <Button onClick={handleCreateRule}>Create Rule</Button>
    </Card>
  );
}