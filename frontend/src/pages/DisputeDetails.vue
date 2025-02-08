<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useDisputeStore } from "@/stores/disputes.js";
import EvidenceUploader from "@/components/EvidenceUploader.vue";

const router = useRouter();
const route = useRoute();
const disputeStore = useDisputeStore();

// Reactive references
const loading = ref(false);
const error = ref(null);
const activeTab = ref(0);
const evidenceDialog = ref(false);
const selectedEvidence = ref(null);
const resolutionNotes = ref("");
const selectedAction = ref(null);
const aiFindings = ref([]);
const riskScore = ref(0);
const riskFactors = ref([]);
const form = ref(null);

// Computed properties
const dispute = computed(() => {
  return (
    disputeStore.activeDispute || {
      id: "",
      type: "",
      amount: 0,
      status: "",
      createdAt: "",
      timeRemaining: "",
      riskScore: 0,
      buyer: {
        username: "",
        riskScore: "",
        verifiedStatus: false,
        accountAge: "",
        previousDisputes: 0,
      },
      seller: {
        username: "",
        riskScore: "",
        verifiedStatus: false,
        accountAge: "",
        previousDisputes: 0,
      },
      evidence: {},
      isAIHandled: false,
    }
  );
});

const hasSubmittedEvidence = computed(() => {
  return (
    dispute.value?.evidence && Object.keys(dispute.value.evidence).length > 0
  );
});

const isResolutionValid = computed(() => {
  return selectedAction.value && resolutionNotes.value.length > 0;
});

const documentMetrics = computed(() => ({
  "Document Authenticity":
    dispute.value?.evidence?.bank_statement?.authenticity_score || 0,
  "Metadata Validity": dispute.value?.evidence?.bank_statement?.metadata_valid
    ? 100
    : 0,
  "Content Match": dispute.value?.evidence?.bank_statement?.content_match
    ? 100
    : 0,
}));

const videoMetrics = computed(() => ({
  "Video Authenticity":
    dispute.value?.evidence?.video_evidence?.authenticity_score || 0,
  "Interface Validation": dispute.value?.evidence?.video_evidence
    ?.interface_valid
    ? 100
    : 0,
  "Timeline Consistency": dispute.value?.evidence?.video_evidence
    ?.manipulation_detected
    ? 0
    : 100,
}));

// Methods
const getRiskColor = (status) => {
  switch (status) {
    case "High Risk":
      return "error";
    case "Medium Risk":
      return "warning";
    case "Low Risk":
      return "success";
    default:
      return "grey";
  }
};

const getMetricColor = (value) => {
  if (value >= 90) return "success";
  if (value >= 70) return "warning";
  return "error";
};

const getEvidenceStatusColor = (score) => {
  if (score >= 90) return "success";
  if (score >= 70) return "warning";
  return "error";
};

const viewEvidence = (evidence) => {
  selectedEvidence.value = evidence;
  evidenceDialog.value = true;
};

const handleEvidenceAnalysis = (results) => {
  aiFindings.value = [
    {
      type:
        results.pdf_analysis.authenticity_score > 70 ? "success" : "warning",
      message: `Bank Statement Analysis: ${results.pdf_analysis.authenticity_score}% authentic`,
    },
    {
      type:
        results.video_analysis.authenticity_score > 70 ? "success" : "warning",
      message: `Video Evidence Analysis: ${results.video_analysis.authenticity_score}% authentic`,
    },
  ];

  riskScore.value = results.risk_assessment.risk_score;
  riskFactors.value = [
    ...results.pdf_analysis.suspicious_patterns,
    ...results.video_analysis.risk_factors,
  ];
};

const submitResolution = async () => {
  if (!isResolutionValid.value) return;

  loading.value = true;
  try {
    await disputeStore.submitResolution({
      disputeId: dispute.value.id,
      action: selectedAction.value,
      notes: resolutionNotes.value,
      aiAnalysis: {
        riskScore: riskScore.value,
        findings: aiFindings.value,
      },
    });
    router.push("/disputes");
  } catch (error) {
    console.error("Error submitting resolution:", error);
  } finally {
    loading.value = false;
  }
};

