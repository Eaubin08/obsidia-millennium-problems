
FROM python:3.10-slim
RUN apt-get update && apt-get install -y build-essential git curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY repro/environment.yml /app/repro/environment.yml
RUN pip install --upgrade pip
# Install Python packages via pip for portability (conda not present in slim image)
RUN pip install numpy scipy mpmath requests pandas matplotlib tqdm pycryptodome
COPY . /app
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["/bin/bash", "/app/repro/entrypoint.sh"]
