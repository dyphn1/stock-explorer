# Development Guide — Stock Explorer

> **Audience**: Developers, AI Agents | **Last Updated**: 2026-06-17

---

## 1. Environment Setup

### 1.1 Prerequisites
- Python 3.11+
- Git
- (Optional) uv package manager

### 1.2 Installation Steps
```bash
# 1. Clone
git clone https://github.com/your-username/stock-explorer.git
cd stock-explorer

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -e .

# 4. Start development server
streamlit run src/main.py
```

### 1.3 Verify Environment
```bash
# Run tests
uv run pytest

# Verify syntax
uv run python -c "import src; print('OK')"
```

---

## 2. Layered Architecture Standards

### 2.1 Strict Layering
```
Presentation (src/pages/) → Routing (src/pages/router.py) → Services (src/services/) → Data (src/data/)
```

### 2.2 Layer Responsibilities and Restrictions

#### Data Layer (`src/data/`)
```python
# ✅ Correct: return DataFrame
def get_daily_price(self, stock_id: str) -> pd.DataFrame: ...

# ✅ Correct: return None to indicate no data (don't raise exception)
def get_latest_price(self, stock_id: str) -> dict | None: ...

# ❌ Wrong: deciding whether to show spinner in data layer
# ❌ Wrong: business logic in data layer (e.g., sorting, taking top N)
```
- **Forbidden**: import streamlit, containing business logic

#### Service Layer (`src/services/`)
```python
# ✅ Correct: pure function, input data → output chart
def create_revenue_trend_chart(revenue_df: pd.DataFrame) -> go.Figure: ...

# ✅ Correct: pure function, input value → output text
def get_gross_margin_analogy(margin: float) -> str: ...

# ❌ Wrong: using st.plotly_chart() in service layer
# ❌ Wrong: calling FinMind API directly in service layer
```
- **Forbidden**: import streamlit, direct API calls, side effects

#### Routing Layer (`src/pages/router.py`)
- The only place that decides "when to load what data"
- Manages loading state during page transitions
- **Forbidden**: direct UI component generation

#### Presentation Layer (`src/pages/*.py`)
```python
# ✅ Correct: View receives data dict, calls service to generate charts
def _render_business_card(data: dict, client: FinMindClient):
    st.markdown(f"## {data['stock_name']}")
    fig = create_revenue_pie_chart(data["monthly_revenue"])
    st.plotly_chart(fig)

# ❌ Wrong: reloading data in View that router already loaded
# ❌ Wrong: complex calculations in View
```
- **Forbidden**: direct cache read/write, complex calculations, business logic

---

## 3. Coding Standards

### 3.1 Naming Conventions
- **Files**: `snake_case.py` (e.g., `business_card.py`)
- **Functions**: `snake_case` (e.g., `get_revenue_data`)
- **Classes**: `PascalCase` (e.g., `FinMindClient`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **i18n key**: `dot.notation` (e.g., `pages.business_card.title`)

### 3.2 String Handling
```python
# ✅ Correct: use i18n
from src.core.i18n import t
st.markdown(t("pages.business_card.title"))

# ❌ Wrong: hardcoded Chinese
st.markdown("Business Card")
```

### 3.3 Error Handling
```python
# ✅ Correct: graceful degradation
data = client.get_daily_price(stock_id)
if data is None or len(data) == 0:
    st.warning(t("errors.no_data"))
    return

# ❌ Wrong: letting exceptions crash the entire page
data = client.get_daily_price(stock_id)  # may raise exception
```

### 3.4 Cache Usage
```python
# ✅ Correct: through FinMindClient (built-in cache)
client = FinMindClient()
data = client.get_daily_price(stock_id)

# ❌ Wrong: directly reading/writing .cache/ directory
with open(".cache/some_file.json") as f: ...
```

---

## 4. Adding a New Page

### 4.1 Current Process (requires modifying 3 places)
1. Create new page file in `src/pages/`
2. Add import in `src/pages/router.py`
3. Add if-elif branch in `src/pages/router.py`

### 4.2 Target Process (Plugin Chassis)
1. Create new plugin in `src/plugins/`
2. Inherit `BasePlugin`, implement `render()` method
3. Auto-scan and register, **zero routing logic changes**

---

## 5. Testing Standards

### 5.1 Test Layers
| Layer | What It Checks | Pass Criteria |
|-------|----------------|---------------|
| **L0** | Syntax, imports, key uniqueness | Must pass before commit |
| **L1** | Page rendering (all pages load without crash) | Must pass before handoff |
| **L2** | Interactions (buttons, navigation, forms) | Must pass before release |
| **L3** | Visual/UX (screenshot analysis) | Designer review |

### 5.2 Running Tests
```bash
# All tests
uv run pytest

# Specific file
uv run pytest tests/test_business_logic.py

# Specific marker
uv run pytest -m tone
```

---

## 6. Git Standards

### 6.1 Commit Style
Follow Angular-style Conventional Commits:
```
feat: add revenue pie chart to business card
fix: resolve cache invalidation in get_daily_price
refactor: extract business_card.py into sub-directory
docs: update architecture overview
test: add unit tests for analogy_engine
```

### 6.2 Branch Strategy
- `main`: Stable version
- `feature/Cxxx-<name>`: New feature
- `fix/Dxxx-<name>`: Bug fix
- `refactor/TDxxx-<name>`: Refactor

---

## 7. AI Agent Collaboration Standards
