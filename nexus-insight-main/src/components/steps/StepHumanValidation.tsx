import { useDecisionFlow, ValidationDecision } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { AlertTriangle, CheckCircle, XCircle, Pencil, ShieldAlert } from "lucide-react";
import { useState } from "react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

const OPTIONS: { value: ValidationDecision; icon: React.FC<{ className?: string }>; label: string; description: string }[] = [
  { value: "approve", icon: CheckCircle, label: "Approve", description: "Accept the AI recommendation as presented" },
  { value: "reject", icon: XCircle, label: "Reject", description: "Decline the recommendation in its entirety" },
  { value: "modify", icon: Pencil, label: "Modify", description: "Accept the recommendation with amendments" },
];

const StepHumanValidation = () => {
  const {
    decision, setDecision, explanation, setExplanation,
    acknowledged, setAcknowledged,
    hasViewedExplanation,
    finalize, nextStep, prevStep,
  } = useDecisionFlow();
  const [errors, setErrors] = useState<string[]>([]);
  const [showConfirm, setShowConfirm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const needsExplanation = decision === "reject" || decision === "modify";

  const validate = (): string[] => {
    const errs: string[] = [];
    if (!decision) errs.push("A decision selection is required before finalization.");
    if (needsExplanation && explanation.trim().length < 20) {
      errs.push("A written justification of at least 20 characters is required for rejection or modification.");
    }
    if (!acknowledged) {
      errs.push("You must acknowledge decision accountability before proceeding.");
    }
    if (!hasViewedExplanation && decision === "approve") {
      errs.push("Please review the Explainability page (Step 5) before approving the recommendation.");
    }
    return errs;
  };

  const handleFinalize = () => {
    const errs = validate();
    if (errs.length > 0) {
      setErrors(errs);
      return;
    }
    setErrors([]);
    setShowConfirm(true);
  };

  const confirmFinalize = () => {
    setIsSubmitting(true);
    setShowConfirm(false);
    finalize();
    nextStep();
  };

  const canFinalize = !!decision && acknowledged && (!needsExplanation || explanation.trim().length >= 20);

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Human Decision Required</h1>
        <p className="text-sm text-muted-foreground leading-6">
          The AI-generated recommendation requires explicit human validation.
          Select your decision and provide justification where applicable.
        </p>
      </div>

      <div className="flex items-start gap-3 p-4 rounded-lg bg-secondary border border-primary/20">
        <AlertTriangle className="w-5 h-5 text-primary mt-0.5 shrink-0" />
        <p className="text-sm text-foreground leading-6">
          <strong>Mandatory Validation:</strong> The AI system cannot finalize decisions autonomously.
          Human review and explicit validation is required for all recommendations.
        </p>
      </div>

      <Card>
        <CardContent className="p-4">
          <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wide font-medium">AI Recommendation Summary</p>
          <p className="text-sm text-foreground leading-7">
            Approving the proposed infrastructure upgrade with phased implementation to mitigate risk exposure.
          </p>
        </CardContent>
      </Card>

      <div className="space-y-3">
        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Select Decision</p>
        {OPTIONS.map((opt) => (
          <button
            key={opt.value}
            onClick={() => { setDecision(opt.value); setErrors([]); }}
            className={`w-full text-left p-4 rounded-lg border-2 transition-colors ${
              decision === opt.value
                ? "border-primary bg-secondary"
                : "border-border hover:border-muted-foreground/40"
            }`}
          >
            <div className="flex items-center gap-3">
              <opt.icon className={`w-5 h-5 ${decision === opt.value ? "text-primary" : "text-muted-foreground"}`} />
              <div>
                <p className="font-medium text-sm text-foreground">{opt.label}</p>
                <p className="text-xs text-muted-foreground leading-5">{opt.description}</p>
              </div>
            </div>
          </button>
        ))}
      </div>

      {needsExplanation && (
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">
            {decision === "reject" ? "Justification for Rejection" : "Description of Modifications"}
          </label>
          <Textarea
            value={explanation}
            onChange={(e) => { setExplanation(e.target.value); setErrors([]); }}
            placeholder="Provide a detailed explanation (minimum 20 characters)..."
            className="min-h-[100px]"
          />
          <p className="text-xs text-muted-foreground">
            {explanation.length} / 20 characters minimum
            {explanation.length >= 20 && " ✓"}
          </p>
        </div>
      )}

      {/* Accountability acknowledgment */}
      <div className="flex items-start gap-3 p-4 rounded-lg border bg-secondary/50">
        <ShieldAlert className="w-5 h-5 text-primary mt-0.5 shrink-0" />
        <div className="space-y-3">
          <p className="text-sm text-foreground leading-6">
            <strong>Decision Accountability:</strong> By finalizing this decision, you acknowledge
            that the outcome is your responsibility. The AI system serves as a decision-support
            tool and bears no liability for the final determination.
          </p>
          <div className="flex items-center gap-2">
            <Checkbox
              id="acknowledge"
              checked={acknowledged}
              onCheckedChange={(v) => { setAcknowledged(!!v); setErrors([]); }}
            />
            <label htmlFor="acknowledge" className="text-sm text-foreground cursor-pointer leading-5">
              I understand that I am responsible for this decision.
            </label>
          </div>
        </div>
      </div>

      {errors.length > 0 && (
        <div className="space-y-1 p-3 rounded-lg border border-destructive/30 bg-destructive/5">
          {errors.map((e, i) => (
            <p key={i} className="text-sm text-destructive leading-6">{e}</p>
          ))}
        </div>
      )}

      <div className="flex justify-between pt-4">
        <Button variant="ghost" onClick={prevStep}>← Back</Button>
        <Button onClick={handleFinalize} disabled={!canFinalize || isSubmitting}>
          Finalize Decision
        </Button>
      </div>

      {/* Confirmation dialog */}
      <AlertDialog open={showConfirm} onOpenChange={setShowConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirm Decision Finalization</AlertDialogTitle>
            <AlertDialogDescription className="space-y-2">
              <span className="block">
                You are about to finalize your decision as: <strong className="text-foreground">
                {decision === "approve" ? "Approved" : decision === "reject" ? "Rejected" : "Modified"}
                </strong>
              </span>
              <span className="block">
                This action is irreversible. After finalization, you will not be able to return
                to previous steps or modify your decision.
              </span>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={confirmFinalize}>
              Confirm Finalization
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default StepHumanValidation;
