import { Button } from "@/components/ui/button";
import { Card, CardAction, CardContent, CardTitle } from "@/components/ui/card";
import "@xyflow/react/dist/style.css";
import { Link } from "react-router";

const dummyGraph = [
  {
    id: 1,
    name: "Graph1",
  },
  {
    id: 2,
    name: "Graph2",
  },
];

function GraphList() {
  return (
    <div className="flex justify-between">
      <div className="flex gap-4">
        {dummyGraph.map((g) => {
          return (
            <Card key={g.id}>
              <CardContent>
                <CardTitle>{g.name}</CardTitle>
                <CardAction>
                  <Button asChild>
                    <Link to={`/graph/${g.id}`}>Edit</Link>
                  </Button>
                </CardAction>
              </CardContent>
            </Card>
          );
        })}
      </div>
      <Button asChild>
        <Link to="/create">新規作成</Link>
      </Button>
    </div>
  );
}

export default GraphList;
