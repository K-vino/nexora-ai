import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Search, Users, ClipboardList } from "lucide-react";

const StepIntroduction = () => {
  const { nextStep } = useDecisionFlow();

  const principles = [
    {
      icon: Search,
      title: "Explainability First",
      description: "The system prioritises transparency — presenting reasoning and evidence before any recommendation.",
    },
    {
      icon: Users,
      title: "Human-in-the-Loop",
      description: "Every AI-generated recommendation requires explicit human review and validation before finalization.",
    },
    {
      icon: ClipboardList,
      title: "Decision Support Only",
      description: "The system serves as an advisory tool — it recommends, but never autonomously decides.",
    },
  ];

  return (
    <div className="space-y-8">
      <div className="space-y-4">
        <h1 className="text-[28px] font-semibold text-primary leading-tight">NEXORA AI</h1>
        <p className="text-base text-foreground leading-7 max-w-2xl">
          NEXORA AI is an academic prototype designed to demonstrate the principles of
          explainable decision intelligence. The system employs a Retrieval-Augmented
          Generation (RAG) pipeline to produce transparent, evidence-grounded
          recommendations. All outputs require mandatory human validation prior to
          finalization, ensuring accountability and auditability throughout the
          decision-making process.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {principles.map((p) => (
          <Card key={p.title} className="border bg-secondary/50">
            <CardContent className="p-6 text-center space-y-3">
              <p.icon className="w-8 h-8 mx-auto text-primary" />
              <h2 className="text-base font-semibold text-foreground leading-tight">{p.title}</h2>
              <p className="text-sm text-muted-foreground leading-6">{p.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Button onClick={nextStep} size="lg">
        Begin Decision Flow →
      </Button>
    </div>
  );
};

export default StepIntroduction;
