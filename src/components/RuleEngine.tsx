import React, { useState } from 'react';
import { CreateRule } from './rules/CreateRule';
import { CombineRules } from './rules/CombineRules';
import { EvaluateRule } from './rules/EvaluateRule';
import { ModifyRule } from './rules/ModifyRule';
import { Notification } from './ui/Notification';

export function RuleEngine() {
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  return (
    <div className="space-y-8">
      {result && (
        <Notification
          success={result.success}
          message={result.message}
          onClose={() => setResult(null)}
        />
      )}
      <CreateRule onResult={setResult} />
      <CombineRules onResult={setResult} />
      <EvaluateRule onResult={setResult} />
      <ModifyRule onResult={setResult} />
    </div>
  );
}