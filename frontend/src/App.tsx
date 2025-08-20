import "@xyflow/react/dist/style.css";
import { BrowserRouter, Route, Routes } from "react-router";
import { CreateGraphScreen } from "./pages/create-graph";
import GraphList from "./pages/graph-list";
import GraphDetails from "./pages/graph-details";
import Layout from "./pages/layout";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/create" element={<CreateGraphScreen />} />
          <Route path="/graph">
            <Route index element={<GraphList />} />
            <Route path=":graph" element={<GraphDetails />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
