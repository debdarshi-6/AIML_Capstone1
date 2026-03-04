import axios from "axios";

// Change to true if backend is not running
const USE_MOCK = false;

// Your deployed API
// Change this to your local IP while testing
const API_URL = "https://aiml-capstone1.onrender.com"; 

const api = axios.create({
  baseURL: API_URL, // Use the variable here
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000,
});

export const predictTicket = async (ticket_text) => {
  // -------------------------
  // MOCK RESPONSE
  // -------------------------
  if (USE_MOCK) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          department: "Tech",
          priority: "High",
        });
      }, 800);
    });
  }

  try {
    const response = await api.post("/predict", {
      ticket_text: ticket_text,
    });
    return response.data;
    
  } catch (error) {
    console.error("Prediction failed:", error);
    throw error;
  }
};