# Challenger Round 1 — Challenge Report

**Date:** 2026-06-10
**Challenger:** Challenger sub-agent (gpt-oss-120b)
**Context:** PM proposes implementing 3 P0 features (C01, C02, C03) in order C01 → C03 → C02

---

## Challenge 1: Priority Order — Is C01 Really the Right First Feature?

**The PM says:** C01 (dividend calendar, 1-2h) is the quickest win, so do it first.

**My challenge:** Why are we doing ANY new features right now? The tech debt report just identified **7 HIGH severity issues**, 2 of which are directly in `get_stock_data()` — the function that ALL pages depend on. Specifically:

1. **Silent exception swallowing in `get_stock_data()`** — 10 sequential API calls where ONE failure kills the entire page. This is on the critical path of every single feature we're about to build. If we add new API calls to this function (dividend data for C01?), we're making this WORSE.
2. **Sequential API calls** — 5-15 seconds per page load. Adding MORE API calls by implementing C01 will increase load times.

**The real question is:** Are we building new features on a broken foundation? The tech debt report recommends "Immediate (Next Sprint — 1 day)" cleanup of 7 items taking ~2 hours. Why is the PM proposing to skip this and jump straight to features?

**Counter-proposal:** Do the 2-hour "Immediate" tech debt cleanup FIRST (items 1-7 from the tech debt report), THEN implement C01. This is a 2-hour investment that makes every subsequent feature faster to build and less bug-prone.

---

## Challenge 2: Scope — Is This Too Much for One Sprint?

**The PM says:** 3 features, roughly 7-10 hours total (C01: 1-2h, C02: 3-4h, C03: 3-4h).

**My challenge:** 

1. These are PM ESTIMATES with no developer validation. The Developer hasn't reviewed the actual code to confirm feasibility. Has anyone checked:
   - What does `business_card.py` actually look like? How easy is it to add a new section?
   - Does `FinMind TaiwanStockDividend` actually work on the free tier? The competitor research says "需確認免費 tier 是否包含" but I don't see confirmation anywhere.
   - Does the `watchlist.yaml` refactoring in C03 touch `watchlist.py` which already has a known ETF bug? Yes — `current_problems.md` Issue #2 and Issue #3 directly implicate `watchlist.py`.

2. **C02 (Notifier) is severely under-estimated.** Building an email notification system involves:
   - SMTP configuration (credentials, security)
   - Email template design
   - Background worker implementation
   - User configuration UI (email address input, notification preferences)
   - Testing (how do you test email sending in a cron-based dev cycle?)
   - Error handling (what if SMTP is down? retry logic?)
   
   This is NOT 3-4 hours. This is 3-4 hours if everything goes perfectly AND you already know the codebase intimately. In reality, this is more like 6-8 hours.

3. **We have 10 TODO items in the issue tracker, all from competitor research done 1 day ago.** Are we seriously going to implement all 10 items without Daniel's input on priorities? That's a LOT of churn.

---

## Challenge 3: Dependencies — Does C02 Really Depend on C03?

**The PM says:** C01 → C03 → C02 (C02 depends on C03).

**My challenge:** WHERE does the dependency come from?

- **C02** is about email notifications for events (revenue ±30%, price ±7%). It depends on `adaptive_engine.py` and creates `src/services/notifier.py`.
- **C03** is about refactoring `watchlist.yaml` from a flat list to a `lists` structure. It touches `watchlist.py`, `watchlist_page.py`, and `business_card.py`.

These are COMPLETELY independent code paths. The notifier doesn't care about watchlists at all — it sends emails about events. The watchlist refactoring doesn't affect the event detection engine.

**Unless** the PM is thinking "notifications should notify about watchlist items" — but that's a different feature (watchlist-specific notifications), which is NOT what C02 describes. C2 is about EVENT notifications, not watchlist notifications.

**My assessment:** The dependency claim is bogus. C01, C02, and C03 are independent. If anything, C02 should be done LAST because it's the most complex and has the most unknowns.

---

## Challenge 4: Are All 3 Items Truly P0?

Let me re-examine the evidence:

### C01: Dividend Calendar — P0 ✅ (mostly justified)
- GoodInfo and 财報狗 both have it
- "One of the most common beginner questions" — and Stock Explorer can't answer it
- Data is available (FinMind TaiwanStockDividend)
- **However:** The competitor research itself notes "需確認免費 tier 是否包含". If this API requires paid tier, the whole feature is blocked. P0 rating is premature.

### C02: Notification System — P0 ❓ (questionable)
- Event detection EXISTS but can't push notifications
- However, Stock Explorer has no user accounts, no login, no email addresses. HOW do you send notifications to users?
- This is a fundamentally architectural problem. The app is a single-user local Streamlit app. Who gets the email? Daniel, running it locally?
- If we're building a notification system with no defined recipient, infrastructure, or delivery mechanism, this is NOT P0 — it's a research/spike task.
- **Suggested reclassification: P1** (or even a design spike before any implementation)

