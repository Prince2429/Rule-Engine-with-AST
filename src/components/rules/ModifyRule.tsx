import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { Input } from '../ui/Input';
import { TextArea } from '../ui/TextArea';
import { Button } from '../ui/Button';

interface ModifyRuleProps {
  onResult: (result: { success: boolean; message: string }) => void;
}

export function ModifyRule({ onResult }: ModifyRuleProps) {
  const [modifyRuleId, setModifyRuleId] = useState('');
  const [newRuleString, setNewRuleString] = useState('');

  const handleModifyRule = async () => {
    if (!modifyRuleId.trim() || !newRuleString.trim()) {
      onResult({ success: false, message: 'Rule ID and new rule string are required' });
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/modify-rule', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rule_id: modifyRuleId,
          new_rule_string: newRuleString,
        }),
      });
      const data = await response.json();
      onResult({ success: response.ok, message: data.message });
      if (response.ok) {
        setModifyRuleId('');
        setNewRuleString('');
      }
    } catch (error) {
      onResult({ success: false, message: 'Failed to modify rule' });
    }
  };

  return (
    <Card title="Modify Rule">
      <Input
        value={modifyRuleId}
        onChange={(e) => setModifyRuleId(e.target.value)}
        placeholder="Enter rule ID to modify"
      />
      <TextArea
        value={newRuleString}
        onChange={(e) => setNewRuleString(e.target.value)}
        placeholder="Enter new rule string"
      />
      <Button onClick={handleModifyRule}>Modify Rule</Button>
    </Card>
  );
}