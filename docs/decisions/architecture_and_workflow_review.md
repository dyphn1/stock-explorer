# Stock Explorer - Architecture & Workflow Review

This document outlines the fundamental flaws in the current project workflow and codebase architecture, establishing mandatory guidelines for the upcoming refactoring phase. These rules MUST be followed by all AI Agents before any new features are developed.

---

## 1. Project Development Workflow

### 1.1 The "Document-First" Mandate
The current "code-first" approach has led to a spaghetti codebase. Moving forward, a strict **Documentation-First** workflow is mandatory.
* **No coding without design**: Before writing any implementation code, the following documents must be established and approved:
  1. **System Architecture Design**: Data flow, module boundaries, state management.
  2. **UI/UX Design**: Wireframes, interaction logic, user journey flows.
  3. **Functional Specification**: Input/output parameters, edge cases, business logic rules.

### 1.2 Feature Convergence & Refactoring Phase
* **Stop new features**: Halt all current unguided feature development.
* **Convergence**: Audit existing features against the newly created design documents. Discard redundant or out-of-scope features to define a clear Minimum Viable Product (MVP).
* **Refactoring First**: The entire codebase must be restructured according to the architectural rules below *before* any new development resumes.

---

## 2. Quality Assurance & Testing

### 2.1 Lack of Automated Testing
The project currently lacks a reliable safety net, causing regression issues during every modification.
* **Unit & Integration Tests**: Core business logic and data processing must be covered by robust automated tests (e.g., `pytest`).
* **Test-Driven or Test-Verified**: All new code and refactored code must pass CI/CD checks before merging.

### 2.2 UI/UX Flow & Visual Validation
Testing must go beyond backend logic.
* **UX Flow Validation**: Before implementing UI changes, define State/Flow diagrams. Verify that the UI transitions correctly match the expected states (e.g., clicking the FAB updates the main content but preserves the top search bar state).
* **Visual Regression**: Ensure UI layout, CSS injections, and card styling do not break across different functional pages.

---

## 3. Codebase Architecture & Design Patterns

The current `src/` directory is merely a collection of scripts, lacking a formal software architecture.

### 3.1 Adopt a Formal Design Pattern (e.g., POP + MVC)
The codebase lacks a systemic coding philosophy. We must adopt and strictly adhere to a clear architectural pattern.
* **Model-View-Controller (MVC) adaptation for Streamlit**:
  * **Model (Data/Core)**: Pure Python classes/functions handling business rules, calculations (e.g., annualized dividend yields), and data state. 100% testable and decoupled from Streamlit.
  * **View (UI Components)**: Functions responsible *only* for rendering Streamlit elements. No data fetching or math operations should occur here.
  * **Controller (Routing/Services)**: Orchestrates the flow—fetching data via the Model, passing it to the View, and handling user inputs (e.g., FAB clicks, search queries).
* **Protocol-Oriented Programming (POP) / Interface-driven**: Define clear protocols/interfaces for services (e.g., Data Fetchers, Analyzers) to ensure decoupling and easily mockable dependencies for testing.

### 3.2 Strict Layered Architecture (Separation of Concerns)
* **Core Business Logic (`src/core/`)**: Must be pure Python. Example: Dividend projection algorithms.
* **Data Access Layer (`src/data/`)**: Handles external API communication (FinMind), caching, error retries, and data normalization.
* **Shared UI Library (`src/ui/components/`)**: Reusable UI elements (Hero cards, specialized charts, FABs). Stop copy-pasting HTML/CSS across pages.
* **Pages (`src/pages/`)**: Lean controllers that stitch together Data Services and Shared UI Components based on the routing state.

### 3.3 Core Framework vs. Plugin Architecture (The "Chassis" Pattern)
**The most critical architectural failure of the current project is the absence of a unified core framework (a "chassis").** 

Currently, features are implemented haphazardly and stuffed into the project like stuffing into a plush toy, creating a monolithic and tightly coupled nightmare.

* **Framework First**: A robust, overarching framework must be designed and implemented *before* any individual feature is developed. This framework handles the lifecycle, routing, state management, and dependency injection of the entire application.
* **Plugin-based Feature Modules (Plug-and-Play)**: 
  * Every feature (e.g., Business Card, Financial Health, Peer Comparison) must be designed as an independent **plugin or module**.
  * Features must conform to a standardized protocol/interface defined by the core framework.
  * The core framework is responsible for dynamically loading, rendering, and routing these plugins. 
  * **Rule of Thumb**: Adding, removing, or disabling a feature should involve registering or unregistering a plugin, requiring absolutely zero modifications to the core framework's routing logic or other features.

---

## 4. Security & Error Handling

### 4.1 Lack of Security Best Practices
The project must adhere to standard security protocols, especially when handling external API keys, user data, or executing dynamic queries.
* **Secret Management**: API keys (e.g., FinMind token) or database credentials must *never* be hardcoded. They must be managed via strict environment variables (`.env`) and secure secret managers.
* **Input Validation & Sanitization**: All user inputs (especially the global search bar) must be strictly validated and sanitized to prevent injection attacks or unexpected system crashes.

### 4.2 Graceful Degradation & Error Boundaries
* **Fail Gracefully**: If a specific plugin (e.g., Financial Health) or external API fails, it should *only* crash that specific component, displaying a localized error state (Empty State/Error Boundary) rather than crashing the entire Streamlit application.
* **Rate Limit Handling**: Implement robust interceptors for external API rate limits (HTTP 429), providing cached fallback data and clear warnings to the user instead of unhandled exceptions.
