# Stock Explorer Project Restructuring and Design Review

This document records the comprehensive status review and restructuring requirements for the "Stock Explorer" project as of 2026-06-14. These requirements will serve as the highest guiding principles (Action Plan) for subsequent automated development and refactoring by AI Agents.

---

## 1. Core Layout and Navigation Architecture (UI/UX Layout)

Completely abandon the current lengthy single sidebar design and adopt a "two-tier/dynamic navigation" architecture similar to VS Code and modern SaaS Apps (referencing the spirit of `stock_app_layout.html`).

### 1.1 Persistent Areas
* **Top Navigation Bar (Search-First)**:
  * A **global search box** must be permanently docked at the top of the screen (replacing the current left-side search) to align with modern software intuition.
  * Regardless of the functional depth, users can switch the observed stock at any time via the top search bar.
* **Leftmost Minimalist Activity Bar (Icon Bar)**:
  * Provides only "top-level (global)" navigation, e.g., Home, Blue-chip Stocks, Popular ETFs, My Watchlist, etc.
  * **Style Specification**: Uses an Icon + Text design. When collapsed or on smaller screens, it must gracefully degrade (e.g., showing only icons or only text) to ensure the layout doesn't break.
  * **Settings Portal**: A dedicated "Settings" button must be independently placed at the very bottom of the activity bar to unify all system/account settings.

### 1.2 Main Content & Floating Action Button (FAB)
* **Main Content Area**:
  * Entirely focused on "data and chart presentation," free from the distraction of complex menus.
* **Dynamic Floating Action Button (FAB)**:
  * A persistent floating button in the bottom-right corner of the main screen.
  * **Context-Aware Menu**: The functional menu that expands upon clicking the FAB is "dynamic."
  * **Example**: When a user searches for a specific stock (e.g., 2330 TSMC) and enters the "Company Homepage," all in-depth analysis functions (Business Card, Operational Checkup, Financial Health, Peer Comparison, Group Structure, etc.) are **fully contained within this floating menu**.
  * **In-place Switching**: After clicking a menu item (e.g., Financial Health), the main content area will "update in-place" to that function's screen, while the top search bar remains focused on 2330.

---

## 2. Visual Style & Layout Principles

### 2.1 PPT Presentation Style (One Viewport Principle)
* **Single-Screen Focus**: The primary screen should act like a PowerPoint slide, striving to present everything within "one screen (Viewport)" to avoid infinite scrolling.
* **One Screen, One Chart**:
  * Strictly prohibit cramming too many charts into a single screen.
  * Each perspective/screen focuses on conveying "one core theme," using the single most accurate chart accompanied by a concise text summary to allow users to "understand in seconds."

### 2.2 Company Landing Page Restructuring
* When searching and entering a specific stock, **do not directly throw a bunch of cold numbers or tables at the user**.
* **Hero Section**:
  * Display the large title (Company Name).
  * Must have a **"One-liner"** summarizing the company's core value proposition (e.g., "The world's best foundry, manufacturing over 90% of high-end chips").
  * Paired with a representative or high-quality conceptual image.
* **Right-side Dynamic Feed**:
  * Place the company's latest updates, news links, or significant events to give the page a sense of vitality.

---

## 3. Content Depth, Data Accuracy, and Professionalism

Current content is superficial and contains errors or unprofessional terminology, requiring a "global audit and correction."

### 3.1 Data Logic & Accuracy
* **Dividend Yield Calculation**:
  * **Strictly prohibit** treating a single quarter's (e.g., Q1) dividend as the annual dividend or calculating the annual yield haphazardly based on it.
  * **Must adopt an "Annualized Projection Logic"**: For example, if Q1 growth is 25% and dividend payout increases by 15%, the system should project the annual total dividend based on this logic and clearly mark it as an "Estimated Value."
  * **Historical Comparison**: Provide a table/chart with a selectable time range comparing historical dividend yields over recent years to help users judge stability.
* **Unit Accuracy**:
  * Conduct a global audit of all financial data "units (e.g., billions, millions)" for revenue, profit, etc., ensuring absolute precision and consistency across charts, text, and numbers.

### 3.2 Professional Tone of Voice & i18n Architecture
* **Internationalization (i18n) Architecture**:
  * **Crucial Upgrade**: The current codebase suffers from hardcoded strings, making it look like an amateur project. We must implement a robust **multi-language (i18n) architecture**.
  * All UI text, system messages, and chart labels must be extracted into centralized language files/dictionaries (e.g., JSON/YAML). 
  * This enables easy text matching/searching, structured content management, and elevates the software architecture to professional enterprise standards.
* **Ban Internet Slang and Non-local Terms**:
  * Completely eradicate terms like "一個小目標" (a small target) or other unprofessional banter.
  * For world-class enterprises (like TSMC), such language severely damages the software's professionalism.
* **Specific and Objective**: All descriptions must be based on concrete numbers and objective facts.

### 3.3 Progressive Disclosure & Deep Insights
* **From Surface to Deep (More...)**:
  * Following the "One Screen, One Chart" principle, the homepage only presents summaries (e.g., revenue structure pie chart).
  * Must provide a **"More... (View Details)"** button leading to an in-depth analysis page.
* **Demonstrating Software Value (The "So What")**:
  * Professional software cannot merely provide easily accessible surface numbers.
  * In the "More..." details, **deep insights** must be provided. For instance, instead of just telling the user 3nm accounts for 20%, explain "who the primary clients for 3nm are," "what the absolute output value is," establishing the software's irreplaceable value.

---

## 4. Action Items for AI Agent

1. **[Architecture/i18n]** Implement a multi-language (i18n) architecture. Extract all hardcoded strings into centralized localization files to elevate codebase professionalism.
2. **[UI/UX]** Remove the ineffective "Page Navigation" button row below the search bar on the homepage.
3. **[UI/UX]** Implement a persistent Top Navigation Bar (Search).
4. **[UI/UX]** Implement a minimalist left-side Activity Bar (Icon Bar) with a bottom Settings button.
5. **[UI/UX]** Implement a context-aware dynamic Floating Action Button (FAB) in the bottom right, migrating functions like Business Card and Operational Checkup into this menu.
6. **[Content]** Refactor the company homepage to implement a "One-liner summary + Image + Right-side News Feed" layout.
7. **[Data]** Correct the dividend yield calculation logic, incorporating annualized projection algorithms and historical comparison features.
8. **[Data]** Execute a global audit and correction of data Units.
9. **[Content]** Execute a global copywriting audit, eliminating all unprofessional slang and inappropriate regional terms via the new i18n system.
10. **[Architecture]** Enforce the "One Screen, One Chart" and "Progressive Disclosure (More...)" data presentation architecture, enriching each sub-page with deep insight data.
