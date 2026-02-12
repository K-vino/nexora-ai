import { DecisionFlowProvider } from "@/context/DecisionFlowContext";
import WizardLayout from "@/components/WizardLayout";

const Index = () => (
  <DecisionFlowProvider>
    <WizardLayout />
  </DecisionFlowProvider>
);

export default Index;
