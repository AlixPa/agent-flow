import { useDnD } from "@/contexts/dnd-context";

export const AgentsSidebar = () => {
  const [_, setType] = useDnD();

  const onDragStart = (
    event: React.DragEvent<HTMLDivElement>,
    nodeType: string
  ) => {
    setType(nodeType);
    event.dataTransfer.effectAllowed = "move";
  };
  
  return (
    <aside>
      <div draggable onDragStart={(e) => onDragStart(e, "input")}>
        Input Node
      </div>
      <div draggable onDragStart={(e) => onDragStart(e, "default")}>
        Default Node
      </div>
      <div draggable onDragStart={(e) => onDragStart(e, "output")}>
        Output Node
      </div>
    </aside>
  );
};
