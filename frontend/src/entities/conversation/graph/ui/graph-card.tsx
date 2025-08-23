import { Link } from "react-router";
import type { Graph } from "../model";
import {
  Card,
  CardContent,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";

type Props = {
  graph: Graph;
};

export const GraphCard = ({ graph }: Props) => {
  return (
    <Link to={`/graph/${graph.id}`}>
      <Card key={graph.id} className="w-80 h-45">
        <CardContent className="flex flex-col h-full">
          <CardTitle>{graph.name}</CardTitle>
          <CardDescription>{graph.memo}</CardDescription>
          <div className="flex flex-col justify-end flex-1">
            <div className="flex items-center gap-1">
              <i className="fa-regular fa-calendar text-muted-foreground"></i>
              <p className="text-muted-foreground text-md">{graph.createdAt}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};
