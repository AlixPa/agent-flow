import "@xyflow/react/dist/style.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { CreateGraphScreen } from "./pages/create-graph";
import GraphList from "./pages/graph-list";

function App() {
  return (
     <BrowserRouter>
      <Routes>
        <Route path="/" element={<GraphList />} />
        <Route path="/create" element={<CreateGraphScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
