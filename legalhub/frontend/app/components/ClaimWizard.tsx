"use client";

import React from "react";

interface WizardProps {
  steps: React.ReactNode[];
}

export function ClaimWizard({ steps }: WizardProps) {
  const [stepIndex, setStepIndex] = React.useState(0);

  const isFirst = stepIndex === 0;
  const isLast = stepIndex === steps.length - 1;

  const next = () => {
    if (!isLast) setStepIndex((i) => i + 1);
  };

  const prev = () => {
    if (!isFirst) setStepIndex((i) => i - 1);
  };

  return (
    <div className="space-y-4">
      <div className="text-sm text-slate-600">
        Step {stepIndex + 1} of {steps.length}
      </div>
      <div className="border rounded-lg p-4 bg-white">
        {steps[stepIndex]}
      </div>
      <div className="flex justify-between pt-2">
        <button
          type="button"
          onClick={prev}
          disabled={isFirst}
          className="px-4 py-2 border rounded disabled:opacity-50"
        >
          Back
        </button>
        <button
          type="button"
          onClick={next}
          className="px-4 py-2 bg-slate-900 text-white rounded"
        >
          {isLast ? "Review" : "Next"}
        </button>
      </div>
    </div>
  );
}
