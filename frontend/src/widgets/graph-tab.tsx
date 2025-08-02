import { useDnD } from "@/contexts/dnd-context";
import { AgentsSidebar } from "@/features/agents-sidebar";
import {
  addEdge,
  Background,
  Controls,
  ReactFlow,
  useEdgesState,
  useNodesState,
  useReactFlow,
  type OnConnect,
} from "@xyflow/react";
import { useCallback } from "react";

const initialNodes = [
  {
    id: "1",
    type: "input",
    data: { label: "input node" },
    position: { x: 250, y: 5 },
  },
];

let id = 0;

const getId = () => `dndnode_${id}`;

export const GraphTab = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const { screenToFlowPosition } = useReactFlow();

  const [type, setType] = useDnD();

  const onConnect: OnConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  const onDragOver: React.DragEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";
    },
    []
  );

  const onDrop: React.DragEventHandler<HTMLDivElement> = useCallback((e) => {
    e.preventDefault()
    if (!type) return;

    const position = screenToFlowPosition({
      x: e.clientX,
      y: e.clientY,
    });

    const nodeId = getId();

    const newNode = {
      id: nodeId,
      type,
      position,
      data: { label: `${type} node` },
    };

    setNodes((nodes) => [...nodes, newNode]);
    id++;
  }, [screenToFlowPosition, type]);

  const onDragStart: React.DragEventHandler<HTMLDivElement> = (
    e: React.DragEvent<HTMLDivElement>,
    nodeType?: string
  ) => {
    if (nodeType === undefined) return;
    setType(nodeType);
    e.dataTransfer.setData("text/plain", nodeType);
    e.dataTransfer.effectAllowed = "move";
  };

  return (
    <div className="flex flex-row gap-4 p-4 h-full" >
      <AgentsSidebar />
      <div className="w-full border-2 border-orange-400 rounded-4xl">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDragStart={onDragStart}
          onDragOver={onDragOver}
          onDrop={onDrop}
          fitView
        >
          <Controls />
          <Background />
        </ReactFlow>
      </div>
    </div>
  );
};
