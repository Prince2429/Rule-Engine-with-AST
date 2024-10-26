import React from 'react';

interface CardProps {
  title: string;
  children: React.ReactNode;
}

export function Card({ title, children }: CardProps) {
  return (
    <div className="bg-white rounded-lg shadow-xl p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
      <div className="space-y-4">
        {children}
      </div>
    </div>
  );
}