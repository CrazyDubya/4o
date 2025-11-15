# Document Processing System Blueprint

This blueprint outlines a vendor-agnostic, end-to-end architecture for a multi-tenant document processing pipeline. It emphasizes reliable queue handling, persistent storage, multi-user safety, collision avoidance, backups, and redo/replay capabilities.

## System Overview
- **API Layer:** REST interface with multi-tenant authentication.
- **Metadata Database:** SQL store tracking batches, documents, runs, results, reviews, links, and audit data.
- **Object Storage:** Immutable originals and versioned derivatives stored using content-addressed identifiers.
- **Work Queues:** Lease-based queues with visibility timeouts and dead-letter queues (DLQs).
- **Workers:** Specialized workers process stages: ingest → preprocess → OCR → layout/KV → LLM parse → reconcile → match → package.
- **Orchestrator:** Saga-based orchestration maintains stage state machines and retries.
- **Review UI:** Dual-pane UI with optimistic locking for concurrent edits.
- **Backups & Redo:** Content-addressed storage, lineage tracking, and run replay support.

## Core Identifiers and Idempotency
- Stable identifiers: `tenant_id`, `batch_id`, `doc_id`, `run_id` (per processing attempt), and `trace_id` (per stage).
- Clients may provide an `Idempotency-Key`; the API persists a request hash to prevent duplicate enqueues.
- Content hashes (SHA-256) deduplicate files and underpin content-addressed storage.

## Data Model Sketch (SQL)
```sql
-- Tenancy & users
CREATE TABLE tenants(
  tenant_id UUID PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMPTZ
);
CREATE TABLE users(
  user_id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants,
  email TEXT UNIQUE,
  role TEXT,
  created_at TIMESTAMPTZ
);

-- Batches & documents
CREATE TABLE batches(
  batch_id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants,
  status TEXT,
  created_at TIMESTAMPTZ,
  webhook_url TEXT,
  schema_mapping JSONB,
  dedupe BOOLEAN DEFAULT true
);
CREATE TABLE documents(
  doc_id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants,
  batch_id UUID REFERENCES batches,
  filename TEXT,
  content_sha256 BYTEA,
  pages INT,
  status TEXT,
  created_at TIMESTAMPTZ,
  version INT DEFAULT 1  -- optimistic locking for UI edits
);

-- Storage references (immutable)
CREATE TABLE blobs(
  blob_id UUID PRIMARY KEY,
  tenant_id UUID REFERENCES tenants,
  sha256 BYTEA UNIQUE,
  bytes_len BIGINT,
  mime TEXT,
  uri TEXT,
  created_at TIMESTAMPTZ
);
CREATE TABLE derivatives(
  artifact_id UUID PRIMARY KEY,
  doc_id UUID REFERENCES documents,
  stage TEXT,
  sha256 BYTEA,
  uri TEXT,
  created_at TIMESTAMPTZ
);

-- Runs & stages (lineage)
CREATE TABLE runs(
  run_id UUID PRIMARY KEY,
  doc_id UUID REFERENCES documents,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  status TEXT,
  attempt INT,
  parent_run_id UUID NULL,
  reason TEXT
);
CREATE TABLE stages(
  stage_id UUID PRIMARY KEY,
  run_id UUID REFERENCES runs,
  name TEXT,
  status TEXT,
  started_at TIMESTAMPTZ,
  ended_at TIMESTAMPTZ,
  worker_id TEXT,
  retries INT,
  error TEXT,
  trace JSONB
);

-- Results & matches (versioned)
CREATE TABLE results(
  result_id UUID PRIMARY KEY,
  doc_id UUID REFERENCES documents,
  run_id UUID REFERENCES runs,
  result_version INT,
  payload JSONB,
  confidences JSONB,
  created_at TIMESTAMPTZ
);
CREATE UNIQUE INDEX results_latest ON results(doc_id, result_version);

CREATE TABLE matches(
  match_id UUID PRIMARY KEY,
  doc_id UUID REFERENCES documents,
  run_id UUID REFERENCES runs,
  rank INT,
  db_id TEXT,
  score NUMERIC,
  reason TEXT,
  snapshot JSONB,
  created_at TIMESTAMPTZ
);

-- Human review & links
CREATE TABLE reviews(
  review_id UUID PRIMARY KEY,
  doc_id UUID REFERENCES documents,
  user_id UUID REFERENCES users,
  created_at TIMESTAMPTZ,
  edit_patch JSONB,
  from_result_version INT,
  to_result_version INT
);
CREATE TABLE links(
  link_id UUID PRIMARY KEY,
  doc_id UUID REFERENCES documents,
  db_id TEXT,
  link_type TEXT,
  user_id UUID REFERENCES users,
  confidence NUMERIC,
  created_at TIMESTAMPTZ
);

-- Webhook/outbox pattern
CREATE TABLE outbox_events(
  evt_id UUID PRIMARY KEY,
  tenant_id UUID,
  topic TEXT,
  payload JSONB,
  created_at TIMESTAMPTZ,
  delivered BOOLEAN DEFAULT false,
  attempts INT DEFAULT 0,
  last_error TEXT
);

-- Audit
CREATE TABLE audit_log(
  audit_id UUID PRIMARY KEY,
  tenant_id UUID,
  user_id UUID NULL,
  actor TEXT,  -- 'system' or user ID
  entity_type TEXT,
  entity_id UUID,
  action TEXT,
  detail JSONB,
  ts TIMESTAMPTZ
);
```

