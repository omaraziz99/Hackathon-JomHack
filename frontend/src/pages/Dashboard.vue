<!-- src/views/DisputeDashboard.vue -->
<template>
  <v-container fluid class="dispute-dashboard">
    <v-tabs v-model="activeTab" :color="colors.primary">
      <v-tab value="active">Active Disputes</v-tab>
      <v-tab value="ai-closed">AI-Resolved Disputes</v-tab>
    </v-tabs>

    <v-window v-model="activeTab">
      <!-- Active Disputes Tab -->
      <v-window-item value="active">
        <!-- Summary Cards -->
        <v-row class="mb-6">
          <v-col
            v-for="(card, index) in activeMetrics"
            :key="index"
            cols="12"
            md="3"
          >
            <v-card class="metric-card">
              <v-card-text>
                <div class="d-flex justify-space-between align-center">
                  <div>
                    <div class="text-subtitle-1 metric-title">
                      {{ card.title }}
                    </div>
                    <div class="text-h4 metric-value">{{ card.value }}</div>
                  </div>
                  <v-icon :color="card.color" size="32">{{ card.icon }}</v-icon>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Active Disputes List -->
        <v-card class="disputes-card">
          <v-card-title
            class="d-flex justify-space-between align-center card-header"
          >
            <span>Active Disputes</span>
            <v-text-field
              v-model="activeSearchQuery"
              label="Search active disputes"
              prepend-inner-icon="mdi-magnify"
              dense
              outlined
              class="search-field"
              hide-details
            ></v-text-field>
          </v-card-title>

          <v-card-text>
            <v-list class="dispute-list">
              <v-list-item
                v-for="dispute in filteredActiveDisputes"
                :key="dispute.id"
                class="mb-4"
                @click="navigateToDispute(dispute.id, false)"
              >
                <v-card outlined class="w-100 dispute-item">
                  <v-card-text>
                    <div class="d-flex justify-space-between align-start mb-2">
                      <div>
                        <h3 class="dispute-title">{{ dispute.type }}</h3>
                        <p class="text-caption text--secondary">
                          {{ dispute.description }}
                        </p>
                      </div>
                      <v-chip :color="getRiskColor(dispute.status)" dark>
                        {{ dispute.status }}
                      </v-chip>
                    </div>
                    <v-row class="mt-4">
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">Amount</div>
                        <div class="value-text">${{ dispute.amount }}</div>
                      </v-col>
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">
                          Time Remaining
                        </div>
                        <div class="value-text">
                          {{ dispute.timeRemaining }}
                        </div>
                      </v-col>
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">Risk Score</div>
                        <div class="value-text">{{ dispute.riskScore }}%</div>
                      </v-col>
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">Patterns</div>
                        <div class="patterns-text">
                          {{ dispute.patterns.join(", ") }}
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-window-item>
      <!-- AI-Resolved Disputes Tab -->
      <v-window-item value="ai-closed">
        <v-row class="mb-6">
          <v-col
            v-for="(card, index) in aiMetrics"
            :key="index"
            cols="12"
            md="3"
          >
            <v-card class="metric-card">
              <v-card-text>
                <div class="d-flex justify-space-between align-center">
                  <div>
                    <div class="text-subtitle-1 metric-title">
                      {{ card.title }}
                    </div>
                    <div class="text-h4 metric-value">{{ card.value }}</div>
                  </div>
                  <v-icon :color="card.color" size="32">{{ card.icon }}</v-icon>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- AI-Resolved Disputes List -->
        <v-card class="disputes-card">
          <v-card-title
            class="d-flex justify-space-between align-center card-header"
          >
            <span>AI-Resolved Disputes</span>
            <v-text-field
              v-model="aiSearchQuery"
              label="Search AI-resolved disputes"
              prepend-inner-icon="mdi-magnify"
              dense
              outlined
              class="search-field"
              hide-details
            ></v-text-field>
          </v-card-title>

          <v-card-text>
            <v-list class="dispute-list">
              <v-list-item
                v-for="dispute in filteredAiDisputes"
                :key="dispute.id"
                class="mb-4"
                @click="navigateToDispute(dispute.id, true)"
              >
                <v-card outlined class="w-100 dispute-item">
                  <v-card-text>
                    <div class="d-flex justify-space-between align-start mb-2">
                      <div>
                        <h3 class="dispute-title">{{ dispute.type }}</h3>
                        <p class="text-caption text--secondary">
                          ID: {{ dispute.id }}
                        </p>
                      </div>
                      <div class="d-flex gap-2">
                        <v-chip :color="colors.success" dark>
                          {{ dispute.resolution }}
                        </v-chip>
                        <v-chip
                          :color="
                            dispute.aiConfidenceScore > 95
                              ? colors.success
                              : colors.warning
                          "
                          dark
                        >
                          AI Confidence: {{ dispute.aiConfidenceScore }}%
                        </v-chip>
                      </div>
                    </div>

                    <v-row class="mt-4">
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">Amount</div>
                        <div class="value-text">${{ dispute.amount }}</div>
                      </v-col>
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">
                          Resolution Time
                        </div>
                        <div class="value-text">
                          {{ dispute.aiAnalysis.timeToResolve }}
                        </div>
                      </v-col>
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">
                          Resolution Method
                        </div>
                        <div class="value-text">
                          {{ dispute.aiAnalysis.resolutionDetails }}
                        </div>
                      </v-col>
                      <v-col cols="12" md="3">
                        <div class="text-caption label-text">Verification</div>
                        <div class="patterns-text">
                          {{
                            dispute.aiAnalysis.fraudChecks.documentAuthenticity
                          }},
                          {{ dispute.aiAnalysis.fraudChecks.transactionMatch }}
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-window-item>
    </v-window>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useDisputeStore } from "@/stores/disputes.js";

