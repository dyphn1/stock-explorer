# ADR-001: Choose Streamlit as the Frontend Framework

## Status
Accepted

## Date
2026-06-06

## Background

Stock Explorer is an MVP-stage tool that requires rapid iteration. The team needs a frontend framework that allows Python developers to quickly build data applications.

## Decision

Choose **Streamlit** as the frontend framework.

## Rationale

1. **Development speed**: Pure Python development, no frontend knowledge required, ideal for rapid iteration
2. **Data-friendly**: Native support for pandas DataFrame and Plotly charts
3. **MVP positioning**: Suitable for single-user local deployment, no complex user authentication needed
4. **AI Agent friendly**: Python code is easy for AI Agents to understand and modify

## Alternatives

| Option | Pros | Cons | Reason for Rejection |
|--------|------|------|---------------------|
| React + FastAPI | Full frontend-backend separation | High development cost, requires frontend knowledge | Over-engineered for MVP stage |
| Gradio | Lighter weight | Weaker customization | Insufficient layout flexibility |
| Flask + Jinja2 | Full control | Requires hand-written HTML/JS | Slow development speed |

## Consequences

- ✅ Rapid MVP delivery
- ✅ Lower barrier for AI Agent development
- ⚠️ Multi-user deployment limited (Streamlit is designed for single-user)
- ⚠️ Mobile experience limited
- ⚠️ Highly customized UI requires CSS injection

## Future Considerations

If multi-user deployment or mobile support is needed in the future, consider migrating to React/Vite + FastAPI. However, for the current MVP stage, Streamlit is the best choice.
