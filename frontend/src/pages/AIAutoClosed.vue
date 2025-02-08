<!-- src/views/AIDisputeDetails.vue -->
<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useDisputeStore } from "@/stores/disputes.js";

const route = useRoute();
const disputeStore = useDisputeStore();
const router = useRouter();
const activeTab = ref(0);
const evidenceDialog = ref(false);
const selectedEvidence = ref(null);

// Mock data for AI-handled dispute
const dispute = computed(() => {
  return disputeStore.getAiResolvedDisputeById(route.params.id);
});

// Methods
const getConfidenceColor = (confidence) => {
  if (confidence >= 95) return "green";
  if (confidence >= 85) return "orange";
  return "red";
};

const viewEvidence = (evidence) => {
  selectedEvidence.value = evidence;
  evidenceDialog.value = true;
};

const fetchAIDisputeDetails = async () => {
  try {
    // Simulated API call
    console.log("Fetching AI dispute details...");
  } catch (error) {
    console.error("Error fetching AI dispute details:", error);
  }
};

// Computed properties
const resolutionTime = computed(() => {
  const start = new Date(dispute.value.createdAt);
  const end = new Date(dispute.value.resolvedAt);
  return ((end - start) / 1000).toFixed(1) + " seconds";
});

onMounted(() => {
  fetchAIDisputeDetails();
});
</script>

