<!-- src/views/DisputeDashboard.vue -->
<template>
  <v-container fluid class="dispute-dashboard">
    <v-alert v-if="error" type="error" dismissible @click:close="error = null">
      {{ error }}
    </v-alert>

    <!-- Tabs -->
    <v-tabs
      v-model="activeTab"
      :color="colors.primary"
      class="mb-6 custom-tabs"
    >
      <v-tab value="active" class="custom-tab">Active Disputes</v-tab>
      <v-tab value="ai-closed" class="custom-tab">AI-Resolved Disputes</v-tab>
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
        <!-- Summary Cards for AI-Resolved Disputes -->
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
const error = ref(null);

// Color palette
const colors = {
  primary: "#ff444f",
  secondary: "#85acb0",
  background: "#151b28",
  cardBg: "#1c2331",
  text: "#e6e9ed",
  success: "#4bb4b3",
  warning: "#ffad3a",
  info: "#377cfc",
  border: "#2a3245",
};

// Shared state
const activeTab = ref("active");
const activeSearchQuery = ref("");
const aiSearchQuery = ref("");

// Metrics for Active Disputes
const activeMetrics = ref([
  {
    title: "Active Disputes",
    value: "24",
    icon: "mdi-alert-circle",
    color: colors.primary,
  },
  {
    title: "Avg Resolution Time",
    value: "1.5h",
    icon: "mdi-clock",
    color: colors.info,
  },
  {
    title: "Resolved Today",
    value: "18",
    icon: "mdi-check-circle",
    color: colors.success,
  },
  {
    title: "Fraud Prevented",
    value: "$2.4k",
    icon: "mdi-shield",
    color: colors.info,
  },
]);

// Metrics for AI-Resolved Disputes
const aiMetrics = ref([
  {
    title: "AI Resolutions",
    value: "156",
    icon: "mdi-robot",
    color: colors.primary,
  },
  {
    title: "Avg AI Resolution Time",
    value: "45s",
    icon: "mdi-clock-fast",
    color: colors.info,
  },
  {
    title: "Success Rate",
    value: "98%",
    icon: "mdi-check-circle",
    color: colors.success,
  },
  {
    title: "Cost Saved",
    value: "$5.2k",
    icon: "mdi-cash",
    color: colors.info,
  },
]);

// Active disputes data
const activeDisputes = ref([
  {
    id: 1,
    type: "Unauthorized Transaction",
    amount: 500,
    status: "High Risk",
    timeRemaining: "1h 45m",
    riskScore: 85,
    description: "User claims transaction was not authorized",
    patterns: ["Multiple failed attempts", "New device", "Unusual amount"],
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
  },
  {
    id: 3,
    type: "Payment Error",
    amount: 100,
    status: "Low Risk",
    timeRemaining: "0h 45m",
    riskScore: 25,
    description: "Double payment reported",
    patterns: ["System lag detected", "Duplicate transaction ID"],
  },
]);

// AI-resolved disputes data
const aiClosedDisputes = ref([
  {
    id: "D123456",
    type: "Buyer Underpaid",
    amount: 500.0,
    resolution: "Auto-resolved",
    closedAt: "2023-07-20 15:30",
    aiConfidenceScore: 98,
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
  },
  {
    id: "D123457",
    type: "Buyer Overpaid",
    amount: 1200.0,
    resolution: "Auto-refunded",
    closedAt: "2023-07-20 16:45",
    aiConfidenceScore: 99,
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
  },
]);

// Computed properties
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
    router.push({ name: "AIDisputeDetails", params: { id: id.toString() } });
  } else {
    router.push({ name: "DisputeDetails", params: { id: id.toString() } });
  }
};

// Update the fetch methods to use store
onMounted(async () => {
  error.value = null;

  try {
    await disputeStore.fetchActiveDisputes();
    await disputeStore.fetchAiResolvedDisputes();
  } catch (err) {
    error.value = "Failed to load disputes. Please try again later.";
    console.error("Error loading disputes:", err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.dispute-dashboard {
  background-color: v-bind("colors.background");
  min-height: 100vh;
  padding: 20px;
}

.custom-tabs {
  background-color: v-bind("colors.cardBg");
  border-radius: 8px;
}

.custom-tab {
  color: v-bind("colors.text") !important;
  font-weight: 500;
}

.metric-card {
  background-color: v-bind("colors.cardBg") !important;
  border: 1px solid v-bind("colors.border");
  border-radius: 8px;
}

.metric-title {
  color: v-bind("colors.text");
  opacity: 0.8;
}

.metric-value {
  color: v-bind("colors.text");
  font-weight: 700;
}

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

.search-field {
  max-width: 250px;
  background-color: v-bind("colors.background");
}

.search-field :deep(.v-field) {
  background-color: v-bind("colors.background") !important;
  border-color: v-bind("colors.border") !important;
}

.dispute-list {
  background-color: transparent;
}

.dispute-item {
  background-color: v-bind("colors.background") !important;
  border: 1px solid v-bind("colors.border") !important;
}

.dispute-title {
  color: v-bind("colors.text");
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 4px;
}

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