// Lifecycle hooks
onMounted(async () => {
  loading.value = true;
  try {
    await disputeStore.fetchDisputeDetails(route.params.id);
    if (hasSubmittedEvidence.value) {
      const analysis = await disputeStore.getDisputeAnalysis(route.params.id);
      handleEvidenceAnalysis(analysis);
    }
  } catch (err) {
    error.value = "Failed to load dispute details";
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <v-container>
    <!-- Loading State -->
    <v-overlay :model-value="loading">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>

    <!-- Error State -->
    <v-alert v-if="error" type="error" dismissible @click:close="error = null">
      {{ error }}
    </v-alert>

    <!-- Content -->
    <template v-if="!loading && !error">
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
                Dispute #{{ dispute.id }}
                <v-chip :color="getRiskColor(dispute.status)" dark class="ml-4">
                  {{ dispute.status }}
                </v-chip>
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
                  <div class="caption">Time Remaining</div>
                  <div class="body-1">{{ dispute.timeRemaining }}</div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Evidence Upload Section -->
          <v-card v-if="!hasSubmittedEvidence" class="mb-6">
            <v-card-title>Submit Evidence</v-card-title>
            <v-card-text>
              <evidence-uploader
                :dispute-id="dispute.id"
                @evidence-analyzed="handleEvidenceAnalysis"
              />
            </v-card-text>
          </v-card>

          <!-- Parties Information -->
          <v-row>
            <!-- Buyer Information -->
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>
                  Buyer Information
                  <v-chip
                    :color="getRiskColor(dispute.buyer.riskScore)"
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
                        <v-list-item-subtitle>
                          {{ dispute.buyer.accountAge }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Previous Disputes</v-list-item-title>
                        <v-list-item-subtitle>
                          {{ dispute.buyer.previousDisputes }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Seller Information -->
            <v-col cols="12" md="6">
              <v-card>
                <v-card-title>
                  Seller Information
                  <v-chip
                    :color="getRiskColor(dispute.seller.riskScore)"
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
                        <v-list-item-subtitle>
                          {{ dispute.seller.accountAge }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Previous Disputes</v-list-item-title>
                        <v-list-item-subtitle>
                          {{ dispute.seller.previousDisputes }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Evidence & Analysis Section -->
          <v-card class="mt-6">
            <v-card-title>Evidence & Analysis</v-card-title>
            <v-card-text>
              <v-tabs v-model="activeTab">
                <v-tab>Submitted Evidence</v-tab>
                <v-tab>AI Analysis</v-tab>
                <v-tab>Risk Assessment</v-tab>
                <v-tab>Transaction History</v-tab>
              </v-tabs>

              <v-window v-model="activeTab">
                <!-- Submitted Evidence Tab -->
                <v-window-item>
                  <v-list>
                    <v-list-item
                      v-for="evidence in dispute.evidence"
                      :key="evidence.id"
                    >
                      <v-list-item-content>
                        <v-list-item-title>{{
                          evidence.type
                        }}</v-list-item-title>
                        <v-list-item-subtitle>
                          Submitted: {{ evidence.submittedAt }}
                        </v-list-item-subtitle>
                        <v-chip
                          :color="
                            getEvidenceStatusColor(evidence.authenticity_score)
                          "
                          small
                          class="mt-2"
                        >
                          {{ evidence.authenticity_score }}% Authentic
                        </v-chip>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn
                          text
                          color="primary"
                          @click="viewEvidence(evidence)"
                        >
                          View Evidence
                        </v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list>
                </v-window-item>

                <!-- AI Analysis Tab -->
                <v-window-item>
                  <v-card flat>
                    <v-card-text>
                      <v-alert
                        v-for="(finding, index) in aiFindings"
                        :key="index"
                        :type="finding.type"
                        border="left"
                        class="mb-4"
                      >
                        {{ finding.message }}
                      </v-alert>

                      <!-- AI Confidence Metrics -->
                      <v-row class="mt-4">
                        <v-col cols="12" md="6">
                          <v-card outlined>
                            <v-card-title>Document Analysis</v-card-title>
                            <v-card-text>
                              <v-list dense>
                                <v-list-item
                                  v-for="(score, key) in documentMetrics"
                                  :key="key"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>{{
                                      key
                                    }}</v-list-item-title>
                                    <v-progress-linear
                                      :model-value="score"
                                      :color="getMetricColor(score)"
                                      height="25"
                                    >
                                      <template v-slot:default="{ value }">
                                        <strong>{{ Math.ceil(value) }}%</strong>
                                      </template>
                                    </v-progress-linear>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </v-card-text>
                          </v-card>
                        </v-col>

                        <v-col cols="12" md="6">
                          <v-card outlined>
                            <v-card-title>Video Analysis</v-card-title>
                            <v-card-text>
                              <v-list dense>
                                <v-list-item
                                  v-for="(score, key) in videoMetrics"
                                  :key="key"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>{{
                                      key
                                    }}</v-list-item-title>
                                    <v-progress-linear
                                      :model-value="score"
                                      :color="getMetricColor(score)"
                                      height="25"
                                    >
                                      <template v-slot:default="{ value }">
                                        <strong>{{ Math.ceil(value) }}%</strong>
                                      </template>
                                    </v-progress-linear>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-window-item>

                <!-- Risk Assessment Tab -->
                <v-window-item>
                  <v-card flat>
                    <v-card-text>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-card outlined>
                            <v-card-title>Overall Risk Score</v-card-title>
                            <v-card-text class="text-center">
                              <v-progress-circular
                                :rotate="-90"
                                :size="100"
                                :width="15"
                                :model-value="dispute.riskScore"
                                :color="getRiskColor(dispute.status)"
                              >
                                {{ dispute.riskScore }}%
                              </v-progress-circular>
                              <div class="mt-4">
                                <v-chip :color="getRiskColor(dispute.status)">
                                  {{ dispute.status }}
                                </v-chip>
                              </div>
                            </v-card-text>
                          </v-card>
                        </v-col>

                        <v-col cols="12" md="6">
                          <v-card outlined>
                            <v-card-title>Risk Factors</v-card-title>
                            <v-card-text>
                              <v-list dense>
                                <v-list-item
                                  v-for="(factor, index) in riskFactors"
                                  :key="index"
                                >
                                  <v-list-item-icon>
                                    <v-icon color="error"
                                      >mdi-alert-circle</v-icon
                                    >
                                  </v-list-item-icon>
                                  <v-list-item-content>
                                    <v-list-item-title>{{
                                      factor
                                    }}</v-list-item-title>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-window-item>

                <!-- Transaction History Tab -->
                <v-window-item>
                  <v-timeline dense>
                    <v-timeline-item
                      v-for="(event, index) in dispute.timeline"
                      :key="index"
                      :color="event.color || 'primary'"
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
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>

          <!-- Action Panel -->
          <v-card v-if="!dispute.isAIHandled" class="mt-6">
            <v-card-title>Resolution Actions</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" md="8">
                  <v-textarea
                    v-model="resolutionNotes"
                    label="Resolution Notes"
                    outlined
                  ></v-textarea>
                </v-col>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="selectedAction"
                    :items="['Approve', 'Reject', 'Escalate']"
                    label="Select Action"
                    outlined
                  ></v-select>
                  <v-btn
                    color="primary"
                    block
                    class="mt-4"
                    @click="submitResolution"
                    :disabled="!isResolutionValid"
                    :loading="loading"
                  >
                    Submit Resolution
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

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
              <v-chip
                :color="
                  getEvidenceStatusColor(selectedEvidence.authenticity_score)
                "
                class="mr-2"
              >
                Authenticity Score: {{ selectedEvidence.authenticity_score }}%
              </v-chip>
            </div>

            <!-- PDF Viewer -->
            <iframe
              v-if="selectedEvidence.type === 'pdf'"
              :src="selectedEvidence.url"
              width="100%"
              height="600"
              class="evidence-viewer"
            ></iframe>

            <!-- Video Player -->
            <video
              v-else-if="selectedEvidence.type === 'video'"
              controls
              width="100%"
              class="evidence-viewer"
            >
              <source
                :src="selectedEvidence.url"
                :type="selectedEvidence.mimeType"
              />
              Your browser does not support the video tag.
            </video>
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

.evidence-viewer {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.v-chip {
  margin-right: 8px;
}
</style>
