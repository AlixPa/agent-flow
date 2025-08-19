import "@xyflow/react/dist/style.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { CreateGraphScreen } from "./pages/create-graph";
import GraphList from "./pages/graph-list";
import GraphDetails from "./pages/graph-details";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GraphList />} />
        <Route path="/create" element={<CreateGraphScreen />} />
        <Route path="graph">
          <Route path=":graph" element={<GraphDetails />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
