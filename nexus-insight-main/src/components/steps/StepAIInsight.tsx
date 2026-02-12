import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const StepAIInsight = () => {
  const { nextStep, prevStep } = useDecisionFlow();

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Structured AI Recommendation</h1>
        <p className="text-sm text-muted-foreground leading-6">
          The following recommendation was generated through analysis of the uploaded evidence corpus.
        </p>
      </div>

      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">Recommendation</CardTitle></CardHeader>
        <CardContent>
          <p className="text-foreground leading-7">
            Based on the analyzed evidence, the system recommends <strong>approving the proposed infrastructure upgrade</strong> with
            an emphasis on phased implementation to mitigate risk exposure.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">Influencing Factors</CardTitle></CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-2 text-sm text-foreground leading-7">
            <li>Historical performance data indicates a 23% efficiency improvement with comparable upgrades</li>
            <li>Risk assessment documentation highlights manageable transition costs within budget thresholds</li>
            <li>Regulatory compliance requirements mandate infrastructure modernization by Q3 2025</li>
            <li>Stakeholder consultation results support a phased rollout methodology</li>
            <li>Budget allocation analysis confirms alignment with projected implementation expenditure</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">Confidence Assessment</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-foreground leading-7">
            The recommendation carries a <strong>moderate-high confidence level (78%)</strong>, derived from
            the consistency, recency, and mutual corroboration of retrieved evidence segments.
          </p>
          <div className="space-y-1">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Aggregate Confidence Score</span>
              <span>78 / 100</span>
            </div>
            <Progress value={78} className="h-2" />
          </div>
          <p className="text-xs text-muted-foreground leading-5">
            Confidence is computed as the weighted average of individual evidence relevance scores.
            Values above 70% indicate strong corroboration across multiple sources.
            Values below 50% would suggest insufficient or contradictory evidence.
          </p>
        </CardContent>
      </Card>

      <p className="text-sm text-muted-foreground italic leading-6">
        This is an AI-generated recommendation produced by the RAG pipeline.
        It requires mandatory human validation before finalization.
      </p>

      <div className="flex justify-between pt-4">
        <Button variant="ghost" onClick={prevStep}>← Back</Button>
        <Button onClick={nextStep}>View Explanation →</Button>
      </div>
    </div>
  );
};

export default StepAIInsight;
