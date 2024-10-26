import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export function Button({ children, className = '', ...props }: ButtonProps) {
  return (
    <button
      className={`w-full bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}