### C03: Multiple Watchlists — P0 ❌ (NOT P0)
- Yahoo Finance and 财報狗 support multiple watchlists
- BUT: Stock Explorer is an educational tool, not a portfolio tracker. The use case "I want to track dividend stocks separately from growth stocks" is a nice-to-have, not a critical gap.
- The current single watchlist works fine for educational exploration
- **Suggested reclassification: P1** (it's useful but NOT critical — no competitor gap analysis says users are churning because of this)

**Summary:** Only C01 truly deserves P0. C02 should be P1 with a design spike first. C03 should be P1.

---

## Challenge 5: Daniel Hasn't Confirmed Priorities

This is the biggest issue of all.

From `STATUS.md` line 373: "See `docs/status/issues.md` for 10 new items labeled `source: competitor research`"
From `STATUS.md` line 382: "⏳ Awaiting Daniel's Input — New feature prioritization"
From `STATUS.md` line 373: "10 competitor-research features in `docs/status/issues.md`"

**The PM is proposing to implement 3 of 10 features that Daniel has NOT reviewed yet.** Not only that, the PM is assigning P0 priorities to features that the REPORT itself says need confirmation (C01's data feasibility is unconfirmed, C02's infrastructure requirements are undefined, C03 is a nice-to-have).

**My position:** We should NOT implement ANY of these features until Daniel reviews and confirms priorities. The proper workflow is:
1. Present the 10 items to Daniel with priority RECOMMENDATIONS
2. Daniel reviews and says "yes, these 3 are P0" or "no, I want C05 and C06 instead"
3. THEN we implement

Implementing features Daniel hasn't approved wastes effort on potentially wrong things. We already have a mechanism for this: `pending_review.md`.

---

## Challenge 6: Should Tech Debt Cleanup Come First?

The tech debt report specifically recommends "Immediate (Next Sprint — 1 day)" with 7 items taking ~2 hours. Two of these are code duplication issues that will DIRECTLY affect the features we're building:

1. **`_find_value` / `_find_financial_value` duplicated across 4 files** — If C01 needs to look up dividend data from DataFrames, it will either add a 5th duplication or need to use the existing broken system.
2. **Card helpers duplicated across 4+ files** — C01 requires adding a new card section to `business_card.py`. Will we add it with the duplicated helpers or the canonical ones?

**My position:** Yes, the 2-hour Immediate tech debt cleanup MUST come before any new feature work. This is non-negotiable. Building features on top of duplicated, fragile code guarantees bugs and rework.

---

## Challenge 7: Timeline Filter Bug and Event Engine Issues

From `current_problems.md`:
- **Issue #9 (High):** Timeline filter silently fails — charts don't update, no error shown (UX Issue 9) — marked as P1-7 and supposedly fixed
- **Issue #4 (High):** DuplicateWidgetID crash in event dashboard — marked as P0-1 and supposedly fixed

**My question:** These were SUPPOSED to be fixed in the 2026-06-09 P0/P1 fixes. Has Daniel actually VERIFIED these fixes work? The STATUS.md says all fixes are "code complete" but Daniel hasn't done manual testing. If these core interaction bugs are still present in practice, adding new features (especially C01 which depends on `business_card.py` rendering) is premature.

---

## Challenge 8: Notification System — Fundamental Architectural Concern

Let's dig deeper into C02. Stock Explorer is:
- A Streamlit single-user local app
- No user authentication
- No user database
- No background worker infrastructure (it runs via Streamlit's single-process model)

Building `src/services/notifier.py` as a "background worker + SMTP" requires:
1. A process that runs INDEPENDENTLY of Streamlit
2. A way to store user email addresses (currently the app has no concept of users)
3. A way to store notification preferences
4. A triggering mechanism (when does the notifier check? schedule? on every page load? cron?)

None of this infrastructure exists. The PM's estimate of "3-4 hours" suggests they think this is just "write some SMTP code and call it done." This is a massive underestimate that ignores the architectural requirements.

**My position:** C02 should be DEPRIORITIZED until after we have:
1. A clear architectural plan for background processing in a Streamlit app
2. A user configuration system (at minimum: email address + notification preferences storage)
3. Confirmation that Daniel actually wants email notifications (maybe he doesn't — he runs the app locally)

---

## Summary of Challenges

| # | Challenge | Severity | My Position |
|---|-----------|----------|-------------|
| 1 | Priority order — tech debt before features | HIGH | Do 2h tech debt cleanup FIRST |
| 2 | Scope too large — estimates unvalidated | HIGH | Developer must validate estimates before sprint planning |
| 3 | C02 dependency on C03 is bogus | MEDIUM | All 3 are independent; dependency chain is artificial |
| 4 | Not all 3 items are truly P0 | HIGH | C01=P0, C02=P1 (needs spike), C03=P1 |
| 5 | Daniel hasn't confirmed ANY of these | CRITICAL | Halt implementation until Daniel reviews the 10 items |
| 6 | Tech debt cleanup must come first | HIGH | Non-negotiable 2h investment |
| 7 | P0/P1 fixes may not be verified | HIGH | Daniel needs to verify before new features |
| 8 | C02 has massive hidden complexity | HIGH | Needs architecture design spike, not implementation |

---

## My Verdict

**🛑 DO NOT PROCEED WITH IMPLEMENTATION — YET.**

The PM is trying to sprint before the starting gun. Here's what I recommend instead:

### Immediate Actions (Before Any Implementation)
1. **Wait for Daniel's review** of all 10 competitor-research features in `issues.md`
2. **Do the 2-hour Immediate tech debt cleanup** (7 items from `tech_debt.md`) — this is quick and high-value regardless of which features we implement
3. **Downgrade C02 to P1** and schedule a design spike for the notification architecture
4. **Downgrade C03 to P1** — it's useful but not critical
5. **Verify C01's data feasibility** — confirm `TaiwanStockDividend` API works on FinMind free tier
6. **Get developer validation** of all 3 time estimates before committing to a sprint

### After Daniel's Confirmation
- Implement in order: C01 → C03 → C02 (the original order is fine IF Daniel approves)
- BUT do the tech debt cleanup FIRST (only 2 hours)
- AND do a design spike for C02 before implementation

---

*Challenger out. Waiting for team response before Round 2.*
