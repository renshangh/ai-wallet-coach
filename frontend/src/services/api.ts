import axios from "axios";
const api = axios.create({ baseURL: "http://localhost:5057/api" });
export const getProfile = () => api.get("/profile").then(r => r.data);
export const getTransactions = () => api.get("/transactions").then(r => r.data);
export const getInsights = () => api.get("/insights").then(r => r.data);
export const acceptNudge = (type: string) => api.post("/nudge/accept", { type }).then(r => r.data);
export const getYieldAlts = () => api.get("/yield/alternatives").then(r => r.data);

export const fetchLLMNudge = () => api.get("/nudge/llm").then(r => r.data);
