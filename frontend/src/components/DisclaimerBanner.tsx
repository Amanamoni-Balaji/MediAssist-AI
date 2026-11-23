import React, { useState } from 'react';
import { AlertTriangle, X } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 text-xs text-amber-900 flex items-center justify-between shadow-xs">
      <div className="flex items-center gap-2 max-w-6xl mx-auto flex-1">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
        <p>
          <strong className="font-semibold">Educational Healthcare Assistant:</strong> This AI system is strictly for informational and educational awareness. It does NOT provide medical diagnosis, treatment, or prescriptions. For medical emergencies, immediately dial <strong>911 / 999 / 112</strong>.
        </p>
      </div>
      <button
        onClick={() => setDismissed(true)}
        className="text-amber-700 hover:text-amber-950 p-1 rounded-md transition-colors"
        title="Dismiss notice"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  );
};