const router = useRouter();
const disputeStore = useDisputeStore();

// Shared state
const activeTab = ref("active");
const activeSearchQuery = ref("");
const aiSearchQuery = ref("");

// Add to Dashboard.vue <script setup> section
const colors = {
  primary: "#ff444f", // Deriv Red
  secondary: "#85acb0", // Deriv Teal
  success: "#4bb4b3", // Deriv Green
  warning: "#ffad3a", // Deriv Orange
  info: "#377cfc", // Deriv Blue
  background: "#ffffff", // White
  text: "#333333", // Dark Text
  border: "#e6e9ed", // Border Color
  cardBg: "#f2f3f4", // Light Gray Background
};

// Get metrics from store with proper reactivity
const activeMetrics = computed(() => disputeStore.getActiveMetrics);
const aiMetrics = computed(() => disputeStore.getAiMetrics);
const activeDisputes = computed(() => disputeStore.activeDisputes);
const aiClosedDisputes = computed(() => disputeStore.aiResolvedDisputes);

// Initialize store data on component mount
onMounted(async () => {
  await Promise.all([
    disputeStore.fetchActiveDisputes(),
    disputeStore.fetchAiResolvedDisputes(),
    disputeStore.fetchMetrics(),
  ]);
});

// Computed properties for filtering
const filteredActiveDisputes = computed(() => {
  return activeDisputes.value.filter((dispute) => {
    return (
      dispute.type
        .toLowerCase()
        .includes(activeSearchQuery.value.toLowerCase()) ||
      dispute.description
        .toLowerCase()
        .includes(activeSearchQuery.value.toLowerCase())
    );
  });
});

const filteredAiDisputes = computed(() => {
  return aiClosedDisputes.value.filter((dispute) => {
    return (
      dispute.id.toLowerCase().includes(aiSearchQuery.value.toLowerCase()) ||
      dispute.type.toLowerCase().includes(aiSearchQuery.value.toLowerCase())
    );
  });
});

// Methods
const getRiskColor = (status) => {
  switch (status) {
    case "High Risk":
      return colors.primary;
    case "Medium Risk":
      return colors.warning;
    case "Low Risk":
      return colors.success;
    default:
      return colors.secondary;
  }
};

