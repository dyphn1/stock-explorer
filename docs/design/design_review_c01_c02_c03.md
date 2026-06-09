# Design Review: ISSUE-C01 / C02 / C03

> **Reviewer:** Design Reviewer sub-agent
> **Date:** 2026-06-09
> **Scope:** UX/Visual design review for 3 P0 competitor-driven features
> **Documents reviewed:**
> - `docs/design/design_system.md` (PPT-style design system)
> - `docs/design/design_review.md` (consolidated roadmap)
> - `docs/research/competitor_research.md` (competitor analysis)
> - `docs/status/issues.md` (issue definitions)
> - `docs/strategy/product_vision.md` (product vision)
> - `src/pages/business_card.py` (current layout)
> - `src/pages/watchlist_page.py` (current layout)
> - `src/services/adaptive_engine.py` (event detection engine)
> - `src/services/watchlist.py` (watchlist data layer)
> - `src/pages/event_dashboard.py` (event dashboard)

---

## Design Philosophy Reminder

All 3 features must adhere to the core principles:

1. **Historian, not stock picker** — Never give buy/sell advice
2. **PPT style** — One key point per page, image-first, text as supplement
3. **Ten-second test** — A novice can summarize the core concept after 10 seconds
4. **Beginner-friendly** — All professional terms must have plain-language translations
5. **Correctness > Clarity > Completeness > Aesthetics**

---

## ISSUE-C01: Ex-Dividend Calendar (除權息行事曆)

### Current State Analysis

The Business Card page (`business_card.py`) currently has these sections in order:
1. Header (name, price, watchlist button)
2. One-liner positioning statement
3. Key metrics 3-column cards (PER / Revenue / Dividend Yield)
4. Revenue breakdown (pie chart + descriptions)
5. Revenue trend chart
6. Recent news (plain-language summaries)
7. Disclaimer

The page already shows **dividend yield** in the third card (line 119-127), but it's a single static number with no context about *when* dividends are paid, *how much* historically, or *what the pattern is*. This is exactly the gap competitors like GoodInfo and 財報狗 fill.

### UX Recommendations

#### Where to Place It

**Insert a new section between "Key Metrics" and "Revenue Breakdown"** — after the 3-card row, before the pie chart. This follows the natural reading flow: "What is this company?" → "What are its key numbers?" → "When does it pay dividends?" → "How does it make money?"

Rationale: Dividend information is a **secondary key metric** — it belongs near the top of the page but below the primary financial health indicators. Placing it after revenue breakdown would bury it too deep; placing it above key metrics would disrupt the established visual hierarchy.

#### Visual Layout

