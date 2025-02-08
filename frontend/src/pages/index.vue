<!-- src/components/DocumentUploader.vue -->
<template>
  <div class="document-uploader">
    <v-file-input
      v-model="selectedFile"
      :rules="fileRules"
      accept=".pdf,.mp4,.mov"
      label="Upload Document"
      @change="handleFileSelect"
    ></v-file-input>

    <v-btn
      :loading="uploading"
      :disabled="!selectedFile"
      color="primary"
      @click="uploadDocument"
    >
      Upload
    </v-btn>

    <!-- Document List -->
    <v-list v-if="documents.length">
      <v-list-item v-for="doc in documents" :key="doc.id">
        <v-list-item-content>
          <v-list-item-title>{{ doc.original_filename }}</v-list-item-title>
          <v-list-item-subtitle>
            Type: {{ doc.file_type }} | Uploaded:
            {{ formatDate(doc.upload_date) }}
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon @click="downloadDocument(doc.id)">
            <v-icon>mdi-download</v-icon>
          </v-btn>
          <v-btn icon @click="deleteDocument(doc.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      uploading: false,
      documents: [],
      fileRules: [
        (v) =>
          !v || v.size < 50000000 || "File size should be less than 50 MB!",
        (v) => !v || /\.(pdf|mp4|mov)$/i.test(v.name) || "Invalid file type!",
      ],
    };
  },

  mounted() {
    this.loadDocuments();
  },

  methods: {
    async uploadDocument() {
      if (!this.selectedFile) return;

      this.uploading = true;
      const formData = new FormData();
      formData.append("file", this.selectedFile);
      formData.append("user_id", 1); // Replace with actual user ID

      try {
        const response = await fetch(
          "http://localhost:8000/api/upload/document",
          {
            method: "POST",
            body: formData,
          }
        );

        if (response.ok) {
          const result = await response.json();
          this.$emit("upload-success", result);
          this.loadDocuments();
        } else {
          throw new Error("Upload failed");
        }
      } catch (error) {
        console.error("Upload error:", error);
        this.$emit("upload-error", error);
      } finally {
        this.uploading = false;
        this.selectedFile = null;
      }
    },

    async loadDocuments() {
      try {
        const response = await fetch("http://localhost:8000/api/documents/1"); // Replace with actual user ID
        if (response.ok) {
          this.documents = await response.json();
        }
      } catch (error) {
        console.error("Error loading documents:", error);
      }
    },

    async downloadDocument(documentId) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/document/${documentId}`
        );
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = this.documents.find(
            (d) => d.id === documentId
          ).original_filename;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          a.remove();
        }
      } catch (error) {
        console.error("Error downloading document:", error);
      }
    },

    async deleteDocument(documentId) {
      if (!confirm("Are you sure you want to delete this document?")) return;

      try {
        const response = await fetch(
          `http://localhost:8000/api/document/${documentId}`,
          {
            method: "DELETE",
          }
        );
        if (response.ok) {
          this.loadDocuments();
        }
      } catch (error) {
        console.error("Error deleting document:", error);
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
  },
};
</script>
