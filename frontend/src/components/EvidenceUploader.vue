<!-- components/EvidenceUploader.vue -->
<template>
  <v-card class="evidence-uploader">
    <v-card-title>Submit Evidence</v-card-title>
    <v-card-text>
      <v-form ref="form" @submit.prevent="handleSubmit">
        <!-- Bank Statement Upload -->
        <v-file-input
          v-model="bankStatement"
          label="Bank Statement (PDF)"
          accept=".pdf"
          :rules="[(v) => !!v || 'Bank statement is required']"
          prepend-icon="mdi-file-document"
          @change="validateBankStatement"
        ></v-file-input>

        <!-- Video Evidence Upload -->
        <v-file-input
          v-model="videoEvidence"
          label="Video Evidence"
          accept="video/*"
          :rules="[(v) => !!v || 'Video evidence is required']"
          prepend-icon="mdi-video"
          @change="validateVideo"
        ></v-file-input>

        <v-btn
          :loading="loading"
          :disabled="!isValid"
          color="primary"
          @click="handleSubmit"
          block
        >
          Submit Evidence
        </v-btn>
      </v-form>

      <!-- Analysis Results -->
      <v-expand-transition>
        <div v-if="analysisResults" class="mt-4">
          <v-alert
            :type="getAlertType(analysisResults.risk_assessment.risk_score)"
            border="left"
          >
            Risk Score: {{ analysisResults.risk_assessment.risk_score }}%
          </v-alert>

          <v-list>
            <v-list-item
              v-for="(analysis, type) in getAnalysisDetails()"
              :key="type"
            >
              <v-list-item-content>
                <v-list-item-title>{{ type }}</v-list-item-title>
                <v-list-item-subtitle>
                  Authenticity Score: {{ analysis.authenticity_score }}%
                </v-list-item-subtitle>
                <v-chip
                  small
                  :color="
                    analysis.authenticity_score > 70 ? 'success' : 'error'
                  "
                  class="mt-2"
                >
                  {{
                    analysis.authenticity_score > 70 ? "Verified" : "Suspicious"
                  }}
                </v-chip>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
      </v-expand-transition>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed } from "vue";
import { useDisputeStore } from "@/stores/disputes";

const props = defineProps({
  disputeId: {
    type: String,
    required: true,
  },
});

const disputeStore = useDisputeStore();
const form = ref(null);
const bankStatement = ref(null);
const videoEvidence = ref(null);
const loading = ref(false);
const analysisResults = ref(null);

const isValid = computed(() => {
  return bankStatement.value && videoEvidence.value;
});

const validateBankStatement = (file) => {
  if (file && !file.type.includes("pdf")) {
    bankStatement.value = null;
    alert("Please upload a PDF file");
  }
};

const validateVideo = (file) => {
  if (file && !file.type.includes("video")) {
    videoEvidence.value = null;
    alert("Please upload a video file");
  }
};

const getAlertType = (score) => {
  if (score >= 75) return "error";
  if (score >= 50) return "warning";
  return "success";
};

const getAnalysisDetails = () => {
  if (!analysisResults.value) return {};
  return {
    "Bank Statement": analysisResults.value.pdf_analysis,
    "Video Evidence": analysisResults.value.video_analysis,
  };
};

const handleSubmit = async () => {
  if (!isValid.value) return;

  loading.value = true;
  try {
    analysisResults.value = await disputeStore.uploadAndAnalyzeEvidence(
      props.disputeId,
      bankStatement.value,
      videoEvidence.value
    );
  } catch (error) {
    console.error("Error uploading evidence:", error);
  } finally {
    loading.value = false;
  }
};
</script>
