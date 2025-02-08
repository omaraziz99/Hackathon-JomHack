// stores/disputes.js
import { defineStore } from "pinia";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

// Add axios interceptor for better error handling
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    if (error.response?.status === 500) {
      // Handle server errors
      console.error("Server error:", error.response.data);
    }
    return Promise.reject(error);
  }
);

export const useDisputeStore = defineStore("disputes", {
  state: () => ({
    disputes: [],
    aiResolvedDisputes: [],
    activeDispute: null,
    loading: false,
    error: null,
  }),

  getters: {
    getActiveDisputeById: (state) => (id) => {
      return state.disputes.find((dispute) => dispute.id === id);
    },
    getAiResolvedDisputeById: (state) => (id) => {
      return state.aiResolvedDisputes.find((dispute) => dispute.id === id);
    },
  },

  actions: {
    async fetchActiveDisputes() {
      this.loading = true;
      try {
        const response = await axios.get(`${API_BASE_URL}/disputes`);
        this.disputes = response.data.data.filter((d) => !d.resolvedAt);
        return this.disputes;
      } catch (error) {
        console.error("Error fetching active disputes:", error);
        this.error = error.message;
        this.disputes = [];
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchAiResolvedDisputes() {
      this.loading = true;
      try {
        const response = await axios.get(
          `${API_BASE_URL}/disputes?status=resolved`
        );
        this.aiResolvedDisputes = response.data.data.filter(
          (d) => d.resolvedAt
        );
        return this.aiResolvedDisputes;
      } catch (error) {
        console.error("Error fetching AI resolved disputes:", error);
        this.error = error.message;
        this.aiResolvedDisputes = [];
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchDisputeDetails(id) {
      this.loading = true;
      try {
        const response = await axios.get(`${API_BASE_URL}/disputes/${id}`);
        this.activeDispute = {
          ...response.data,
          isAIHandled: !!response.data.resolvedAt, // Add this flag
        };
        return this.activeDispute;
      } catch (error) {
        console.error("Error fetching dispute details:", error);
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    },
  },
});
