export type Graph = { 
  id: string,
  name: string,
  memo?: string,
  createdAt: string,
}

export const fixture: Graph[] = [
  {
    id: "a3f1d4c2-7e9b-4c41-9d2f-89f8a2c3b6e1",
    name: "Content Generation Pipeline",
    memo: "An AI agent chain that automatically generates blog articles",
    createdAt: "2024/12/15"
  },
  {
    id: "b6a9e2f4-1c8d-4f2b-93ab-6d7c1e4f2a89",
    name: "Customer Support Bot",
    memo: "A multi-agent system that automates customer support",
    createdAt: "2024/12/14"
  },
  {
    id: "c4d7f3e9-8b2a-4e91-94f1-7a3b2d5e9c47",
    name: "Data Analysis Workflow",
    memo: "A workflow that automates everything from data analysis to insight generation",
    createdAt: "2024/12/13"
  }
];