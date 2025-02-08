<!-- src/views/DisputeDetails.vue -->
<template>
  <v-container fluid class="dispute-details">
    <!-- Back Button -->
    <v-row>
      <v-col cols="12">
        <v-btn @click="router.go(-1)" text :color="colors.primary">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Dashboard
        </v-btn>
      </v-col>

      <!-- Dispute Header -->
      <v-col cols="12">
        <v-card class="mb-6 header-card">
          <v-card-title class="d-flex justify-space-between">
            <div>
              Dispute #{{ dispute.id }}
              <v-chip :color="getRiskColor(dispute.status)" dark class="ml-4">
                {{ dispute.status }}
              </v-chip>
            </div>
            <div v-if="!dispute.isAIHandled">
              <v-btn :color="colors.primary" @click="handleDispute">
                Take Action
              </v-btn>
            </div>
          </v-card-title>

          <v-card-text>
            <v-row>
              <v-col cols="12" md="3">
                <div class="caption">Dispute Type</div>
                <div class="body-1">{{ dispute.type }}</div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="caption">Amount</div>
                <div class="body-1">${{ dispute.amount }}</div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="caption">Created Date</div>
                <div class="body-1">{{ dispute.createdAt }}</div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="caption">Resolution Deadline</div>
                <div class="body-1">{{ dispute.deadline }}</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Parties Information -->
        <v-row>
          <v-col cols="12" md="6">
            <v-card class="info-card">
              <v-card-title>Buyer Information</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Username</v-list-item-title>
                      <v-list-item-subtitle>{{
                        dispute.buyer.username
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Account Age</v-list-item-title>
                      <v-list-item-subtitle>{{
                        dispute.buyer.accountAge
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Previous Disputes</v-list-item-title>
                      <v-list-item-subtitle>{{
                        dispute.buyer.previousDisputes
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="info-card">
              <v-card-title>Seller Information</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Username</v-list-item-title>
                      <v-list-item-subtitle>{{
                        dispute.seller.username
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Account Age</v-list-item-title>
                      <v-list-item-subtitle>{{
                        dispute.seller.accountAge
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Previous Disputes</v-list-item-title>
                      <v-list-item-subtitle>{{
                        dispute.seller.previousDisputes
                      }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Evidence Section -->
        <v-card class="mt-6 evidence-card">
          <v-card-title>Evidence & Documentation</v-card-title>
          <v-card-text>
            <v-tabs v-model="activeTab" :color="colors.primary">
              <v-tab>Submitted Evidence</v-tab>
              <v-tab>AI Analysis</v-tab>
              <v-tab>Transaction History</v-tab>
            </v-tabs>

            <v-tabs-items v-model="activeTab">
              <v-tab-item>
                <v-list>
                  <v-list-item
                    v-for="evidence in dispute.evidence"
                    :key="evidence.id"
                    @click="openEvidenceViewer(evidence)"
                  >
                    <v-list-item-content>
                      <v-list-item-title>{{ evidence.type }}</v-list-item-title>
                      <v-list-item-subtitle>
                        Submitted: {{ evidence.submittedAt }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-chip
                        :color="
                          evidence.verified ? colors.success : colors.warning
                        "
                        small
                      >
                        {{
                          evidence.verified
                            ? "Verified"
                            : "Pending Verification"
                        }}
                      </v-chip>
                    </v-list-item-action>
                  </v-list-item>
                </v-list>
              </v-tab-item>

              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <v-alert
                      v-for="(alert, index) in aiAnalysis"
                      :key="index"
                      :type="alert.type"
                      :color="
                        alert.type === 'warning'
                          ? colors.warning
                          : colors.primary
                      "
                      border="left"
                      class="mb-4"
                    >
                      {{ alert.message }}
                    </v-alert>
                  </v-card-text>
                </v-card>
              </v-tab-item>

              <v-tab-item>
                <v-timeline dense>
                  <v-timeline-item
                    v-for="event in transactionHistory"
                    :key="event.id"
                    :color="event.color"
                    small
                  >
                    <div class="font-weight-normal">
                      <strong>{{ event.title }}</strong>
                      <div class="text-caption">{{ event.timestamp }}</div>
                    </div>
                    <div>{{ event.description }}</div>
                  </v-timeline-item>
                </v-timeline>
              </v-tab-item>
            </v-tabs-items>
          </v-card-text>
        </v-card>

        <!-- Action Panel -->
        <v-card v-if="!dispute.isAIHandled" class="mt-6 action-card">
          <v-card-title>Resolution Actions</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="8">
                <v-textarea
                  v-model="resolutionNotes"
                  label="Resolution Notes"
                  outlined
                  :color="colors.primary"
                ></v-textarea>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="selectedAction"
                  :items="resolutionActions"
                  label="Select Action"
                  outlined
                  :color="colors.primary"
                ></v-select>
                <v-btn
                  :color="colors.primary"
                  block
                  class="mt-4"
                  @click="submitResolution"
                  :disabled="!isResolutionValid"
                >
                  Submit Resolution
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Evidence Viewer Dialog -->
    <v-dialog v-model="evidenceDialog" max-width="1200px">
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          Evidence Viewer
          <v-btn icon @click="evidenceDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <div v-if="!showPendingMessage" class="evidence-viewer">
            <div class="evidence-container" v-if="hasDocumentEvidence">
              <div class="evidence-title">Document Evidence</div>
              <iframe
                :src="selectedEvidence.documentUrl"
                frameborder="0"
                class="evidence-frame"
              ></iframe>
            </div>

            <div class="evidence-container" v-if="hasVideoEvidence">
              <div class="evidence-title">Video Evidence</div>
              <video controls class="evidence-frame">
                <source :src="selectedEvidence.videoUrl" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </div>

          <div v-else class="pending-evidence">
            <v-alert type="info" prominent border="left" :color="colors.info">
              Pending: Waiting for
              {{ selectedEvidence?.pendingParty || "parties" }} to upload
              evidence.
            </v-alert>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useDisputeStore } from "@/stores/disputes.js";

const router = useRouter();
const route = useRoute();
const disputeStore = useDisputeStore();

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
// Reactive state
const evidenceDialog = ref(false);
const selectedEvidence = ref(null);
const activeTab = ref(0);
const resolutionNotes = ref("");
const selectedAction = ref(null);

// Computed properties
const hasDocumentEvidence = computed(() => {
  return selectedEvidence.value?.documentUrl;
});

const hasVideoEvidence = computed(() => {
  return selectedEvidence.value?.videoUrl;
});

const showPendingMessage = computed(() => {
  return !hasDocumentEvidence.value && !hasVideoEvidence.value;
});

const dispute = computed(() => {
  return disputeStore.getActiveDisputeById(Number(route.params.id));
});

const isResolutionValid = computed(() => {
  return selectedAction.value && resolutionNotes.value.length > 0;
});

// Data
const aiAnalysis = ref([
  {
    type: "warning",
    message:
      "Suspicious pattern detected: Transaction time differs from usual pattern",
  },
  {
    type: "error",
    message: "Document manipulation detected in submitted evidence",
  },
]);

const transactionHistory = ref([
  {
    id: 1,
    title: "Dispute Initiated",
    timestamp: "2023-07-20 14:30",
    description: "Buyer reported unauthorized transaction",
    color: colors.primary,
  },
]);

const resolutionActions = [
  "Approve Refund",
  "Reject Dispute",
  "Request Additional Evidence",
  "Escalate to Supervisor",
];

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

const openEvidenceViewer = (evidence) => {
  selectedEvidence.value = evidence;
  evidenceDialog.value = true;
};

const handleDispute = async () => {
  try {
    console.log("Handling dispute...");
  } catch (error) {
    console.error("Error handling dispute:", error);
  }
};

const submitResolution = async () => {
  try {
    if (!selectedAction.value) {
      throw new Error("Please select an action");
    }

    const resolution = {
      disputeId: dispute.value.id,
      action: selectedAction.value,
      notes: resolutionNotes.value,
    };

    console.log("Submitting resolution:", resolution);
    selectedAction.value = null;
    resolutionNotes.value = "";
  } catch (error) {
    console.error("Error submitting resolution:", error);
  }
};

const fetchDisputeDetails = async () => {
  try {
    console.log("Fetching dispute details...");
  } catch (error) {
    console.error("Error fetching dispute details:", error);
  }
};

onMounted(() => {
  fetchDisputeDetails();
});
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap");

.dispute-details {
  font-family: "IBM Plex Sans", sans-serif;
  background-color: v-bind("colors.background");
  min-height: 100vh;
  padding: 20px;
}

/* Updated card styling to match Dashboard */
.header-card,
.info-card,
.evidence-card,
.action-card {
  background-color: v-bind("colors.cardBg") !important;
  border: 1px solid v-bind("colors.border");
  border-radius: 8px;
  margin-bottom: 16px;
  transition: transform 0.2s;
}

.header-card:hover,
.info-card:hover,
.evidence-card:hover,
.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Updated text styling */
.caption {
  color: v-bind("colors.text");
  opacity: 0.7;
  font-size: 0.75rem;
  font-weight: 500;
}

.body-1 {
  color: v-bind("colors.text");
  font-size: 1rem;
  font-weight: 500;
  margin-top: 4px;
}

/* Buyer/Seller Information Cards */
.v-list {
  background-color: transparent !important;
  color: v-bind("colors.text") !important;
}

.v-list-item {
  background-color: v-bind("colors.background") !important;
  border: 1px solid v-bind("colors.border");
  border-radius: 8px !important;
  margin-bottom: 8px;
  transition: transform 0.2s;
}

.v-list-item:hover {
  transform: translateY(-2px);
  background-color: v-bind("colors.cardBg") !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Evidence viewer styling */
.evidence-viewer {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  margin: 16px 0;
  background-color: v-bind("colors.background");
}

.evidence-container {
  flex: 1;
  min-width: 0;
}

.evidence-title {
  font-weight: 600;
  margin-bottom: 8px;
  color: v-bind("colors.text");
}

.evidence-frame {
  width: 100%;
  height: 600px;
  border: 1px solid v-bind("colors.border");
  border-radius: 8px;
  background-color: v-bind("colors.background");
}

/* Updated Vuetify component overrides */
.v-card-title {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
  color: v-bind("colors.text") !important;
}

.v-alert__content {
  color: v-bind("colors.text") !important;
  font-weight: 500;
}

.v-timeline-item__body {
  color: v-bind("colors.text") !important;
  font-weight: 500;
}

.v-timeline-item .text-caption {
  color: v-bind("colors.text") !important;
  opacity: 0.7;
}

.v-timeline-item .font-weight-normal strong {
  color: v-bind("colors.text") !important;
  font-weight: 600;
}

.v-card-text .v-label {
  color: v-bind("colors.text") !important;
  font-weight: 500;
}

.v-select__selection {
  color: v-bind("colors.text") !important;
  font-weight: 500;
}

/* Utility classes */
.w-100 {
  width: 100% !important;
}

.font-weight-bold {
  font-weight: 600 !important;
}

.gap-2 {
  gap: 8px !important;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .dispute-details {
    padding: 16px;
  }

  .evidence-viewer {
    flex-direction: column;
  }

  .evidence-frame {
    height: 400px;
  }
}

@media (max-width: 600px) {
  .v-card-title {
    font-size: 1.1rem !important;
  }

  .evidence-frame {
    height: 300px;
  }
}
</style>