// API calls
const fetchActiveDisputes = async () => {
  try {
    const response = await fetch("http://localhost:8000/disputes/active");
    const data = await response.json();
    activeDisputes.value = data;
  } catch (error) {
    console.error("Error fetching active disputes:", error);
  }
};

const fetchAiDisputes = async () => {
  try {
    const response = await fetch("http://localhost:8000/disputes/ai-resolved");
    const data = await response.json();
    aiClosedDisputes.value = data;
  } catch (error) {
    console.error("Error fetching AI-resolved disputes:", error);
  }
};

const fetchMetrics = async () => {
  try {
    const [activeResponse, aiResponse] = await Promise.all([
      fetch("http://localhost:8000/disputes/active-metrics"),
      fetch("http://localhost:8000/disputes/ai-metrics"),
    ]);

    const activeData = await activeResponse.json();
    const aiData = await aiResponse.json();

    activeMetrics.value = activeData;
    aiMetrics.value = aiData;
  } catch (error) {
    console.error("Error fetching metrics:", error);
  }
};

const navigateToDispute = (id, isAiDispute) => {
  if (isAiDispute) {
    router.push({
      name: "AIDisputeDetails",
      params: { id: id.toString() },
    });
  } else {
    router.push({
      name: "DisputeDetails",
      params: { id: id.toString() },
    });
  }
};

// Fetch data on mount
onMounted(async () => {
  await Promise.all([
    disputeStore.fetchActiveDisputes(),
    disputeStore.fetchAiResolvedDisputes(),
    disputeStore.fetchMetrics(),
  ]);
});
</script>

<style>
/* Import Deriv's IBM Plex Sans font */
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap");

/* Main container */
.dispute-dashboard {
  font-family: "IBM Plex Sans", sans-serif;
  background-color: v-bind("colors.background");
  min-height: 100vh;
  padding: 20px;
}

/* Tabs styling */
.custom-tabs {
  background-color: v-bind("colors.cardBg");
  border-radius: 8px;
}

.custom-tab {
  color: v-bind("colors.text") !important;
  font-weight: 500;
  text-transform: none;
}

/* Card styling */
.metric-card {
  background-color: v-bind("colors.cardBg") !important;
  border: 1px solid v-bind("colors.border");
  border-radius: 8px;
  transition: transform 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-title {
  color: v-bind("colors.text");
  font-weight: 500;
  opacity: 0.8;
}

.metric-value {
  color: v-bind("colors.text");
  font-weight: 600;
}

/* Disputes card specific styling */
.disputes-card {
  background-color: v-bind("colors.cardBg") !important;
  border: 1px solid v-bind("colors.border");
  border-radius: 8px;
}

.card-header {
  background-color: v-bind("colors.cardBg");
  border-bottom: 1px solid v-bind("colors.border");
  color: v-bind("colors.text");
}

/* Search field styling */
.search-field {
  max-width: 250px;
  background-color: v-bind("colors.background");
}

.search-field :deep(.v-field) {
  background-color: v-bind("colors.background") !important;
  border-color: v-bind("colors.border") !important;
}

/* Dispute list styling */
.dispute-list {
  background-color: transparent;
}

.dispute-item {
  background-color: v-bind("colors.background") !important;
  border: 1px solid v-bind("colors.border") !important;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.dispute-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dispute-title {
  color: v-bind("colors.text");
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 4px;
}

/* Text styling */
.label-text {
  color: v-bind("colors.text");
  opacity: 0.7;
}

.value-text {
  color: v-bind("colors.text");
  font-weight: 600;
  font-size: 1rem;
}

.patterns-text {
  color: v-bind("colors.text");
  opacity: 0.9;
  font-size: 0.875rem;
}

/* Vuetify component overrides */
.v-btn {
  text-transform: none;
  font-weight: 500;
}

.v-chip {
  font-weight: 500;
}

/* Utility classes */
.w-100 {
  width: 100%;
}

.font-weight-bold {
  font-weight: 600 !important;
}

.text-subtitle-2 {
  color: v-bind("colors.text");
  opacity: 0.8;
  font-weight: 500;
}

.gap-2 {
  gap: 8px;
}
</style>
