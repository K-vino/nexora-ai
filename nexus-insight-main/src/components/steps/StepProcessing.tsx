import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Check } from "lucide-react";
import { useEffect, useState, useRef } from "react";

const STAGES = [
  "Chunking Evidence",
  "Generating Embeddings",
  "Retrieving Relevant Context",
  "Constructing Structured Prompt",
  "Generating Explainable Recommendation",
];

const StepProcessing = () => {
  const { nextStep, prevStep, setProcessingComplete } = useDecisionFlow();
  const [activeStage, setActiveStage] = useState(0);
  const [stageProgress, setStageProgress] = useState(0);
  const [cancelled, setCancelled] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (cancelled) return;

    if (activeStage >= STAGES.length) {
      setProcessingComplete(true);
      const timeout = setTimeout(() => nextStep(), 600);
      return () => clearTimeout(timeout);
    }

    setStageProgress(0);
    intervalRef.current = setInterval(() => {
      setStageProgress((p) => {
        if (p >= 100) {
          if (intervalRef.current) clearInterval(intervalRef.current);
          setTimeout(() => setActiveStage((s) => s + 1), 200);
          return 100;
        }
        return p + 5;
      });
    }, 60);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [activeStage, cancelled, nextStep, setProcessingComplete]);

  const handleCancel = () => {
    setCancelled(true);
    if (intervalRef.current) clearInterval(intervalRef.current);
  };

  const handleRetry = () => {
    setCancelled(false);
    setActiveStage(0);
    setStageProgress(0);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Analyzing Evidence</h1>
        <p className="text-sm text-muted-foreground leading-6">
          The system is processing uploaded documents through the RAG pipeline.
          Each stage is executed sequentially.
        </p>
      </div>

      <div className="space-y-4">
        {STAGES.map((stage, i) => {
          const isComplete = i < activeStage;
          const isActive = i === activeStage && !cancelled;

          return (
            <div key={stage} className="space-y-2">
              <div className="flex items-center gap-3">
                <div
                  className={`w-6 h-6 rounded flex items-center justify-center text-xs font-medium border transition-colors ${
                    isComplete
                      ? "bg-success border-success text-success-foreground"
                      : isActive
                      ? "border-primary text-primary"
                      : "border-muted-foreground/30 text-muted-foreground"
                  }`}
                >
                  {isComplete ? <Check className="w-4 h-4" /> : i + 1}
                </div>
                <span className={`text-sm leading-7 ${isActive ? "font-semibold text-foreground" : isComplete ? "text-foreground" : "text-muted-foreground"}`}>
                  {stage}
                </span>
                <span className={`text-xs ml-auto ${isComplete ? "text-success" : isActive ? "text-primary" : "text-muted-foreground"}`}>
                  {isComplete ? "Complete" : isActive ? "Processing..." : cancelled && i === activeStage ? "Interrupted" : "Pending"}
                </span>
              </div>
              {isActive && <Progress value={stageProgress} className="h-2 ml-9" />}
            </div>
          );
        })}
      </div>

      <p className="text-xs text-muted-foreground italic pt-2 leading-6">
        Note: Processing is simulated for demonstration purposes. In a production implementation,
        each stage would interface with the respective NLP and vector database components.
      </p>

      {!cancelled && activeStage < STAGES.length && (
        <div className="flex justify-start pt-2">
          <Button variant="ghost" size="sm" onClick={handleCancel}>
            Cancel Processing
          </Button>
        </div>
      )}

      {cancelled && (
        <div className="flex gap-3 pt-2">
          <Button variant="ghost" onClick={prevStep}>← Back</Button>
          <Button onClick={handleRetry}>Retry Processing</Button>
        </div>
      )}
    </div>
  );
};

export default StepProcessing;