## Queues and Topics
- `ingest.q` → upload registration, document creation, blob storage.
- `preprocess.q` → deskew, denoise, masking.
- `ocr.q` → multi-engine OCR execution.
- `layout.q` → key-value and table detection.
- `llm.q` → schema-guided LLM parsing.
- `reconcile.q` → consensus and validation checks.
- `match.q` → exact and fuzzy lookup (top 20 candidates).
- `package.q` → persist results and emit outbox events.
- Each queue applies visibility timeouts, per-stage retry limits, and dedicated dead-letter queues (`*.dlq`).

### Message Envelope
```json
{
  "tenant_id": "t...",
  "doc_id": "d...",
  "run_id": "r...",
  "stage": "ocr",
  "attempt": 1,
  "deadline": "2025-11-01T17:50:00Z",
  "idempotency_key": "hash(tenant|doc|stage|attempt)",
  "trace_parent": "00-...-..."
}
```

## Orchestration and State Machines
- Document processing progression: `UPLOADED → PREPROCESSING → OCR → LAYOUT → LLM_PARSE → RECONCILE → MATCH → PACKAGED`. Retries branch to `FAILED → DLQ (quarantine)` after exhausting attempts.
- Orchestrator records `stages` rows for every hop and manages retries with exponential backoff (30s → 2m → 10m → 1h with jitter).
- Workers obtain leases, emit heartbeats, and must be idempotent; success upserts the stage and enqueues the next stage. Crashes release messages for reprocessing (at-least-once semantics).

## Persistence Guarantees
- Workers derive outputs from immutable inputs and write using unique `(doc_id, stage, attempt)` keys.
- Outbox pattern ensures events and state changes persist atomically; a dispatcher reliably delivers notifications.
- Optimistic concurrency uses `documents.version` and `results.result_version` for compare-and-swap updates.
- Advisory locks (or short-TTL distributed locks) mitigate high-contention edits.

## Multi-User Collision Avoidance
- Read path: UI fetches fields alongside `result_version` and `documents.version`.
- Write path: clients supply `If-Match` headers (expected version). Updates increment `version`; mismatches return HTTP 409 for conflict resolution.
- Per-field drafts live in `reviews.edit_patch` (JSON Patch). Re-search operations leverage drafts without committing new result versions until saved.
- Linking enforces uniqueness on `(doc_id, db_id, link_type)` while preserving audit history.

