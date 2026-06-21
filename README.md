# ppt_gen_agents

An agentic pipeline that automatically generates structured PowerPoint-ready slide data from educational syllabus content. The system uses a multi-agent architecture built on the OpenAI Agents SDK, with Google Gemini models served through Vertex AI, and stores all intermediate and final output in MongoDB.

---

## What it does

Given a document ID that references a course/unit structure in MongoDB, the system:

1. Reads the units and topics for the course from MongoDB.
2. Fetches the raw text chunks for each topic from a SQLite knowledge base.
3. Runs a multi-stage agentic pipeline per topic to produce fully-populated slide data structures.
4. Validates and sanitizes every generated slide against the target layout schema.
5. Writes the final validated slide data back to MongoDB, ready to be consumed by a frontend renderer.

The output is a JSON representation of each slide (layout type + all placeholder content), not an actual `.pptx` file. A downstream renderer is expected to turn this JSON into a real presentation.

---

## Agentic workflow

The pipeline has three distinct agentic stages.

### Stage 1: Slide Layout Planner (`planner` agent)

Model: `google/gemini-2.5-flash-preview-05-20` via Vertex AI

The planner receives the raw topic text plus base64-encoded thumbnail images of every available slide template (stored in `Agents/assets/`). It reasons about the content and produces a sequenced list of `(layout, title)` pairs — one entry per slide it recommends creating. The structured output is typed as `list[PlannerOutput]`.

Available layouts: `titleSlide`, `contentFull`, `contentTwoCol`, `contentThreeCol`, `contentFourCol`, `contentWithMediaRight`, `contentWithMediaLeft`, `imageWithCaption`, `videoWithCaption`, `imageGrid`, `table`, `chartSingle`, `chartDual`, `dashboard`, `processHorizontal`, `processVertical`, `timelineHorizontal`, `timelineVertical`.

### Stage 2: Content Generation (`content_generator` agent + specialist sub-agents)

Model: `google/gemini-2.5-flash-preview-05-20` (orchestrator), `google/gemini-2.0-flash` (specialists)

For each planned slide, the `content_generator` agent acts as an orchestrator. It reads the layout schema and dispatches work to specialized sub-agents exposed as tools:

| Sub-agent | Tool name | Responsibility |
|---|---|---|
| `text_agent` | `text_placeholder_content_generation` | Generates text for all text-based placeholders, respecting word limits defined per layout |
| `image_agent` | `image_placeholder_content_generation` | Searches Google Custom Search API for relevant images, uses Gemini to generate descriptions, and selects the best match |
| `table_agent` | `table_placeholder_content_generation` | Produces structured table data (header row + up to 4 data rows, 3-6 columns) |
| `chart_agent` | `chart_placeholder_content_generation` | Selects chart type (line, bar, pie, doughnut, area) and generates data series from explicit or qualitative information in the content |
| `media_agent` | `media_placeholder_content_generation` | Searches YouTube via the YouTube Data API, fetches transcripts, and selects the most relevant video URL |

The orchestrator's output is then passed to the `content_formatter` agent, which strips Markdown code fences and extracts a clean JSON object matching the `ContentOutput` schema.

### Stage 3: Validation (`validator` agent)

Model: `google/gemini-2.0-flash`

The validator receives every formatted slide JSON and checks:
- Structural correctness against the target layout's schema (required/optional keys, types).
- Word count compliance for text placeholders.
- Semantic consistency with the original source content.
- Presence of Markdown or other formatting, which it removes.

Valid, sanitized output is written to the `validated_layouts` field in MongoDB.

---

## Tech stack

| Component | Technology |
|---|---|
| Agent framework | `openai-agents` (OpenAI Agents SDK) |
| LLM provider | Google Gemini 2.5 Flash and 2.0 Flash via Vertex AI (OpenAI-compatible endpoint) |
| Image understanding | Google Gemini 2.0 Flash (`google-genai`) |
| Image search | Google Custom Search API |
| Video search + transcripts | YouTube Data API v3 + `youtube-transcript-api` |
| API server | FastAPI + Uvicorn |
| Job scheduling | Google Cloud Batch |
| Database | MongoDB (presentation state) + SQLite (knowledge base) |
| Logging | Google Cloud Logging |
| Container registry | Google Artifact Registry |
| Deployment | Google Cloud Run (API) + Google Cloud Batch (worker) |
| CI/CD | GitHub Actions |

