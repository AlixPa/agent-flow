import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState } from "react";

type Tab = "flow" | "chat";

function App() {
  const [tab, setTab] = useState<Tab>("flow");

  const handleTabChange = (v: string) => {
    setTab(v as Tab)
  }

  return (
    <Tabs defaultValue="flow" className="w-[400px]" value={tab} onValueChange={handleTabChange}>
      <TabsList>
        <TabsTrigger value="flow">Flow</TabsTrigger>
        <TabsTrigger value="chat">Chat</TabsTrigger>
      </TabsList>
      <TabsContent value="flow">
        Flow tab
      </TabsContent>
      <TabsContent value="chat">Chat tab</TabsContent>
    </Tabs>
  );
}

export default App;
