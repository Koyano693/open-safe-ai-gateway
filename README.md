# Open Safe-AI Gateway

> A Production-Ready Reference Implementation for High-Availability & Self-Governing AI Infrastructure via Policy as Code and Semantic Caching.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Amazon%20Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)

---

## 💡 Overview

As enterprise adoption of Generative AI (LLMs) accelerates, software engineering teams face three critical structural challenges:
1. **Security & Privacy Risks**: PII leakage, prompt injection, and unauthorized data access.
2. **Hallucination & Governance**: Unreliable responses and rigid, manual compliance management.
3. **Resilience & Availability**: Cloud API throttling (HTTP 429) and upstream service outages.

**Open Safe-AI Gateway** addresses these challenges through **infrastructure, facts, and structure** rather than speculative assumptions. It provides a multi-layered, zero-trust defense gateway integrating FastAPI, Amazon Bedrock Guardrails, and Redis Stack (Vector Search).

---

## 🔑 Key Features & Architecture

- **Policy as Code Governance**: Guardrail policies are defined declaratively in YAML and synchronized directly to AWS Bedrock Guardrails using GitHub Actions with OIDC authentication.
- **Zero-Downtime Resilience**: Implements a circuit breaker pattern with Redis HNSW Vector Search. If upstream AI services experience outages or throttling, high-similarity responses from historical queries are served within milliseconds.
- **Contextual Grounding**: Automated real-time verification of model output factual consistency before returning responses to clients.

---

## 🚀 Quick Start (Docker Compose)

### 1. Clone the Repository & Setup Environment

```bash
git clone [https://github.com/Koyano693/open-safe-ai-gateway.git](https://github.com/Koyano693/open-safe-ai-gateway.git)
cd open-safe-ai-gateway
cp .env.example .env

docker-compose up --build -d
