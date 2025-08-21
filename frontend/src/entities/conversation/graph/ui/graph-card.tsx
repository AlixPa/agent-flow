import { Link } from "react-router";
import type { Graph } from "../model";
import { Card, CardContent, CardTitle } from "@/components/ui/card";

type Props = {
  graph: Graph;
};

export const GraphCard = ({ graph }: Props) => {
  return (
    <Link to={`/graph/${graph.id}`}>
      <Card key={graph.id} className="w-80 h-40">
        <CardContent>
          <CardTitle>{graph.name}</CardTitle>
          <p>{graph.memo}</p>
          <p>{graph.createdAt}</p>
        </CardContent>
      </Card>
    </Link>
  );
};