**Use a dedicated "Dividend Story" card section** — NOT a dense data table. The PPT-style principle demands we avoid the competitor mistake of showing raw dividend tables (GoodInfo's approach).

Recommended layout:

```
┌─────────────────────────────────────────────────────────┐
│  💵 Dividend Story (配息故事)                            │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  "過去 5 年，台積電每季約發 2.75 元"              │    │
│  │  (Plain-language summary — the "headline")       │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 2.75 元  │  │ 11.0 元  │  │ 3.2%     │              │
│  │ 最近一季  │  │ 預估全年  │  │ 殖利率    │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│                                                         │
│  [展開查看歷史除權息紀錄 ▼]                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │  2024 │ 2.75 元 │ 2024/06/13 │ 除息 │ ✓ 已發放  │    │
│  │  2024 │ 2.75 元 │ 2024/03/14 │ 除息 │ ✓ 已發放  │    │
│  │  2023 │ 2.75 元 │ 2023/12/14 │ 除息 │ ✓ 已發放  │    │
│  │  ...  (最多顯示 5-8 筆)                          │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

#### Component Breakdown

**1. Plain-Language Headline (REQUIRED — PPT Style)**
- A single sentence summarizing the dividend pattern
- Examples:
  - "Over the past 5 years, TSMC has steadily paid ~2.75 NT$ per share each quarter, like a regular allowance"
  - "This company has not paid dividends in the past 3 years, choosing to reinvest profits into expanding operations"
  - "Dividends are inconsistent — sometimes paid, sometimes not, like an irregular bonus"
- This is the **most important element** — it's what passes the 10-second test
- Style: Use the existing tip card pattern (orange `#FFF8F0` background, `#F39C12` left border)

**2. Three Mini-Cards (Secondary)**
- Most recent dividend per share
- Estimated annual dividend (latest quarterly × 4, with TTM note if applicable)
- Current dividend yield (already shown in key metrics — consider deduplicating)
- Style: Use the existing card pattern but smaller (font-size: 1.4rem instead of 1.8rem)

**3. Expandable History Table (Tertiary — Collapsed by Default)**
- Show max 5-8 most recent ex-dividend dates
- Columns: Year | Amount | Ex-Date | Type | Status
- Status indicators: ✓ Paid (已發放) / ⏳ Upcoming Ex-Dividend (即將除息)
- Use `st.expander()` to keep the PPT-style clean
- **Do NOT show this expanded by default** — it violates the "one key point per page" principle

#### What to Avoid (Competitor Mistakes)

| Competitor | Mistake | What We Should Do |
|------------|---------|-------------------|
| GoodInfo | Dense table with 20+ rows of raw data | Show max 5-8 rows, collapsed behind expander |
| GoodInfo | No plain-language explanation | Always lead with a 1-sentence summary |
| 財報狗 | Shows dividend yield prominently but no payment schedule | Show both the "when" and the "how much" |
| CMoney | Focuses on yield for stock-picking | Frame as "understanding the company's cash return pattern" |
| All | Shows stock dividends and cash dividends without explaining the difference | Add a plain-language note: "Stock dividend = additional shares issued to you; Cash dividend = money paid directly to you" (股票股利 = 多給你幾張股票；現金股利 = 直接發錢給你) |

#### Visual Hierarchy

1. **Headline sentence** (largest text, most prominent — this is the "one key point")
2. **Mini-cards** (supporting numbers, smaller)
3. **Expandable table** (detail for curious users, hidden by default)
4. **Educational note** (optional, collapsed: "What is ex-dividend?" (什麼是除權息？) with a 2-sentence explanation)

#### Color Usage

- Use `#3498DB` (blue) for upcoming ex-dividend dates
- Use `#27AE60` (green) for already-paid dividends
- Use `#F39C12` (orange) for the headline card background
- **Do NOT use red/green for dividend amounts** — red/green is reserved for price direction only (per design system Section 3.1)

#### Edge Cases to Handle

- **No dividend history**: Show a friendly message — "This company has not paid dividends in the past 5 years. Some companies choose to reinvest profits into expanding operations or R&D." (這家公司近 5 年沒有配息。有些公司選擇把賺到的錢留在公司，用來擴大經營或研發。)
- **Irregular dividends**: Show the pattern description — "Dividend payments are inconsistent, with no fixed schedule" (配息不穩定，無固定配息模式)
- **Stock dividends only**: Explain the difference in plain language
- **Data unavailable**: Show `st.info("No ex-dividend data available")` (暫無除權息資料) — never show an empty section

#### Integration with Existing Page

The dividend yield card in the current 3-column key metrics (line 119-127) should be **kept as-is** — it shows the current yield snapshot. The new dividend section provides the *story behind the number*. No deduplication needed; they serve different purposes (snapshot vs. narrative).

---

## ISSUE-C02: Notification/Push System (推播通知系統)

### Current State Analysis

The adaptive engine (`adaptive_engine.py`) already detects:
- Revenue anomalies (YoY ±30%)
- Price anomalies (daily ±7%)
- News events (keyword-based severity classification)

Events are stored in `config/events.yaml` with severity levels (high/medium/low). The event dashboard (`event_dashboard.py`) displays them in expandable cards grouped by date.

**The gap:** Events are only visible when the user actively opens the event dashboard. There is no proactive notification. Competitors (財報狗 with Line Notify, CMoney with App Push) all have proactive notification — this is a significant gap for a tool that aims to help users "understand what's happening."

### UX Recommendations

#### Phase 1: Email Notification UI (Settings Page)

**Do NOT add notification settings to the Business Card page.** Notification preferences are a **global setting**, not a per-stock setting. Adding them to the business card would violate the "one key point per page" principle.

**Recommended approach: Add a "Notification Settings" (通知設定) section to the sidebar or a dedicated settings panel.**

However, since the design system specifies that Zone B (sidebar) should only contain navigation, the best approach is:

**Option A (Recommended): Add notification settings as a new tab in the navbar**
- Add "Notification Settings" (通知設定) as a tab alongside existing tabs
- This keeps it accessible but not intrusive
- The tab only appears relevant once the user has watched stocks

**Option B: Add a notification bell icon in Zone A (header)**
- Small 🔔 icon next to the stock name
- Clicking it opens a popover with notification settings
- Less intrusive but may be overlooked by novices

**Option C: Integrate into the existing Event Dashboard page**
- Add a "Notification Settings" (通知設定) button at the top of the event dashboard
- This is the most contextual place — users already thinking about events
- **Recommended for Phase 1** since it requires no new page/tab

#### Notification Settings UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  🔔 Notification Settings (通知設定)                     │
│                                                         │
│  Send notifications to the following address when events occur: │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 📧 Email: [user@example.com          ]           │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  I want to receive notifications for these event types: │
│                                                         │
│  ┌─ Revenue Anomalies (營收異動) ──────────────────────┐    │
│  │  ☑ Revenue YoY change exceeds ±30%                  │    │
│  │  ☐ Revenue declining for 3 consecutive months (advanced) │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─ Price Anomalies (股價異動) ──────────────────────┐    │
│  │  ☑ Single-day price change exceeds ±7%             │    │
│  │  ☐ Price hits alert threshold (set in watchlist)  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─ News Events (新聞事件) ──────────────────────┐    │
│  │  ☑ Major news (acquisition, merger, loss)         │    │
│  │  ☐ Notable news (dividends, orders, partnerships)  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─ Notification Frequency (通知頻率) ──────────────────┐    │
│  │  ○ Immediate (one per event)                        │    │
│  │  ● Daily digest (one email summarizing all events)  │    │
│  │  ○ Weekly digest (one email per week)               │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  [Save Settings]    [Send Test Notification]             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### Component Details

**1. Email Input**
- Single `st.text_input` with email validation
- Show a note: "We will not send spam — only notifications when important events are detected" (我們不會寄送垃圾郵件，只在偵測到重要事件時通知您)
- Validate format before saving

**2. Event Type Toggles**
- Use `st.checkbox` for each event type
- Group by category using the card pattern (blue left border)
- Default: Enable high-severity events, disable medium/low
- Advanced options (consecutive declines, etc.) should be opt-in with a small label: "Advanced" (進階)

**3. Frequency Selector**
- Use `st.radio` for frequency options
- Default: Daily digest (reduces email fatigue — important for novice users who might be overwhelmed)
- Immediate: Only recommend for users with < 5 watched stocks

**4. Action Buttons**
- "Save Settings" (儲存設定) — primary button, saves to `config/notifications.yaml`
- "Send Test Notification" (寄送測試通知) — secondary button, sends a test email to verify the address

#### Notification Email Design

The email itself should follow the same PPT-style philosophy:

```
Subject: [股識] Daily Event Digest — 2026/06/09

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Today's Key Events (3 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Major
📉 TSMC (2330) stock price dropped 7.2% in a single day
   Closing price 850 NT$, down 7.2% from previous close. High volatility — consider reviewing related announcements.
   → View Business Card: https://...

🟡 Notable
📱 Foxconn (2317) revenue YoY declined 35%
   Recent monthly revenue 450 billion NT$, down 35% YoY. Monitor whether this is a short-term factor.
   → View Business Card: https://...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 This is an event summary only and does not constitute investment advice.
   Stock Explorer — Start by understanding the company
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### What to Avoid (Competitor Mistakes)

| Competitor | Mistake | What We Should Do |
|------------|---------|-------------------|
| CMoney | Push notifications feel like stock-picking alerts | Frame all notifications as "something happened to this company" — never "you should buy/sell" |
| 財報狗 | Line Notify is all-or-nothing (no granular control) | Let users choose which event types and frequency |
| JZ Invest | Alert-first design creates anxiety | Default to daily digest, not immediate — reduce noise for novices |
| All | Notifications lack context | Always include the plain-language summary, not just "TSMC -7%" |
| All | No way to disable specific event types | Provide granular toggles per event category |

#### Visual Hierarchy

1. **Email input** (most important — without this, nothing works)
2. **Event type toggles** (core configuration)
3. **Frequency selector** (preference, not critical)
4. **Action buttons** (save/test)

#### Integration with Existing Architecture

- Store settings in `config/notifications.yaml` (new file)
- Create `src/services/notifier.py` with:
  - `send_notification(email, events, frequency)` — sends email via SMTP
  - `check_and_notify()` — called by cron job, checks events.yaml for new events since last notification
  - `send_test_email(email)` — sends a test email
- The cron job (`dev-cycle`) should call `check_and_notify()` periodically
- **Do NOT add Streamlit UI calls to the notifier service layer** (per design system Section 4.2)

#### Phase 2 Considerations (Line Notify — Out of Scope for Now)

- Line Notify requires a Bot account and API key
- The UI should be designed to accommodate a future "Line Token" input field
- Leave a placeholder comment in the code: `# TODO: Phase 2 — Line Notify integration`

---

## ISSUE-C03: Multiple Watchlists (多 Watchlist 清單)

### Current State Analysis

The current watchlist system (`watchlist.py`) stores a flat list in `config/watchlist.yaml`:
```yaml
- stock_id: "2330"
  name: "台積電"
  type: "stock"
  added_date: "2026-06-01"
  alert_above: null
  alert_below: null
```

The watchlist page (`watchlist_page.py`) shows all watched stocks in a single list with summary cards, price info, and alert settings.

**The gap:** Users cannot categorize their watchlists. A novice might want separate lists for "dividend stocks I'm learning about," "companies I actually own," and "tech sector watchlist." Competitors (Yahoo Finance, 財報狗) all support this.

### UX Recommendations

#### Data Structure Change

Refactor `watchlist.yaml` from a flat list to a lists structure:

```yaml
lists:
  - name: "我的關注"
    default: true
    entries:
      - stock_id: "2330"
        name: "台積電"
        type: "stock"
        added_date: "2026-06-01"
  - name: "存股觀察"
    entries:
      - stock_id: "2881"
        name: "富邦金"
        type: "stock"
  - name: "ETF 清單"
    entries:
      - stock_id: "0050"
        name: "元大台灣50"
        type: "etf"
```

**Backward compatibility:** The `load_watchlist()` function should handle both old (flat list) and new (lists structure) formats. On first load of old format, auto-migrate to new format with a single default list named "我的關注" (My Watchlist).

#### Watchlist Page Layout

Replace the single-list view with a **tab-based multi-list view**:

```
┌─────────────────────────────────────────────────────────┐
│  📋 My Watchlist (我的關注)                              │
│                                                         │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                    │
│  │ My   │ │ Divi-│ │ ETF  │ │  ＋  │                   │
│  │ Watch│ │ dend │ │ List │ │ Add  │                   │
│  │ list │ │ Watch│ │      │ │ New  │                   │
│  └──────┘ └──────┘ └──────┘ └──────┘                    │
│                                                         │
│  ── My Watchlist (3 stocks) ──────────────────────────  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Stock  TSMC (2330)                    850.00   │    │
│  │        🔺 Above 900.00                           │    │
│  │  [View Card] [Remove] [🔔 Set Alert]            │    │
│  └─────────────────────────────────────────────────┘    │
│  ...                                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### Component Details

**1. List Tabs (Zone C Top)**
- Use `st.tabs()` for list selection — this is the Streamlit-native pattern
- Each tab shows the list name and count: `My Watchlist (3)` (我的關注 (3))
- Last tab is always `＋ Add New List` (＋ 新增清單) — clicking it shows a dialog to create a new list
- **Do NOT use `st.radio` or button rows** — `st.tabs()` is cleaner and handles overflow better
- Default tab is the `default: true` list (or first list if none marked default)

**2. List Content (Same as Current)**
- Reuse the existing card-based layout from the current watchlist page
- Summary cards (total/stocks/ETFs) should reflect the **current list only**
- All existing functionality (price, alerts, remove, view card) remains unchanged

**3. Create New List**
- Clicking `＋ Add New List` (＋ 新增清單) tab shows:
  - `st.text_input` for list name
  - `st.checkbox` for "Set as default list" (設為預設列表)
  - `st.button` for "Create" (建立) and "Cancel" (取消)
- Validation: Max 20 characters, no duplicate names, no empty names
- After creation, switch to the new tab

**4. List Management**
- Add a `⋮` (kebab menu) button on each tab for list actions:
  - Rename (重新命名)
  - Delete (刪除列表 — with confirmation, cannot delete the last list)
  - Set as default (設為預設)
- Use `st.popover` for the menu

**5. Move Stock Between Lists**
- On each stock card, add a `↕ Move` (移動) button
- Clicking it shows a popover with a list of other lists
- Selecting a list moves the stock (removes from current, adds to target)
- Show `st.toast(f"Moved {name} to {list_name}")` (已將 {name} 移動到 {list_name})

#### Business Card Page Integration

The "Add to Watchlist" (加入關注) button on the Business Card page needs to be updated:

**Current behavior:** Single button → adds to the one watchlist

**New behavior:**
- If user has only 1 list: Button works as before (adds directly, shows toast)
- If user has multiple lists: Button shows a popover with list selection:
  ```
  ➕ Add to Watchlist (加入關注)
  ┌─────────────────────────┐
  │ Select a list to add to: │
  │ ☑ My Watchlist (我的關注) │
  │ ☐ Dividend Watch (存股觀察) │
  │ ☐ ETF List (ETF 清單)    │
  │                         │
  │ [Add] [Cancel]          │
  └─────────────────────────┘
  ```
- Use `st.popover` with `st.checkbox` for each list
- Default: pre-check the user's default list
- Allow adding to multiple lists at once

#### What to Avoid (Competitor Mistakes)

| Competitor | Mistake | What We Should Do |
|------------|---------|-------------------|
| Yahoo Finance | Too many list management features (drag-drop, reorder, color-code) | Keep it simple: create, rename, delete only |
| 財報狗 | Lists are buried in settings, not immediately visible | Show lists as tabs — always visible on the watchlist page |
| CMoney | Portfolio management is complex (cost basis, P&L, etc.) | Phase 1 is just lists — no cost basis or P&L (that's ISSUE-C05, separate) |
| All | No default list concept | Always have a default list; new additions go there unless user specifies |
| All | Deleting a list deletes all stocks silently | Confirmation dialog + option to move stocks to another list |

#### Visual Hierarchy

1. **List tabs** (primary navigation — which list am I viewing?)
2. **Summary cards** (context — how many stocks in this list?)
3. **Stock cards** (content — the actual stocks)
4. **Action buttons** (per-stock operations)

#### Empty States

- **No lists at all:** Show the current empty state message (already implemented) but change "Add to Watchlist" (加入關注) to guide users to browse categories
- **Empty list (specific tab):** Show "No stocks in this list yet. Browse categories or ETF listings to find stocks of interest." (此列表尚未加入任何股票。前往分類瀏覽或 ETF 瀏覽找到有興趣的標的。)
- **Last list deletion:** Prevent with `st.error("At least one list must be kept")` (至少需要保留一個列表)

#### Color Usage

- Active tab: Use Streamlit's default tab styling (no custom CSS needed)
- The `＋ Add New List` (＋ 新增清單) tab: Use a lighter color or italic text to distinguish it from data tabs
- Keep existing card colors (blue border for stocks, green for ETFs)

---

## Cross-Cutting Concerns

### 1. Loading States (All 3 Features)

Per design system Section 4.1, all data loading must show a spinner:
- **C01 (Dividend data):** Show `st.spinner("Loading ex-dividend data...")` (載入除權息資料...) when fetching dividend history from FinMind
- **C02 (Notification test):** Show `st.spinner("Sending test notification...")` (寄送測試通知...) when sending test email
- **C03 (Watchlist with many lists):** Show `st.spinner("Loading watchlist...")` (載入關注列表...) when loading watchlist data

### 2. Error Handling (All 3 Features)

Per design system Section 4.4:
- **C01:** If FinMind dividend API fails, show `st.info("No ex-dividend data available")` (暫無除權息資料) — never crash
- **C02:** If SMTP fails, show `st.error("Unable to send notification — please check email settings")` (無法寄送通知，請檢查 Email 設定) — include the specific error
- **C03:** If YAML migration fails, show `st.error("Watchlist failed to load — please check config/watchlist.yaml")` (關注列表載入失敗，請檢查 config/watchlist.yaml) — fall back to empty list

### 3. Mobile Responsiveness (All 3 Features)

- **C01:** The 3 mini-cards should stack vertically on narrow screens (use `st.columns` with responsive behavior)
- **C02:** The notification settings form should use full width on mobile (avoid multi-column layouts)
- **C03:** Tabs should scroll horizontally on mobile (Streamlit's `st.tabs()` handles this natively)

### 4. Accessibility

- All emoji icons must have text labels (don't rely on emoji alone)
- All interactive elements must have unique `key` attributes (per design system Section 3.2)
- Color is never the sole indicator — always pair with text or icons

---

## Implementation Sequencing Recommendation

### Sprint 1 (This Week)

| Order | Feature | Task | Effort |
|-------|---------|------|--------|
| 1 | C01 | Add dividend data fetching to `finmind_client.py` | Low |
| 2 | C01 | Add dividend section to `business_card.py` | Medium |
| 3 | C03 | Refactor `watchlist.py` data structure + migration | Medium |
| 4 | C03 | Update `watchlist_page.py` with tabs | Medium |
| 5 | C03 | Update `business_card.py` watchlist button for multi-list | Low |

### Sprint 2 (Next Week)

| Order | Feature | Task | Effort |
|-------|---------|------|--------|
| 6 | C02 | Create `config/notifications.yaml` schema | Low |
| 7 | C02 | Create `src/services/notifier.py` (SMTP) | Medium |
| 8 | C02 | Add notification settings UI to event dashboard | Medium |
| 9 | C02 | Add notification check to cron job | Low |

### Rationale

- **C01 first:** It's a pure UI addition on the business card — no architectural changes, low risk, high visibility
- **C03 before C02:** The watchlist refactor is a prerequisite for meaningful notification (users want to be notified about specific lists)
- **C02 last:** It requires the most new infrastructure (SMTP, cron integration, new service file)

---

## Summary of Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| C01: Dividend section between key metrics and revenue breakdown | Natural reading flow; secondary key metric placement |
| C01: Plain-language headline as primary element | PPT-style "one key point" principle |
| C01: History table collapsed by default | Avoid data overload for novices |
| C02: Settings in event dashboard (not new page) | Contextual placement; no new tab needed for Phase 1 |
| C02: Daily digest as default frequency | Reduces email anxiety for novices |
| C02: Granular event type toggles | More control than competitor all-or-nothing approaches |
| C03: `st.tabs()` for list navigation | Streamlit-native; handles overflow; cleanest UX |
| C03: Backward-compatible YAML migration | No data loss for existing users |
| C03: Multi-list add on business card | Users can add to multiple lists without navigating away |

---

*This design review was produced by analyzing the existing design system, competitor research, current codebase architecture, and product vision. All recommendations align with the "historian, not stock picker" positioning and the PPT-style design philosophy.*
