import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";
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

const FlowDiagram = ({ items }: { items: string[] }) => (
  <div className="flex flex-wrap items-center gap-2 py-2">
    {items.map((item, i) => (
      <div key={i} className="flex items-center gap-2">
        <div className="px-4 py-2.5 rounded-lg border bg-secondary text-xs font-medium text-foreground leading-tight">
          {item}
        </div>
        {i < items.length - 1 && <ArrowRight className="w-4 h-4 text-muted-foreground shrink-0" />}
      </div>
    ))}
  </div>
);

const StepDefenseSummary = () => {
  const { reset } = useDecisionFlow();
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  const handleReset = () => {
    setShowResetConfirm(false);
    reset();
  };

  return (
    <div className="space-y-8 print:space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Project Defense Summary</h1>
        <p className="text-sm text-muted-foreground leading-6">
          Comprehensive overview of the system architecture, methodology, and academic contributions
          for project evaluation and defense presentation.
        </p>
      </div>

      {/* 1. RAG Pipeline */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">1. RAG Pipeline Architecture</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <FlowDiagram items={["Document Ingestion", "Chunking", "Embedding Generation", "Vector Retrieval", "Prompt Construction", "LLM Inference", "Structured Output"]} />
          <ul className="list-disc list-inside text-sm text-muted-foreground leading-7 space-y-1">
            <li>Documents are segmented into semantically coherent chunks for granular retrieval</li>
            <li>Dense vector embeddings enable similarity-based evidence retrieval</li>
            <li>Retrieved context is assembled into a structured prompt with explicit instructions</li>
            <li>LLM output is constrained to recommendation, factors, and confidence assessment</li>
          </ul>
        </CardContent>
      </Card>

      {/* 2. Explainability Architecture */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">2. Explainability Architecture</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <FlowDiagram items={["Evidence Chunks", "Relevance Scoring", "Context Assembly", "Reasoning Chain", "Structured Output"]} />
          <ul className="list-disc list-inside text-sm text-muted-foreground leading-7 space-y-1">
            <li>Each recommendation is fully traceable to specific evidence segments</li>
            <li>Relevance scores quantify the contribution of each evidence segment</li>
            <li>Reasoning chain provides a logical narrative connecting evidence to conclusion</li>
            <li>Academic citation-style referencing enables source verification</li>
          </ul>
        </CardContent>
      </Card>

      {/* 3. Human-in-the-Loop */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">3. Human-in-the-Loop Decision Flow</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <FlowDiagram items={["AI Generates Recommendation", "Human Reviews Evidence", "Human Validates Decision", "Decision Recorded"]} />
          <ul className="list-disc list-inside text-sm text-muted-foreground leading-7 space-y-1">
            <li>AI serves exclusively as an advisory system — it cannot finalize decisions</li>
            <li>Human validator must review the explainability analysis before approval</li>
            <li>Rejection and modification require written justification for audit trail</li>
            <li>Accountability acknowledgment is mandatory prior to finalization</li>
          </ul>
        </CardContent>
      </Card>

      {/* 4. Data Storage */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">4. Data Capture Summary</CardTitle></CardHeader>
        <CardContent>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2 pr-4 font-semibold text-muted-foreground">Pipeline Stage</th>
                <th className="text-left py-2 font-semibold text-muted-foreground">Data Captured</th>
              </tr>
            </thead>
            <tbody className="text-foreground">
              {[
                ["Evidence Upload", "File metadata (name, size, type), document content"],
                ["Processing Pipeline", "Text chunks, vector embeddings, retrieval similarity scores"],
                ["AI Recommendation", "Recommendation text, influencing factors, confidence score"],
                ["Explainability", "Evidence snippets with source attribution, relevance scores, reasoning chain"],
                ["Human Validation", "Decision type (approve/reject/modify), justification text, acknowledgment status"],
                ["Decision Record", "Complete auditable record with timestamp and unique reference ID"],
              ].map(([step, data]) => (
                <tr key={step} className="border-b last:border-b-0">
                  <td className="py-2.5 pr-4 font-medium">{step}</td>
                  <td className="py-2.5 leading-6">{data}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>

      {/* 5. Key Academic Contributions */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">5. Key Academic Contributions</CardTitle></CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-2 text-sm text-foreground leading-7">
            <li><strong>Explainable AI Implementation:</strong> Demonstrates a practical approach to AI transparency through evidence attribution and structured reasoning chains</li>
            <li><strong>Human-in-the-Loop Framework:</strong> Enforces mandatory human oversight with accountability mechanisms, preventing autonomous AI decision-making</li>
            <li><strong>RAG-Based Decision Intelligence:</strong> Applies Retrieval-Augmented Generation to domain-specific decision support with quantified confidence scoring</li>
            <li><strong>Auditable Decision Trail:</strong> Creates a complete, traceable record of the decision process from evidence through to final human determination</li>
          </ul>
        </CardContent>
      </Card>

      {/* 6. Limitations */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">6. Known Limitations</CardTitle></CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-1 text-sm text-foreground leading-7">
            <li>Processing pipeline is simulated with timed delays rather than actual NLP computation</li>
            <li>No real LLM integration — recommendation outputs are hardcoded demonstration content</li>
            <li>Limited file type support restricted to PDF, TXT, and DOCX formats</li>
            <li>Files are registered but not parsed — document content analysis is simulated</li>
            <li>State persistence uses browser localStorage — no server-side database integration</li>
            <li>Single-user prototype — no concurrent multi-user or authentication support</li>
          </ul>
        </CardContent>
      </Card>

      {/* 7. Future Improvements */}
      <Card>
        <CardHeader className="pb-2"><CardTitle className="text-lg">7. Future Improvements</CardTitle></CardHeader>
        <CardContent>
          <ul className="list-disc list-inside space-y-1 text-sm text-foreground leading-7">
            <li>Integration with production LLM APIs (e.g., OpenAI, Anthropic) for real inference</li>
            <li>Implementation of vector database (e.g., Pinecone, Weaviate) for actual semantic retrieval</li>
            <li>Server-side persistence with PostgreSQL for multi-session decision tracking</li>
            <li>Role-based access control for multi-stakeholder decision workflows</li>
            <li>PDF parsing and OCR integration for automated document content extraction</li>
            <li>Export functionality for decision records in standardised formats (PDF, CSV)</li>
          </ul>
        </CardContent>
      </Card>

      <div className="flex gap-3 pt-4 no-print">
        <Button variant="outline" onClick={() => window.print()}>Print Summary</Button>
        <Button onClick={() => setShowResetConfirm(true)}>Start New Decision</Button>
      </div>

      {/* Reset confirmation */}
      <AlertDialog open={showResetConfirm} onOpenChange={setShowResetConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Reset Decision Flow</AlertDialogTitle>
            <AlertDialogDescription>
              This will clear all current session data including uploaded documents,
              the AI recommendation, and the finalized decision record.
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleReset}>Confirm Reset</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default StepDefenseSummary;