## Backup, Redo, and Replay
- Object storage keeps originals and derivatives with versioning enabled; manifests list artifacts and checksums.
- Database strategy: daily full backups plus WAL/binlog shipping targeting ≤5 minute RPO and 1–2 hour RTO.
- Reruns: `POST /v1/documents/{doc_id}/rerun` creates a new `run_id` referencing existing or updated blobs, with lineage tracked via `runs.parent_run_id`.
- Result promotion increments `result_version` and records `reviews` entries.
- Batch exports provide signed manifests for integrity-verified re-ingestion.

## API Surface
- `POST /v1/batches`
- `POST /v1/batches/{id}/documents`
- `GET /v1/batches/{id}` and `/results`
- `POST /v1/documents/{doc_id}/rerun`
- `POST /v1/research`
- `POST /v1/link`
- `PATCH /v1/documents/{doc_id}` (with expected version)
- `GET /v1/audit?doc_id=...`

### Webhooks
- Delivered via outbox dispatcher with signing secret and retries: `batch.completed`, `batch.partial`, `document.completed`, `document.failed`, `document.reviewed`.

## Matching Engine Guidance
- Pre-index normalized keys (`name_norm`, `address_norm`, `zip`, `id_value`).
- Support phonetic keys (Soundex/Metaphone) and optional vector indexes.
- Maintain per-tenant LRU caches of recent candidates.
- Re-search leverages review patches before persisting matches.

## Worker Idempotency Contract
1. Read stage message.
2. Skip processing when a `stages` row already records success for `(run_id, name)`.
3. Produce deterministic artifact names stored under `doc_id/run_id/stage/`.
4. Upsert stage status to `succeeded`, recording retries and trace data.
5. Enqueue the subsequent stage referencing the same `run_id`.
6. When terminal, write outbox events (`document.completed` or `document.failed`) within the same transaction.

## Observability and Health
- Propagate W3C trace context (`traceparent`) from API through workers.
- Monitor queue lag, stage durations, OCR error rates, confidence averages, retries, and DLQ counts.
- Generate drift reports comparing template match scores over time.
- Redact PII in logs; provide secure tracing as an opt-in.

## Roles and Permissions
- Roles: `admin`, `reviewer`, `viewer`, `api_client`.
- Enforce tenant scoping at the row level.
- Reviewers can edit and link; viewers remain read-only. Admins can rerun processes and promote runs.

## Failure Modes and Handling
- Poison documents (e.g., bad PDFs): three rapid retries before DLQ quarantine with remediation guidance.
- Large batch spikes: apply token-bucket rate limiting per tenant, enforce queue quotas, and respond with HTTP 429 when backpressure triggers.
- Webhook outages: the outbox retries exponentially; after configured attempts, mark events as stuck and surface them in an admin view.

## Test and QA Checklist
- Idempotency: duplicate `POST` requests with identical `Idempotency-Key` values must not duplicate documents.
- Lease expiry: terminate a worker mid-stage and confirm another worker safely resumes.
- Conflict handling: simultaneous edits trigger HTTP 409 and offer merge workflows.
- Redo: reruns produce new `run_id` values; promoting results increments `result_version`.
- DLQ: introduce malformed blobs to validate quarantine and admin requeue paths.
- Backup restore: simulate point-in-time recovery and validate manifest checksums.

## Example Sequence (Happy Path)
1. `POST /batches` → receive `batch_id`.
2. `POST /batches/{id}/documents` → create document, store blob, enqueue `ingest.q`.
3. Workers progress: preprocess → OCR → layout → LLM parse → reconcile → match → package.
4. `package.q` persists `results` (`result_version = 1`) and `matches` (≤20), then emits `document.completed`.
5. UI loads document: left pane renders derivative image; right pane displays extracted fields and matches.
6. Reviewer edits address and triggers `POST /v1/research` (no version bump).
7. Reviewer links records via `POST /v1/link`.
8. Reviewer saves: server increments `documents.version`, creates `results` (`result_version = 2`), records `reviews`.
9. Batch completion triggers `batch.completed` webhook via outbox.
