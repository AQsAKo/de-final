variable "project_id" {
  type        = string
  default     = null
  description = "GCP project ID"
}
variable "project_name" {
  type        = string
  default     = "WMATA gtfs buses pipeline"
  description = "GCP project display name"
}
variable "region" {
  type        = string
  default     = null
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
}
variable "zone" {
  type    = string
  default = null
}
variable "credentials" {
  type = string
  sensitive = true
  description = "Google Cloud service account credentials"
}