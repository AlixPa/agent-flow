import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState } from "react";
import { GraphTab } from "./widgets/graph-tab";
import "@xyflow/react/dist/style.css";
import { DnDProvider } from "./contexts/dnd-context";
import { ReactFlowProvider } from "@xyflow/react";

type Tab = "graph" | "conversation";

function App() {
  const [tab, setTab] = useState<Tab>("graph");

  const handleTabChange = (v: string) => {
    setTab(v as Tab);
  };

  return (
    <Tabs
      defaultValue="graph"
      value={tab}
      onValueChange={handleTabChange}
      className="h-screen"
    >
      <TabsList>
        <TabsTrigger value="graph">Graph</TabsTrigger>
        <TabsTrigger value="conversation">Conversation</TabsTrigger>
      </TabsList>
      <TabsContent value="graph">
        <ReactFlowProvider>
          <DnDProvider>
            <GraphTab />
          </DnDProvider>
        </ReactFlowProvider>
      </TabsContent>
      <TabsContent value="conversation">Conversation tab</TabsContent>
    </Tabs>
  );
}

export default App;
