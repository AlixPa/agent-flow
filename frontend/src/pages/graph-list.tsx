import { Button } from "@/components/ui/button";
import { fixture } from "@/entities/conversation/graph/model";
import { GraphCard } from "@/entities/conversation/graph/ui/graph-card";
import "@xyflow/react/dist/style.css";
import { Link } from "react-router";

function GraphList() {
  return (
    <div className="flex flex-col gap-6">
      <Button asChild className="ml-auto">
        <Link to="/create">Create New</Link>
      </Button>
      <div className="flex gap-4">
        {fixture.map((g) => {
          return <GraphCard key={g.id} graph={g} />;
        })}
      </div>
    </div>
  );
}

export default GraphList;
