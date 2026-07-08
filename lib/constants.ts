export const CATEGORIES = [
  "Water",
  "Roads",
  "Drainage",
  "Streetlights",
  "Pension",
  "Health",
  "Education",
  "Sanitation",
  "Electricity",
  "Other",
] as const;
export type Category = (typeof CATEGORIES)[number];

export const URGENCY = ["Low", "Medium", "High", "Critical"] as const;
export type Urgency = (typeof URGENCY)[number];

export const SUBMISSION_SOURCES = [
  "citizen_chat",
  "staff_entry",
  "csv_upload",
  "field_report",
] as const;

export const SUBMISSION_STATUS = [
  "submitted",
  "under_review",
  "attached_to_cluster",
  "closed",
] as const;

export const CLUSTER_STATUS = [
  "new",
  "verified",
  "forwarded",
  "in_progress",
  "resolved",
  "closed",
] as const;

export const VERIFICATION_STATUS = [
  "unverified",
  "staff_verified",
  "disputed",
] as const;

export const LOCATION_TYPES = [
  "locality",
  "ward",
  "village",
  "mandal",
  "constituency",
  "district",
] as const;

export const GUIDANCE_TYPES = [
  "scheme",
  "complaint_channel",
  "department",
  "local_service",
  "helpline",
  "grievance_portal",
] as const;

export const USER_ROLES = ["citizen", "mp", "staff", "admin"] as const;

/**
 * Section 24.2 - submissions mentioning these should be auto-flagged to staff
 * review and never auto-published.
 */
export const SENSITIVE_KEYWORDS = [
  "violence",
  "assault",
  "abuse",
  "harassment",
  "rape",
  "molest",
  "suicide",
  "self-harm",
  "self harm",
  "kill",
  "murder",
  "child safety",
  "kidnap",
  "corruption",
  "bribe",
  "criminal",
  "weapon",
  "bomb",
  "threat",
  "defamation",
  "aadhaar",
];

export const URGENCY_WEIGHT: Record<Urgency, number> = {
  Low: 0.25,
  Medium: 0.5,
  High: 0.8,
  Critical: 1,
};

export const VULNERABLE_GROUP_KEYWORDS = [
  "elderly",
  "old age",
  "senior",
  "pension",
  "children",
  "child",
  "student",
  "school",
  "disabled",
  "disability",
  "handicap",
  "widow",
  "low income",
  "poor",
  "bpl",
];

export const DEFAULT_CONSTITUENCY = {
  area_id: "CONST_001",
  name: "Visakhapatnam",
  state: "Andhra Pradesh",
  district: "Visakhapatnam",
};