---

## Project structure

```
ppt_gen_agents/
├── main.py                  # FastAPI app: /create, /status, /presentation, /ping
├── agent_loop.py            # Entry point for the worker container; drives the full pipeline
├── batch_job.py             # Submits a Cloud Batch job that runs agent_loop.py
├── schema.py                # Pydantic models for the API (Input, PubSubMessage)
├── Agents/
│   ├── agents_new.py        # Planner agent + generate() function (stages 1 and 2)
│   ├── content_agents.py    # Specialist sub-agents (text, image, table, chart, media)
│   ├── validation_agents.py # Validator agent (stage 3)
│   ├── prompts.py           # All system prompts and layout descriptions
│   ├── schema.py            # Pydantic models (SlideLayout enum, PlannerOutput, ContentOutput)
│   ├── tools.py             # function_tool definitions: get_image_description, get_video_and_transcript
│   ├── data.py              # MongoDB + SQLite read/write helpers
│   ├── utils.py             # Output parsing helpers
│   └── assets/              # PNG thumbnails of each slide layout (fed to planner as images)
├── knowledge-base.db        # SQLite database: subjects, units, topics, content chunks
├── Dockerfile               # API server image
├── Dockerfile.worker        # Worker image (runs agent_loop.py)
├── pyproject.toml
├── requirements.txt
└── .github/workflows/
    └── agents-deploy.yml    # CI/CD: build + push both images, deploy API to Cloud Run
```

---

## Installation and setup

### Prerequisites

- Python 3.13+
- A Google Cloud project with the following APIs enabled:
  - Vertex AI
  - Cloud Batch
  - Cloud Logging
  - Artifact Registry
  - Custom Search API
  - YouTube Data API v3
- A MongoDB instance (Atlas or self-hosted)
- `uv` or `pip` for dependency management

### Install dependencies

```bash
pip install -r requirements.txt
```

Or with `uv`:

```bash
uv sync
```

### Environment variables

Create a `.env` file or export the following variables before running:

```
MONGO_URI=mongodb+srv://<user>:<password>@<host>/<dbname>
GEMINI_API_KEY=<your-gemini-or-google-api-key>
OPENAI_API_KEY=<required-by-openai-agents-sdk>
CSE_ID=<google-custom-search-engine-id>
```

Vertex AI authentication uses Application Default Credentials. Run:

```bash
gcloud auth application-default login
```

---

## Running locally

### Start the API server

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Run the agent pipeline directly

The worker entry point can be invoked standalone, bypassing Cloud Batch:

```bash
python agent_loop.py <doc_id>
```

`<doc_id>` must be a valid MongoDB ObjectId string for a document in the `main.PPT` collection that contains a `units` field listing unit IDs to process.

---

## API endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/create` | Accepts `{"doc_id": "<id>"}`, submits a Cloud Batch job, returns `{"status": "scheduled", "job_name": "..."}` |
| `GET` | `/status/{job_name}` | Returns the current state of a Cloud Batch job |
| `GET` | `/presentation/{doc_id}` | Returns the completed slide data for a given document |
| `GET` | `/ping` | Health check |

---

## End-to-end workflow

1. A document record is created in MongoDB with a list of unit IDs and a `status` of `"started"`.
2. `POST /create` is called with the document ID. The API submits a Cloud Batch job that spins up the worker container.
3. The worker runs `agent_loop.py`, which iterates over each unit and topic:
   - Stage 1 (planner) decides which slide layouts to create and in what order.
   - Stage 2 (content generator + specialists) populates every placeholder in every slide.
   - Stage 3 (validator) checks and cleans every slide JSON.
4. Intermediate results are written to MongoDB at each step so the caller can observe progress.
5. On completion, `status` is set to `"completed"` and the validated slide JSON is available via `GET /presentation/{doc_id}`.

---

## Deployment

The CI/CD pipeline (`agents-deploy.yml`) triggers on pushes to `main` or `dev`:

1. Authenticates to Google Cloud using Workload Identity Federation.
2. Builds and pushes two container images to Artifact Registry:
   - `api:latest` — the FastAPI server (`Dockerfile`).
   - `worker:latest` — the batch worker (`Dockerfile.worker`).
3. Deploys the API image to Cloud Run.

The worker image is pulled automatically by Cloud Batch when a job is submitted.
