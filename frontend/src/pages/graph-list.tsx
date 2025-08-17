import { Button } from "@/components/ui/button";
import "@xyflow/react/dist/style.css";
import { Link } from "react-router";

function GraphList() {
  return (
    <>
      <>Show graph list here</>
      <Button asChild>
        <Link to="/create">新規作成</Link>
      </Button>
    </>
  );
}

export default GraphList;
