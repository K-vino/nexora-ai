import { useDecisionFlow } from "@/context/DecisionFlowContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, X, AlertTriangle, FileText } from "lucide-react";
import { useRef, useState } from "react";
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

const StepEvidenceUpload = () => {
  const { files, addFile, removeFile, isDuplicateFile, nextStep, prevStep } = useDecisionFlow();
  const [error, setError] = useState("");
  const [removeTarget, setRemoveTarget] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    setError("");
    const duplicates: string[] = [];
    Array.from(fileList).forEach((f) => {
      if (isDuplicateFile(f.name)) {
        duplicates.push(f.name);
      } else {
        addFile({ name: f.name, size: f.size, id: crypto.randomUUID() });
      }
    });
    if (duplicates.length > 0) {
      setError(`Duplicate file(s) detected and skipped: ${duplicates.join(", ")}`);
    }
  };

  const handleProceed = () => {
    if (files.length === 0) {
      setError("At least one evidence document is required before proceeding to analysis.");
      return;
    }
    nextStep();
  };

  const confirmRemove = () => {
    if (removeTarget) {
      removeFile(removeTarget);
      setRemoveTarget(null);
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const truncateName = (name: string, max = 40) =>
    name.length > max ? name.substring(0, max - 3) + "..." : name;

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-[28px] font-semibold text-foreground leading-tight">Upload Evidence Documents</h1>
        <p className="text-sm text-muted-foreground leading-6">
          Provide the documents that will serve as the evidence base for analysis.
          The system will process only the uploaded materials — no external data sources are accessed.
        </p>
      </div>

      {/* Drop zone */}
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); handleFiles(e.dataTransfer.files); }}
        className="border-2 border-dashed border-muted-foreground/30 rounded-lg p-12 text-center cursor-pointer hover:border-primary/50 transition-colors"
      >
        <Upload className="w-10 h-10 mx-auto text-muted-foreground mb-3" />
        <p className="text-foreground font-medium leading-7">Drop files here or click to browse</p>
        <p className="text-sm text-muted-foreground mt-1 leading-6">
          Accepted formats: PDF, TXT, DOCX — Maximum 10 MB per file
        </p>
        <input
          ref={inputRef}
          type="file"
          multiple
          accept=".pdf,.txt,.docx"
          className="hidden"
          onChange={(e) => { handleFiles(e.target.files); if (inputRef.current) inputRef.current.value = ""; }}
        />
      </div>

      {/* Warning */}
      <div className="flex items-start gap-3 p-4 rounded-lg bg-warning text-warning-foreground">
        <AlertTriangle className="w-5 h-5 mt-0.5 shrink-0" />
        <p className="text-sm leading-6">
          <strong>Data Isolation Notice:</strong> Only uploaded documents will be used for analysis.
          The system does not perform internet retrieval or access external databases.
        </p>
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
            Uploaded Documents ({files.length})
          </p>
          {files.map((f) => (
            <Card key={f.id}>
              <CardContent className="p-4 flex items-center justify-between gap-3">
                <div className="flex items-center gap-3 min-w-0">
                  <FileText className="w-4 h-4 text-muted-foreground shrink-0" />
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-foreground truncate" title={f.name}>
                      {truncateName(f.name)}
                    </p>
                    <p className="text-xs text-muted-foreground">{formatSize(f.size)}</p>
                  </div>
                </div>
                <button
                  onClick={() => setRemoveTarget(f.id)}
                  className="text-muted-foreground hover:text-destructive shrink-0"
                  aria-label={`Remove ${f.name}`}
                >
                  <X className="w-4 h-4" />
                </button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {error && <p className="text-sm text-destructive leading-6">{error}</p>}

      {/* Navigation */}
      <div className="flex justify-between pt-4">
        <Button variant="ghost" onClick={prevStep}>← Back</Button>
        <Button onClick={handleProceed} disabled={files.length === 0}>
          Proceed to Analysis →
        </Button>
      </div>

      {/* Remove confirmation dialog */}
      <AlertDialog open={!!removeTarget} onOpenChange={(open) => !open && setRemoveTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Remove Document</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to remove this document from the evidence set?
              This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={confirmRemove}>Remove</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default StepEvidenceUpload;
