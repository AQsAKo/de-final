terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
  //credentials = file("/mnt/c/work/data-camp/final/secrets/final-385014-62388fe84c7f.json")  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

/*resource "google_project" "final" {
  name       = var.project_name
  project_id = var.project_id
}*/

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "gtfs_static"
  friendly_name               = "gtfs_static"
  location                    = "EU"
  default_table_expiration_ms = 3600000
}
