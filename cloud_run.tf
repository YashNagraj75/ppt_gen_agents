terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "edunova-455712"
  region  = "asia-south1"
}

variable "project_id" {
  default = "edunova-455712"
}

variable "region" {
  default = "asia-south1"
}

variable "api_image_url" {
  default = "asia-south1-docker.pkg.dev/edunova-455712/ppt-gen-agents/api:latest"
}

variable "service_name" {
  default = "ppt-gen-agents"
}

resource "google_cloud_run_service" "default" {
  name     = var.service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.api_image_url
        ports {
          container_port = 8080
        }
        env {
          name  = "GEMINI_API_KEY"
          value = var.GEMINI_API_KEY } 
        env {
          name  = "OPENAI_API_KEY"
          value = var.OPENAI_API_KEY
        }
        env {
          name  = "CSE_ID"
          value = var.CSE_ID
        }
        env {
          name  = "MONGO_URI"
          value = var.MONGO_URI
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "member" {
  location = google_cloud_run_service.default.location
  project = google_cloud_run_service.default.project
  service = google_cloud_run_service.default.name
  role = "roles/run.invoker"
  member = "allUsers"
}