<template>
  <v-container>
    <v-row>
      <!-- Back Button -->
      <v-col cols="12">
        <v-btn @click="router.go(-1)" text>
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Dashboard
        </v-btn>
      </v-col>

      <!-- Dispute Header -->
      <v-col cols="12">
        <v-card class="mb-6">
          <v-card-title class="d-flex justify-space-between">
            <div>
              AI Dispute #{{ dispute.id }}
              <v-chip color="purple" dark class="ml-4"> AI Resolved </v-chip>
              <v-chip color="green" dark class="ml-2">
                {{ dispute.resolution }}
              </v-chip>
            </div>
            <div>
              <span class="text-subtitle-2"
                >Resolution Time: {{ resolutionTime }}</span
              >
            </div>
          </v-card-title>

          <v-card-text>
            <v-row>
              <v-col cols="12" md="3">
                <div class="caption">Pattern Match</div>
                <div class="body-1">{{ dispute.patternMatch }}</div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="caption">Amount</div>
                <div class="body-1">${{ dispute.amount }}</div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="caption">AI Confidence</div>
                <div class="body-1">{{ dispute.resolutionConfidence }}%</div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="caption">Resolution Date</div>
                <div class="body-1">{{ dispute.resolvedAt }}</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Parties Information -->
        <v-row>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>
                Buyer Information
                <v-chip
                  :color="dispute.buyer.riskScore === 'Low' ? 'green' : 'red'"
                  small
                  class="ml-2"
                >
                  {{ dispute.buyer.riskScore }} Risk
                </v-chip>
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Username</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ dispute.buyer.username }}
                        <v-icon
                          v-if="dispute.buyer.verifiedStatus"
                          small
                          color="green"
                        >
                          mdi-check-circle
                        </v-icon>
                      </v-list-item-subtitle>
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
            <v-card>
              <v-card-title>
                Seller Information
                <v-chip
                  :color="dispute.seller.riskScore === 'Low' ? 'green' : 'red'"
                  small
                  class="ml-2"
                >
                  {{ dispute.seller.riskScore }} Risk
                </v-chip>
              </v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Username</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ dispute.seller.username }}
                        <v-icon
                          v-if="dispute.seller.verifiedStatus"
                          small
                          color="green"
                        >
                          mdi-check-circle
                        </v-icon>
                      </v-list-item-subtitle>
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

        <!-- AI Analysis Sections -->
        <v-card class="mt-6">
          <v-card-title>AI Analysis & Resolution</v-card-title>
          <v-card-text>
            <v-tabs v-model="activeTab">
              <v-tab>Resolution Steps</v-tab>
              <v-tab>AI Findings</v-tab>
              <v-tab>Evidence Analysis</v-tab>
              <v-tab>Timeline</v-tab>
            </v-tabs>

            <v-tabs-items v-model="activeTab">
              <!-- Resolution Steps -->
              <v-tab-item>
                <v-timeline dense>
                  <v-timeline-item
                    v-for="step in resolutionSteps"
                    :key="step.id"
                    :color="getConfidenceColor(step.confidence)"
                    small
                  >
                    <div class="font-weight-normal">
                      <strong>{{ step.step }}</strong>
                      <v-chip
                        x-small
                        :color="getConfidenceColor(step.confidence)"
                        class="ml-2"
                      >
                        {{ step.confidence }}% confidence
                      </v-chip>
                      <div class="text-caption">
                        {{ step.timestamp }}
                      </div>
                    </div>
                    <div>{{ step.details }}</div>
                  </v-timeline-item>
                </v-timeline>
              </v-tab-item>

              <!-- AI Findings -->
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <v-alert
                      v-for="(alert, index) in aiAnalysis"
                      :key="index"
                      :type="alert.type"
                      border="left"
                      class="mb-4"
                    >
                      <div class="d-flex justify-space-between align-center">
                        <div>
                          <div>{{ alert.message }}</div>
                          <div class="caption">
                            Rule ID: {{ alert.matchedRule }}
                          </div>
                        </div>
                        <v-chip
                          x-small
                          :color="getConfidenceColor(alert.confidence)"
                        >
                          {{ alert.confidence }}% confidence
                        </v-chip>
                      </div>
                    </v-alert>
                  </v-card-text>
                </v-card>
              </v-tab-item>

              <!-- Evidence Analysis -->
              <v-tab-item>
                <v-list>
                  <v-list-item
                    v-for="evidence in dispute.evidence"
                    :key="evidence.id"
                  >
                    <v-list-item-content>
                      <v-list-item-title>{{ evidence.type }}</v-list-item-title>
                      <v-list-item-subtitle>
                        Submitted: {{ evidence.submittedAt }}
                      </v-list-item-subtitle>
                      <v-list-item-subtitle>
                        Verification: {{ evidence.verificationDetails }}
                      </v-list-item-subtitle>
                      <v-btn
                        text
                        color="primary"
                        @click="viewEvidence(evidence)"
                      >
                        View Evidence
                      </v-btn>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-chip
                        :color="evidence.verified ? 'green' : 'red'"
                        small
                      >
                        {{ evidence.verified ? "Verified" : "Invalid" }}
                      </v-chip>
                    </v-list-item-action>
                  </v-list-item>
                </v-list>
              </v-tab-item>

              <!-- Timeline -->
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
                      <div class="text-caption">
                        {{ event.timestamp }}
                      </div>
                    </div>
                    <div>{{ event.description }}</div>
                  </v-timeline-item>
                </v-timeline>
              </v-tab-item>
            </v-tabs-items>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Evidence Viewer Dialog -->
    <v-dialog v-model="evidenceDialog" max-width="800px">
      <v-card>
        <v-card-title>
          Evidence Viewer
          <v-spacer></v-spacer>
          <v-btn icon @click="evidenceDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <div v-if="selectedEvidence">
            <div class="mb-4">
              <strong>Verification Details:</strong>
              <p>{{ selectedEvidence.verificationDetails }}</p>
            </div>
            <iframe
              v-if="selectedEvidence.type.includes('pdf')"
              :src="selectedEvidence.url"
              width="100%"
              height="600"
            ></iframe>
            <img
              v-else-if="selectedEvidence.type.includes('Screenshot')"
              :src="selectedEvidence.url"
              width="100%"
              alt="Evidence"
            />
            <div v-else class="pa-4 text-center grey lighten-3">
              <v-icon large>mdi-file-document-outline</v-icon>
              <div class="mt-2">{{ selectedEvidence.type }}</div>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.caption {
  color: rgba(0, 0, 0, 0.6);
  font-size: 0.75rem;
  font-weight: 400;
}

.body-1 {
  font-size: 1rem;
  font-weight: 400;
  margin-top: 4px;
}

.v-timeline-item {
  margin-bottom: 12px;
}

.v-chip {
  margin-right: 8px;
}

.confidence-indicator {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
}
</style>
