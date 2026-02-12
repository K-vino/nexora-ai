import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const StepFinalOutcome = () => {
  const { decision, explanation, finalizedAt, decisionId, nextStep } = useDecisionFlow();

  const decisionLabel = decision === "approve" ? "Approved" : decision === "reject" ? "Rejected" : "Modified";

  const rows = [
    { label: "Human Decision", value: decisionLabel },
    {
      label: "AI Recommendation",
      value: "Approving the proposed infrastructure upgrade with phased implementation to mitigate risk exposure.",
    },
    ...(decision === "modify"
      ? [{ label: "Modification Notes", value: explanation || "—" }]
      : []),
    ...(decision === "reject"
      ? [{ label: "Rejection Justification", value: explanation || "—" }]
      : []),
    ...(decision === "approve"
      ? [{ label: "Human Reasoning", value: "Recommendation accepted without modification." }]
      : []),
    {
      label: "Timestamp",
      value: finalizedAt ? new Date(finalizedAt).toLocaleString() : "—",
    },
    { label: "Decision ID", value: decisionId },
  ];

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Decision Record</h1>
        <p className="text-sm text-muted-foreground leading-6">
          The following is the formal record of the finalized decision. This document
          serves as the auditable output of the decision-support process.
        </p>
      </div>

      <Card className="border-2">
        <CardContent className="p-6">
          <div className="border-b pb-3 mb-4">
            <p className="text-xs text-muted-foreground uppercase tracking-wide font-medium">
              NEXORA AI — Decision Record
            </p>
            <p className="text-xs text-muted-foreground">
              Reference: {decisionId}
            </p>
          </div>
          <table className="w-full">
            <tbody>
              {rows.map((row) => (
                <tr key={row.label} className="border-b last:border-b-0">
                  <td className="py-3 pr-4 text-sm font-semibold text-muted-foreground align-top w-1/3">
                    {row.label}
                  </td>
                  <td className="py-3 text-sm text-foreground leading-7">{row.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>

      <div className="flex justify-end pt-4">
        <Button onClick={nextStep}>View Defense Summary →</Button>
      </div>
    </div>
  );
};

export default StepFinalOutcome;
