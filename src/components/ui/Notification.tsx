import React from 'react';
import { AlertCircle, Check, X } from 'lucide-react';

interface NotificationProps {
  success: boolean;
  message: string;
  onClose: () => void;
}

export function Notification({ success, message, onClose }: NotificationProps) {
  return (
    <div className={`p-4 rounded-lg ${success ? 'bg-green-100' : 'bg-red-100'} flex items-center`}>
      {success ? (
        <Check className="h-5 w-5 text-green-500 mr-2" />
      ) : (
        <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
      )}
      <span className={success ? 'text-green-700' : 'text-red-700'}>{message}</span>
      <button
        onClick={onClose}
        className="ml-auto text-gray-500 hover:text-gray-700"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}