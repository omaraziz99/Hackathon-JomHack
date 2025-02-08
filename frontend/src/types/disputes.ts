// Shared types/interfaces (can be kept in frontend/src/types/disputes.ts)

interface Dispute {
  id: string; // Unique dispute ID (e.g., "D123456")
  type: string; // Dispute type (e.g., "Unauthorized Transaction")
  amount: number; // Transaction amount
  status: string; // "High Risk" | "Medium Risk" | "Low Risk"
  createdAt: string; // ISO datetime
  resolvedAt?: string; // ISO datetime for resolved disputes
  timeRemaining: string; // Formatted time remaining
  riskScore: number; // 0-100
  resolution?: string; // For AI-resolved disputes
  resolutionConfidence?: number; // AI confidence score (0-100)

  // Parties
  buyer: {
    username: string;
    riskScore: string; // "Low" | "Medium" | "High"
    verifiedStatus: boolean;
    accountAge: string;
    previousDisputes: number;
  };

  seller: {
    username: string;
    riskScore: string;
    verifiedStatus: boolean;
    accountAge: string;
    previousDisputes: number;
  };

  // Evidence
  evidence: {
    bank_statement?: {
      authenticity_score: number;
      metadata_valid: boolean;
      content_match: boolean;
      suspicious_patterns: string[];
    };
    video_evidence?: {
      authenticity_score: number;
      interface_valid: boolean;
      interaction_natural: boolean;
      manipulation_detected: boolean;
      risk_factors: string[];
    };
  };
}
