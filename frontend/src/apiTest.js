import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchRainfallComparison() {
  try {
    const response = await axios.get(`${API_BASE_URL}/compare?state1=Karnataka&state2=Kerala`);
    return response.data;
  } catch (error) {
    console.error("Error fetching rainfall comparison:", error);
    return null;
  }
}
