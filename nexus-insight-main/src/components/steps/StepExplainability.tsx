import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const EVIDENCE = [
  {
    source: "infrastructure_audit_2024.pdf",
    section: "Section 4.1",
    docRef: "Doc-1",
    text: "Current systems show a 23% decline in processing efficiency over the past 18 months, with projected failure rates increasing by 15% annually without intervention.",
    relevance: 92,
    linkedFactor: "Factor 1: Performance degradation urgency",
  },
  {
    source: "risk_assessment_report.docx",
    section: "Section 2.3",
    docRef: "Doc-2",
    text: "Phased implementation reduces transition risk by 40% compared to full cutover, with rollback capabilities maintained at each stage.",
    relevance: 87,
    linkedFactor: "Factor 2: Risk mitigation via phased approach",
  },
  {
    source: "compliance_requirements.pdf",
    section: "Section 1.1",
    docRef: "Doc-3",
    text: "Regulatory framework mandates infrastructure modernization completion by Q3 2025. Non-compliance penalties estimated at $2.4M annually.",
    relevance: 85,
    linkedFactor: "Factor 3: Regulatory compliance deadline",
  },
  {
    source: "stakeholder_survey_results.txt",
    section: "Summary",
    docRef: "Doc-4",
    text: "78% of surveyed stakeholders prefer a phased approach, citing operational continuity as primary concern.",
    relevance: 74,
    linkedFactor: "Factor 4: Stakeholder consensus alignment",
  },
];

const REASONING = [
  "Quantitative evidence of declining system performance (23% efficiency loss) establishes objective urgency for infrastructure intervention.",
  "Risk assessment data demonstrates that phased implementation reduces transition risk by 40%, supporting it as the methodologically safest approach.",
  "Regulatory compliance requirements impose a hard temporal constraint (Q3 2025), necessitating timely action.",
  "Stakeholder alignment with the phased methodology (78% preference) reduces organisational resistance and implementation friction.",
  "The convergence of quantitative performance data, risk modelling, regulatory constraints, and stakeholder consensus yields a moderate-high aggregate confidence score of 78%.",
];

const getRelevanceColor = (score: number) => {
  if (score >= 90) return "bg-success/15 text-success border-success/30";
  if (score >= 80) return "bg-primary/10 text-primary border-primary/30";
  return "bg-muted text-muted-foreground border-border";
};

const StepExplainability = () => {
  const { nextStep, prevStep, setHasViewedExplanation } = useDecisionFlow();

  const handleProceed = () => {
    setHasViewedExplanation(true);
    nextStep();
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Why This Recommendation?</h1>
        <p className="text-sm text-muted-foreground leading-6">
          Explainability analysis of the generated recommendation, including source attribution and reasoning chain.
        </p>
      </div>

      <div className="p-4 rounded-lg bg-secondary border border-border text-sm text-foreground leading-6">
        This recommendation is derived exclusively from the following retrieved evidence segments.
        Each segment includes its source attribution, relevance score, and linked influencing factor.
      </div>

      <div className="space-y-2">
        <h2 className="text-xl font-semibold text-foreground leading-tight">Retrieved Evidence</h2>
        <div className="space-y-4">
          {EVIDENCE.map((e, i) => (
            <Card key={i} className="border">
              <CardContent className="p-4 space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-0.5">
                    <span className="text-xs font-mono text-muted-foreground">
                      [{e.docRef}, {e.section}]
                    </span>
                    <p className="text-xs text-muted-foreground">{e.source}</p>
                  </div>
                  <Badge
                    variant="outline"
                    className={`text-xs shrink-0 ${getRelevanceColor(e.relevance)}`}
                  >
                    {e.relevance}% relevant
                  </Badge>
                </div>
                <blockquote className="border-l-4 border-primary/30 bg-secondary/50 pl-4 py-2 text-sm text-foreground italic leading-6">
                  "{e.text}"
                </blockquote>
                <p className="text-xs text-muted-foreground">
                  → {e.linkedFactor}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <h2 className="text-xl font-semibold text-foreground leading-tight">Reasoning Chain</h2>
        <p className="text-sm text-muted-foreground leading-6">
          The following chain illustrates how evidence segments were synthesised to produce the final recommendation.
        </p>
        <ol className="space-y-3 text-sm text-foreground">
          {REASONING.map((r, i) => (
            <li key={i} className="flex gap-3 leading-7">
              <span className="font-mono text-xs text-primary font-semibold mt-1 shrink-0">
                R{i + 1}.
              </span>
              <span>{r}</span>
            </li>
          ))}
        </ol>
      </div>

      <div className="flex justify-between pt-4">
        <Button variant="ghost" onClick={prevStep}>← Back</Button>
        <Button onClick={handleProceed}>Proceed to Validation →</Button>
      </div>
    </div>
  );
};

export default StepExplainability;
