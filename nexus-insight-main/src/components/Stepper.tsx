import React from "react";
import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Check } from "lucide-react";

const STEP_LABELS = [
  "Intro",
  "Upload",
  "Process",
  "Insight",
  "Explain",
  "Validate",
  "Outcome",
  "Defense",
];

const Stepper: React.FC = () => {
  const { currentStep, goToStep, finalized } = useDecisionFlow();

  return (
    <div className="flex items-center justify-between w-full max-w-3xl mx-auto py-4 px-2">
      {STEP_LABELS.map((label, i) => {
        const step = i + 1;
        const isCompleted = step < currentStep;
        const isCurrent = step === currentStep;
        const isFuture = step > currentStep;
        const canClick = isCompleted && !(finalized && step < 7);

        return (
          <React.Fragment key={step}>
            {i > 0 && (
              <div
                className={`flex-1 h-px mx-1 ${
                  isCompleted ? "bg-success" : "bg-border"
                }`}
              />
            )}
            <button
              onClick={() => canClick && goToStep(step)}
              disabled={!canClick}
              className={`flex flex-col items-center gap-1 group ${
                canClick ? "cursor-pointer" : "cursor-default"
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold border-2 transition-colors ${
                  isCompleted
                    ? "bg-success border-success text-success-foreground"
                    : isCurrent
                    ? "bg-primary border-primary text-primary-foreground"
                    : "bg-background border-muted-foreground/40 text-muted-foreground"
                }`}
              >
                {isCompleted ? <Check className="w-4 h-4" /> : step}
              </div>
              <span
                className={`text-[11px] leading-tight ${
                  isCurrent
                    ? "text-primary font-semibold"
                    : isCompleted
                    ? "text-success font-medium"
                    : "text-muted-foreground"
                }`}
              >
                {label}
              </span>
            </button>
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default Stepper;
