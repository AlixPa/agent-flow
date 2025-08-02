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
    <aside className="w-sm flex flex-col gap-3">
      <div className="border-2 border-pink-400 rounded-md p-2" draggable onDragStart={(e) => onDragStart(e, "input")}>
        Input Node
      </div>
      <div className="border-2 border-green-400 rounded-md p-2" draggable onDragStart={(e) => onDragStart(e, "default")}>
        Default Node
      </div>
      <div className="border-2 border-blue-400 rounded-md p-2" draggable onDragStart={(e) => onDragStart(e, "output")}>
        Output Node
      </div>
    </aside>
  );
};
