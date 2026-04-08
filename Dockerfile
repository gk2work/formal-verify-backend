FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ── System deps ──────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    ca-certificates \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/bin/python3 /usr/bin/python \
 && ln -sf /usr/bin/pip3   /usr/bin/pip

# ── OSS CAD Suite ────────────────────────────────────────────────
# Includes: yosys (latest, full SV support), sby, boolector, z3, etc.
# Replaces the old Ubuntu apt yosys (v0.9 — no `logic` keyword support).
# URL format: directory uses YYYY-MM-DD, filename uses YYYYMMDD.
RUN curl -L \
    "https://github.com/YosysHQ/oss-cad-suite-build/releases/download/2024-01-01/oss-cad-suite-linux-x64-20240101.tgz" \
    -o /tmp/oss-cad-suite.tgz \
 && tar -xzf /tmp/oss-cad-suite.tgz -C /opt/ \
 && rm /tmp/oss-cad-suite.tgz

ENV PATH="/opt/oss-cad-suite/bin:$PATH"

# ── Python dependencies ──────────────────────────────────────────
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application code ─────────────────────────────────────────────
COPY . .

RUN mkdir -p data/formal_work data/chromadb

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
