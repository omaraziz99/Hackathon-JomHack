// src/stores/disputes.js
import { defineStore } from "pinia";

export const useDisputeStore = defineStore("disputes", {
  state: () => ({
    // Active Disputes Data
    activeDisputes: [
      {
        id: 1,
        type: "Unauthorized Transaction",
        amount: 500,
        status: "High Risk",
        timeRemaining: "1h 45m",
        riskScore: 85,
        description: "User claims transaction was not authorized",
        patterns: ["Multiple failed attempts", "New device", "Unusual amount"],
        buyer: {
          username: "john_doe",
          accountAge: "2 years",
          previousDisputes: 0,
          riskScore: "Low",
          verifiedStatus: true,
        },
        seller: {
          username: "jane_smith",
          accountAge: "1 year",
          previousDisputes: 1,
          riskScore: "Medium",
          verifiedStatus: false,
        },
        evidence: [
          {
            id: 1,
            type: "Bank Transfer PDF",
            submittedAt: "2023-07-20 14:35",
            verified: true,
            documentUrl: "/document.pdf",
            videoUrl: "/video.mp4",
            pendingParty: null,
            verificationDetails: "Document verified with bank records",
          },
          {
            id: 2,
            type: "Pending Evidence",
            submittedAt: null,
            verified: false,
            documentUrl: null,
            videoUrl: null,
            pendingParty: "seller",
            verificationDetails: "Awaiting submission",
          },
        ],
        createdAt: "2023-07-20 14:30",
        deadline: "2023-07-21 14:30",
      },
      {
        id: 2,
        type: "Non-receipt of Goods",
        amount: 250,
        status: "Medium Risk",
        timeRemaining: "1h 30m",
        riskScore: 65,
        description: "Buyer hasn't received the item",
        patterns: ["First-time seller", "No tracking provided"],
        buyer: {
          username: "sarah_parker",
          accountAge: "3 years",
          previousDisputes: 1,
          riskScore: "Low",
          verifiedStatus: true,
        },
        seller: {
          username: "new_seller123",
          accountAge: "1 month",
          previousDisputes: 0,
          riskScore: "High",
          verifiedStatus: false,
        },
        evidence: [],
        createdAt: "2023-07-20 15:00",
        deadline: "2023-07-21 15:00",
      },
    ],

    // AI Resolved Disputes Data
    aiResolvedDisputes: [
      {
        id: "D123456",
        type: "Buyer Underpaid",
        amount: 500.0,
        resolution: "Auto-resolved",
        closedAt: "2023-07-20 15:30",
        aiConfidenceScore: 98,
        patternMatch: "Clear underpayment pattern",
        resolvedAt: "2023-07-20 15:31",
        resolutionConfidence: 98,
        buyer: {
          username: "michael_b",
          accountAge: "4 years",
          previousDisputes: 0,
          riskScore: "Low",
          verifiedStatus: true,
        },
        seller: {
          username: "tech_store",
          accountAge: "5 years",
          previousDisputes: 2,
          riskScore: "Low",
          verifiedStatus: true,
        },
        aiAnalysis: {
          conclusion: "Clear underpayment case",
          evidenceVerified: true,
          fraudChecks: {
            documentAuthenticity: "Verified",
            transactionMatch: "Confirmed",
            patternAnalysis: "No suspicious patterns",
          },
          resolutionDetails: "Seller refunded difference automatically",
          timeToResolve: "45 seconds",
        },
        evidence: [
          {
            id: 1,
            type: "Payment Receipt",
            submittedAt: "2023-07-20 15:30",
            verified: true,
            verificationDetails: "Document verified through blockchain",
            url: "/receipt.pdf",
          },
        ],
        createdAt: "2023-07-20 15:30",
      },
      {
        id: "D123457",
        type: "Buyer Overpaid",
        amount: 1200.0,
        resolution: "Auto-refunded",
        closedAt: "2023-07-20 16:45",
        aiConfidenceScore: 99,
        patternMatch: "System calculation error",
        resolvedAt: "2023-07-20 16:46",
        resolutionConfidence: 99,
        buyer: {
          username: "emma_w",
          accountAge: "2 years",
          previousDisputes: 1,
          riskScore: "Low",
          verifiedStatus: true,
        },
        seller: {
          username: "global_shop",
          accountAge: "3 years",
          previousDisputes: 0,
          riskScore: "Low",
          verifiedStatus: true,
        },
        aiAnalysis: {
          conclusion: "Verified overpayment",
          evidenceVerified: true,
          fraudChecks: {
            documentAuthenticity: "Verified",
            transactionMatch: "Confirmed",
            patternAnalysis: "Normal transaction pattern",
          },
          resolutionDetails: "Excess amount automatically refunded to buyer",
          timeToResolve: "30 seconds",
        },
        evidence: [
          {
            id: 1,
            type: "Transaction Log",
            submittedAt: "2023-07-20 16:45",
            verified: true,
            verificationDetails: "System log verified",
            url: "/transaction.pdf",
          },
        ],
        createdAt: "2023-07-20 16:45",
      },
    ],

    // Metrics Data with Deriv color scheme
    activeMetrics: [
      {
        title: "Active Disputes",
        value: "24",
        icon: "mdi-alert-circle",
        color: "#ff444f", // Deriv Red
      },
      {
        title: "Avg Resolution Time",
        value: "1.5h",
        icon: "mdi-clock",
        color: "#377cfc", // Deriv Blue
      },
      {
        title: "Resolved Today",
        value: "18",
        icon: "mdi-check-circle",
        color: "#4bb4b3", // Deriv Green
      },
      {
        title: "Fraud Prevented",
        value: "$2.4k",
        icon: "mdi-shield",
        color: "#377cfc", // Deriv Blue
      },
    ],

    aiMetrics: [
      {
        title: "AI Resolutions",
        value: "156",
        icon: "mdi-robot",
        color: "#ff444f", // Deriv Red
      },
      {
        title: "Avg AI Resolution Time",
        value: "45s",
        icon: "mdi-clock-fast",
        color: "#377cfc", // Deriv Blue
      },
      {
        title: "Success Rate",
        value: "98%",
        icon: "mdi-check-circle",
        color: "#4bb4b3", // Deriv Green
      },
      {
        title: "Cost Saved",
        value: "$5.2k",
        icon: "mdi-cash",
        color: "#377cfc", // Deriv Blue
      },
    ],
  }),

  getters: {
    // Get active dispute by ID with error handling
    getActiveDisputeById: (state) => (id) => {
      const dispute = state.activeDisputes.find((d) => d.id === Number(id));
      if (!dispute) {
        console.warn(`Active dispute with ID ${id} not found`);
        return null;
      }
      return dispute;
    },

    // Get AI resolved dispute by ID with error handling
    getAiResolvedDisputeById: (state) => (id) => {
      const dispute = state.aiResolvedDisputes.find((d) => d.id === id);
      if (!dispute) {
        console.warn(`AI resolved dispute with ID ${id} not found`);
        return null;
      }
      return dispute;
    },

    // Metrics getters with default values
    getActiveMetrics: (state) => state.activeMetrics || [],
    getAiMetrics: (state) => state.aiMetrics || [],

    // Additional computed getters
    totalDisputes: (state) =>
      state.activeDisputes.length + state.aiResolvedDisputes.length,

    highRiskDisputes: (state) =>
      state.activeDisputes.filter((dispute) => dispute.status === "High Risk"),

    averageResolutionConfidence: (state) => {
      const confidences = state.aiResolvedDisputes.map(
        (d) => d.aiConfidenceScore
      );
      return confidences.length
        ? (confidences.reduce((a, b) => a + b, 0) / confidences.length).toFixed(
            1
          )
        : 0;
    },
  },

  actions: {
    // Fetch active disputes with error handling and loading state
    async fetchActiveDisputes() {
      try {
        const response = await fetch("http://localhost:8000/disputes/active");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.activeDisputes = data;
      } catch (error) {
        console.error("Error fetching active disputes:", error);
        // Keep using mock data if API fails
      }
    },

    // Fetch AI resolved disputes with error handling
    async fetchAiResolvedDisputes() {
      try {
        const response = await fetch(
          "http://localhost:8000/disputes/ai-resolved"
        );
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.aiResolvedDisputes = data;
      } catch (error) {
        console.error("Error fetching AI resolved disputes:", error);
        // Keep using mock data if API fails
      }
    },

    // Fetch metrics with error handling and parallel requests
    async fetchMetrics() {
      try {
        const [activeResponse, aiResponse] = await Promise.all([
          fetch("http://localhost:8000/disputes/active-metrics"),
          fetch("http://localhost:8000/disputes/ai-metrics"),
        ]);

        if (!activeResponse.ok || !aiResponse.ok) {
          throw new Error("One or more metric requests failed");
        }

        const activeData = await activeResponse.json();
        const aiData = await aiResponse.json();

        this.activeMetrics = activeData;
        this.aiMetrics = aiData;
      } catch (error) {
        console.error("Error fetching metrics:", error);
        // Keep using mock data if API fails
      }
    },

    // Additional action for updating dispute status
    async updateDisputeStatus(disputeId, newStatus) {
      try {
        const dispute = this.activeDisputes.find((d) => d.id === disputeId);
        if (!dispute) {
          throw new Error(`Dispute with ID ${disputeId} not found`);
        }

        const response = await fetch(
          `http://localhost:8000/disputes/${disputeId}/status`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ status: newStatus }),
          }
        );

        if (!response.ok) {
          throw new Error(
            `Failed to update dispute status: ${response.status}`
          );
        }

        // Update local state
        dispute.status = newStatus;
      } catch (error) {
        console.error("Error updating dispute status:", error);
        throw error;
      }
    },

    // Initialize store with default data
    async initializeStore() {
      await Promise.all([
        this.fetchActiveDisputes(),
        this.fetchAiResolvedDisputes(),
        this.fetchMetrics(),
      ]);
    },
  },
});
