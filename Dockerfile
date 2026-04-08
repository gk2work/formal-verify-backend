FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ── System packages + EDA tools ─────────────────────────────────
# yosys  : synthesis / elaboration (required by sby)
# z3     : SMT solver used as the default prover
# git    : needed to pip-install sby from GitHub
# build-essential / libffi-dev / libssl-dev : native build deps for
#          chromadb, pyvcd, and other Python C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    yosys \
    z3 \
    git \
    make \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Make `python` / `pip` point to python3
RUN ln -sf /usr/bin/python3 /usr/bin/python \
 && ln -sf /usr/bin/pip3   /usr/bin/pip

# ── SymbiYosys (sby) ────────────────────────────────────────────
# sby has no setup.py — installed via its Makefile.
RUN git clone --depth 1 https://github.com/YosysHQ/sby /tmp/sby \
 && make -C /tmp/sby install \
 && rm -rf /tmp/sby

# ── Python dependencies ─────────────────────────────────────────
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application code ─────────────────────────────────────────────
COPY . .

# Persistent work dirs (ephemeral on free hosts, but needed at runtime)
RUN mkdir -p data/formal_work data/chromadb

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
