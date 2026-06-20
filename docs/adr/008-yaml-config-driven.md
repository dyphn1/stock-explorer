# ADR-008: Fully Config-Driven Design

## Status
Accepted

## Date
2026-06-07

## Background

Stock Explorer needs to support watchlists, event records, learning courses, and more. This data needs to be persistent, but the MVP stage is not suitable for introducing a database.

## Decision

Use **YAML files** as configuration and data storage, implementing a fully config-driven design.

## Configuration File List

| File | Purpose |
|------|---------|
| `config/watchlist.yaml` | Watchlist, price alerts |
| `config/events.yaml` | Event records |
| `config/quiz.yaml` | Comprehension quiz questions |
| `config/lessons/` | Learning academy course content |
| `config/comprehension_quiz.yaml` | Comprehension quiz metadata |

## Rationale

1. **Zero dependencies**: No database needed
2. **Human-readable**: Daniel can edit directly
3. **Version control**: YAML files can be tracked in Git
4. **AI Agent friendly**: Easy to read and write

## Alternatives

| Option | Reason for Rejection |
|--------|---------------------|
| SQLite | Over-engineered for MVP stage |
| JSON | No comment support, poor readability |
| Database (PostgreSQL) | High deployment complexity |

## Consequences

- ✅ Zero-cost persistence
- ✅ Easy to backup and version control
- ⚠️ Concurrent writes require filelock
- ⚠️ Poor performance with large data volumes (acceptable for now)
