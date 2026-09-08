# Market Pulse Agent

A fully autonomous, multi-stage agent that fetches S&P 500 and ASX 200 index

prices twice daily and publishes them to a live dashboard — with no paid

services, API keys, or servers of my own.

**Live dashboard:** [https://doubled112.github.io/market-pulse-agent/](https://doubled112.github.io/market-pulse-agent/)

## Why this exists

This project was built as a hands-on exercise in agent orchestration: rather

than one script that does everything, the work is split into independent

stages that hand data to each other, coordinated by a single orchestrator.

That mirrors how real agentic systems are typically structured — each stage

has one job, can be tested in isolation, and failures are handled at the

point they happen rather than crashing the whole pipeline silently.

## Architecture

