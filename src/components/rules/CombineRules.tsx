import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

interface CombineRulesProps {
  onResult: (result: { success: boolean; message: string }) => void;
}

export function CombineRules({ onResult }: CombineRulesProps) {
  const [ruleIds, setRuleIds] = useState('');

  const handleCombineRules = async () => {
    if (!ruleIds.trim()) {
      onResult({ success: false, message: 'Rule IDs cannot be empty' });
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/combine-rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_ids: ruleIds.split(',').map(id => id.trim()) }),
      });
      const data = await response.json();
      onResult({ success: response.ok, message: data.message });
      if (response.ok) setRuleIds('');
    } catch (error) {
      onResult({ success: false, message: 'Failed to combine rules' });
    }
  };

  return (
    <Card title="Combine Rules">
      <Input
        value={ruleIds}
        onChange={(e) => setRuleIds(e.target.value)}
        placeholder="Enter rule IDs (comma-separated)"
      />
      <Button onClick={handleCombineRules}>Combine Rules</Button>
    </Card>
  );
}