import React from "react";
import { useDecisionFlow } from "@/context/DecisionFlowContext";
import Stepper from "@/components/Stepper";
import StepIntroduction from "@/components/steps/StepIntroduction";
import StepEvidenceUpload from "@/components/steps/StepEvidenceUpload";
import StepProcessing from "@/components/steps/StepProcessing";
import StepAIInsight from "@/components/steps/StepAIInsight";
import StepExplainability from "@/components/steps/StepExplainability";
import StepHumanValidation from "@/components/steps/StepHumanValidation";
import StepFinalOutcome from "@/components/steps/StepFinalOutcome";
import StepDefenseSummary from "@/components/steps/StepDefenseSummary";

const STEPS: Record<number, React.FC> = {
  1: StepIntroduction,
  2: StepEvidenceUpload,
  3: StepProcessing,
  4: StepAIInsight,
  5: StepExplainability,
  6: StepHumanValidation,
  7: StepFinalOutcome,
  8: StepDefenseSummary,
};

const STEP_TITLES: Record<number, string> = {
  1: "Introduction",
  2: "Evidence Upload",
  3: "Processing Pipeline",
  4: "AI Recommendation",
  5: "Explainability Analysis",
  6: "Human Validation",
  7: "Decision Record",
  8: "Defense Summary",
};

const WizardLayout: React.FC = () => {
  const { currentStep } = useDecisionFlow();
  const StepComponent = STEPS[currentStep];

  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Top Bar */}
      <header className="border-b no-print">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-lg font-bold tracking-tight text-primary">NEXORA AI</h1>
          <span className="text-sm text-muted-foreground hidden sm:block">
            Explainable Decision Intelligence
          </span>
        </div>
      </header>

      {/* Stepper */}
      <nav className="border-b no-print">
        <div className="max-w-5xl mx-auto px-6">
          <Stepper />
        </div>
      </nav>

      {/* Step label */}
      <div className="border-b no-print">
        <div className="max-w-[800px] mx-auto px-6 py-2">
          <p className="text-xs text-muted-foreground uppercase tracking-wide font-medium">
            Step {currentStep} of 8 — {STEP_TITLES[currentStep]}
          </p>
        </div>
      </div>

      {/* Content */}
      <main className="flex-1 py-8">
        <div className="max-w-[800px] mx-auto px-6">
          <StepComponent />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t no-print">
        <div className="max-w-5xl mx-auto px-6 py-3">
          <p className="text-xs text-muted-foreground text-center">
            NEXORA AI — Academic Prototype for Explainable Decision Intelligence
          </p>
        </div>
      </footer>
    </div>
  );
};

export default WizardLayout;
