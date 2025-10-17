# TableTalk Agent Monorepo

This repository contains the full stack implementation plan for **TableTalk**, a conversational dining assistant that runs on the Google Agent Development Kit (ADK), serves models via AWS Bedrock, and improves over time with Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO) from human feedback. The repo is organised as a monorepo so that the agent, backend APIs, frontend client, infra-as-code, and training pipelines can evolve together.

## Repository layout

```
agentic-yelp/
  agent/                 # Google ADK planner, tools, and tests
  api/                   # FastAPI backend with Bedrock integration
  frontend/              # Next.js client for chat + feedback
  training/              # SFT and RLHF/DPO pipelines
  data/                  # Seed datasets and menu catalogues
  infra/                 # AWS CDK stacks
  eval/                  # Offline evaluation harness
  .github/workflows/     # CI configuration
```

Each top-level package includes README snippets or docstrings that describe how to extend the scaffolding into production services.

## Getting started

1. **Python env** – create a Python 3.11+ virtualenv, install requirements per package (to be added) and export AWS + Bedrock credentials as described in the package READMEs.
2. **Node env** – install Node.js 20+. The `frontend/` app is a Next.js 14 project and uses Turbopack/Vite during dev.
3. **Infrastructure** – the `infra/cdk/` folder contains AWS CDK stacks for S3, DynamoDB, API Gateway/Lambda (or ECS), and CloudFront. Deploy with `cd infra/cdk && cdk deploy --all` once AWS credentials are configured.
4. **Local orchestration** – run the FastAPI app (`uvicorn api.app.main:app --reload`) and the Next.js dev server (`npm run dev` inside `frontend/`). The agent planner can be invoked directly via `python agent/adk_app/planner.py --demo-prompt "Gluten-free ramen under $20"`.
5. **Model fine-tuning** – seed SFT and RLHF datasets live under `data/`. Scripts in `training/` upload data to S3 and kick off Bedrock or SageMaker jobs for LoRA/SFT and DPO fine-tuning.

## Status

This codebase is a starting blueprint. Core folders include implementation stubs, data schemas, and configuration files that can be fleshed out by a coding agent or engineering team. Follow TODO comments and module docstrings to implement production logic, integrate real data sources, and harden deployment workflows.
