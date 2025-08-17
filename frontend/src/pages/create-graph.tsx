import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState } from "react";
import "@xyflow/react/dist/style.css";
import { ReactFlowProvider } from "@xyflow/react";
import { DnDProvider } from "@/contexts/dnd-context";
import { GraphTab } from "@/widgets/graph-tab";
import { ConversationTab } from "@/widgets/conversation-tab";

type Tab = "graph" | "conversation";

export const CreateGraphScreen = () => {
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
      <TabsContent value="conversation">
        <ConversationTab />
      </TabsContent>
    </Tabs>
  );
};
