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
  default = "fastapi-cloud-run"
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
          value = "AIzaSyDV-VXtQIPXmZV6F8VXiuYHkunMGBvKyIE"
        }
        env {
          name  = "OPENAI_API_KEY"
          value = "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"
        }
        env {
          name  = "CSE_ID"
          value = "34b4b9e66f9e74ad2"
        }
        env {
          name  = "MONGO_URI"
          value = "mongodb+srv://sujay1844:p1cFYY9OP6062xDw@serverlessinstance0.ycj0ic4.mongodb.net/?retryWrites=true&w=majority"
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
