import React, { createContext, useContext, useState, useCallback, useEffect } from "react";

export interface UploadedFile {
  name: string;
  size: number;
  id: string;
}

export type ValidationDecision = "approve" | "reject" | "modify" | null;

interface DecisionFlowState {
  currentStep: number;
  files: UploadedFile[];
  processingComplete: boolean;
  decision: ValidationDecision;
  explanation: string;
  finalized: boolean;
  finalizedAt: string | null;
  decisionId: string;
  hasViewedExplanation: boolean;
  acknowledged: boolean;
}

interface DecisionFlowContextType extends DecisionFlowState {
  goToStep: (step: number) => void;
  nextStep: () => void;
  prevStep: () => void;
  addFile: (file: UploadedFile) => void;
  removeFile: (id: string) => void;
  setProcessingComplete: (v: boolean) => void;
  setDecision: (d: ValidationDecision) => void;
  setExplanation: (e: string) => void;
  setHasViewedExplanation: (v: boolean) => void;
  setAcknowledged: (v: boolean) => void;
  finalize: () => void;
  reset: () => void;
  isDuplicateFile: (name: string) => boolean;
}

const STORAGE_KEY = "nexora-ai-state";

const DecisionFlowContext = createContext<DecisionFlowContextType | null>(null);

const generateId = () =>
  `NXR-${Date.now().toString(36).toUpperCase()}-${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

const defaultState: DecisionFlowState = {
  currentStep: 1,
  files: [],
  processingComplete: false,
  decision: null,
  explanation: "",
  finalized: false,
  finalizedAt: null,
  decisionId: generateId(),
  hasViewedExplanation: false,
  acknowledged: false,
};

const loadPersistedState = (): DecisionFlowState => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...defaultState, decisionId: generateId() };
    const parsed = JSON.parse(raw) as DecisionFlowState;
    // Defensive null-checks
    return {
      currentStep: parsed.currentStep ?? 1,
      files: Array.isArray(parsed.files) ? parsed.files : [],
      processingComplete: parsed.processingComplete ?? false,
      decision: parsed.decision ?? null,
      explanation: parsed.explanation ?? "",
      finalized: parsed.finalized ?? false,
      finalizedAt: parsed.finalizedAt ?? null,
      decisionId: parsed.decisionId ?? generateId(),
      hasViewedExplanation: parsed.hasViewedExplanation ?? false,
      acknowledged: parsed.acknowledged ?? false,
    };
  } catch {
    return { ...defaultState, decisionId: generateId() };
  }
};

export const DecisionFlowProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<DecisionFlowState>(loadPersistedState);

  // Persist state to localStorage on every change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  // Warn before unload if mid-flow
  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      if (state.currentStep > 1 && !state.finalized) {
        e.preventDefault();
      }
    };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, [state.currentStep, state.finalized]);

  const goToStep = useCallback((step: number) => {
    setState((s) => {
      if (step > s.currentStep) return s;
      if (s.finalized && step < 7) return s;
      return { ...s, currentStep: step };
    });
  }, []);

  const nextStep = useCallback(() => {
    setState((s) => ({ ...s, currentStep: Math.min(s.currentStep + 1, 8) }));
  }, []);

  const prevStep = useCallback(() => {
    setState((s) => {
      if (s.finalized) return s;
      return { ...s, currentStep: Math.max(s.currentStep - 1, 1) };
    });
  }, []);

  const addFile = useCallback((file: UploadedFile) => {
    setState((s) => ({ ...s, files: [...s.files, file] }));
  }, []);

  const removeFile = useCallback((id: string) => {
    setState((s) => ({ ...s, files: s.files.filter((f) => f.id !== id) }));
  }, []);

  const isDuplicateFile = useCallback(
    (name: string) => state.files.some((f) => f.name === name),
    [state.files]
  );

  const setProcessingComplete = useCallback((v: boolean) => {
    setState((s) => ({ ...s, processingComplete: v }));
  }, []);

  const setDecision = useCallback((d: ValidationDecision) => {
    setState((s) => ({ ...s, decision: d }));
  }, []);

  const setExplanation = useCallback((e: string) => {
    setState((s) => ({ ...s, explanation: e }));
  }, []);

  const setHasViewedExplanation = useCallback((v: boolean) => {
    setState((s) => ({ ...s, hasViewedExplanation: v }));
  }, []);

  const setAcknowledged = useCallback((v: boolean) => {
    setState((s) => ({ ...s, acknowledged: v }));
  }, []);

  const finalize = useCallback(() => {
    setState((s) => ({ ...s, finalized: true, finalizedAt: new Date().toISOString() }));
  }, []);

  const reset = useCallback(() => {
    const newState = { ...defaultState, decisionId: generateId() };
    setState(newState);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return (
    <DecisionFlowContext.Provider
      value={{
        ...state,
        goToStep, nextStep, prevStep,
        addFile, removeFile, isDuplicateFile,
        setProcessingComplete, setDecision, setExplanation,
        setHasViewedExplanation, setAcknowledged,
        finalize, reset,
      }}
    >
      {children}
    </DecisionFlowContext.Provider>
  );
};

export const useDecisionFlow = () => {
  const ctx = useContext(DecisionFlowContext);
  if (!ctx) throw new Error("useDecisionFlow must be used within DecisionFlowProvider");
  return ctx;
};
