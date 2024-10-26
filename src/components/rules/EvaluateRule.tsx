import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { TextArea } from '../ui/TextArea';
import { Button } from '../ui/Button';
import { Check, X } from 'lucide-react';

interface EvaluateRuleProps {
  onResult: (result: { success: boolean; message: string }) => void;
}

export function EvaluateRule({ onResult }: EvaluateRuleProps) {
  const [evaluationData, setEvaluationData] = useState('');
  const [evaluationResult, setEvaluationResult] = useState<{ result: boolean; visible: boolean } | null>(null);

  const handleEvaluateRule = async () => {
    if (!evaluationData.trim()) {
      onResult({ success: false, message: 'Evaluation data cannot be empty' });
      return;
    }

    try {
      JSON.parse(evaluationData); // Validate JSON
      const response = await fetch('http://localhost:5000/api/evaluate-rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: JSON.parse(evaluationData) }),
      });
      const data = await response.json();
      
      if (response.ok) {
        setEvaluationResult({ result: data.result, visible: true });
        setTimeout(() => setEvaluationResult(prev => prev ? { ...prev, visible: false } : null), 3000);
      }
      
      onResult({ success: response.ok, message: data.message });
    } catch (error) {
      onResult({ success: false, message: 'Invalid JSON data' });
    }
  };

  return (
    <Card title="Evaluate Rule">
      <div className="relative">
        <TextArea
          value={evaluationData}
          onChange={(e) => setEvaluationData(e.target.value)}
          placeholder='Enter JSON data (e.g., {"age": 35, "department": "Sales"})'
        />
        {evaluationResult?.visible && (
          <div className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
            ${evaluationResult.result ? 'bg-green-500' : 'bg-red-500'} 
            text-white rounded-full p-4 shadow-lg animate-fade-in`}>
            {evaluationResult.result ? (
              <Check className="h-8 w-8" />
            ) : (
              <X className="h-8 w-8" />
            )}
          </div>
        )}
      </div>
      <Button onClick={handleEvaluateRule}>Evaluate Rule</Button>
    </Card>
  );
}