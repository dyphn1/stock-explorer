# Stock Explorer — Challenger 3-Round Challenge: C36-C47 Feature Directions

> **作者**: Challenger  
> **日期**: 2026-06-15  
> **對象**: PM 初步決策 — Sprint 12-14 三大方向  
> **參考文件**: product_vision.md, handoff.md, feasibility_c36_c47.md, design_review_c36_c47.md, developer_c36_c47_analysis.md

---

## 前言：背景摘要

PM 綜合建築師、設計師、開發者意見後，得出以下初步結論：

- 12 項競品功能（C36-C47）中，**9 項已完工**（C37、C38、C39、C41、C42、C43、C44、C45）
- 1 項部分完成（C40 簡易/詳細模式已作，缺 navbar 切換）
- 3 項全新構建（C36 Revenue Tree、C46 Moat Analysis、C47 Education Academy）
- 4 項需要投入：C36（12-16h）、C40（6-10h）、C46（14-18h）、C47（22-32h）

**PM 提出的 Sprint 12-14 三大方向：**

| 方向 | Sprint | 內容 | 工時 |
|------|--------|------|------|
| A: Ten-Second Company Page | Sprint 12 | QA/Polish C37/C39/C43/C45 + C40 navbar toggle | ~20-30h |
| B: Historian's Deep Dive | Sprint 13 | C36 Revenue Tree + C46 Moat Analysis | ~26-34h |
| C: Education Platform | Sprint 14 | C47 Education Academy MVP（7 lessons + scaffold） | ~22-32h |

**總剩餘工時：~68-96h（3 個 Sprint）**

---

## 第一輪挑戰：功能方向挑戰

### 🎯 Challenger 問題

**Q1: 「9/12 已完工」的結論是否準確？是否存在「做出來」vs「做好」的差距？**

開發者報告確實列出了 9 項有 service + page layer 的實現。但設計師的 review 中明確指出 **Risk 1: Feature Overload on Business Card Page** — C37 + C39 + C43 + C45 都想放在頁面頂部，可能造成資訊過載。這暗示這些功能雖然「已完工」，但**整合度和 UX 成熟度可能不足**。

> 挑戰：PM 將 Sprint 12 定位為「QA/polish」，但實際可能觸及**架構層面的整合問題**（Business Card 頁面卡片堆疊、資訊層級、progressive disclosure）。20-30h 是否足夠？

**Q2: 三個方向是否真正對齊「historian, not stock picker」定位？**

- Direction A（Ten-Second Page）的核心是**資訊密度優化** — 這偏向 UX 設計，與「historian」定位間接相關但非直接強化。
- Direction B（Revenue Tree + Moat）直接強化「historian」— 解釋公司的商業模式和競爭優勢從何而來。
- Direction C（Education Academy）是**教育平台** — 設計師給 C47 的 DP4（Historian）評分是 ⭐⭐⭐，但 CV5（Benchmark）只有 ⭐。

> 挑戰：Direction A 本質上是一個**通用 UX 優化方向**，而不是「historian」特有的差異化方向。是否應該將 Direction A 降級為 Sprint 12 的「附帶任務」而非獨立方向？

**Q3: C36（Revenue Tree）和 C46（Moat）是否應該在同一 Sprint 開發？**

可行性報告將 C36 + C46 放在同一 Sprint（Direction D），理由是兩者都是「公司本質深度分析」。但：
- C36 的**最大風險是資料源不足**（FinMind 無客戶層級營收拆分，需手動策展 top 20）
- C46 的**最大風險是質化分析的客觀性**（護城河本質是主觀判斷）
- 兩者面對的**風險類型完全不同**：一個是資料工程問題，一個是內容品質問題

> 挑戰：將兩個高風險項目放在同一 Sprint 是否合理？如果 C36 的資料源問題比預期嚴重，是否會拖累 C46？

**Q4: 是否有更好的功能分組方式？**

PM 的分組是：
- A: Polish + C40（可用性）
- B: C36 + C46（深度分析）
- C: C47（教育平台）

但開發者提出了另一種分組：
- Bundle 1: C46 + C43/44 polish（Health & Moat Pack）— 因為 C46 複用 C43 的評分框架
- Bundle 2: C36 + C47（Education Double Feature）— 因為兩者都是教育性質
- Bundle 3: C40 + C42 polish（Discovery & Accessibility）

> 挑戰：PM 的分組邏輯是「使用者旅程層次」（先優化頁面 → 再深度分析 → 再教育平台），而開發者的分組邏輯是「技術複用」（shared infrastructure）。哪種分組更能降低風險？

**Q5: 團隊是否應該在現階段構建新功能？還是應該先解決整合問題？**

Handoff.md 中的 Sprint 11 計劃包含 D16（split analogy_engine.py）和 D24（extract business_card.py）— 這兩項架構債務直接影響 C40 和 C47 的開發。如果 Sprint 11 的架構債務未完成，Sprint 12 的 C40 navbar toggle 可能會在未穩定的架構上開發。

> 挑戰：Sprint 12 的「polish」方向是否應該改為「架構債務 + 整合驗證」？C40 是否應該推遲到架構穩定後再開發？

---

### 📝 團隊回應（模擬）

**A1: 「9/12 已完工」的準確性**
團隊承認「已完工」指的是 service + page layer 存在且通過 L0/L1 測試，但同意「整合度」可能不足。設計師的 Risk 1（Feature Overload）是有效的 concern。團隊回應：Sprint 12 的「polish」應包含「Business Card 頁面資訊層級重排」，這需要額外 4-6h 的設計工作。修訂後的 Sprint 12 工時為 24-36h。

**A2: Direction A 的定位**
團隊同意 Direction A 的「historian」對齊度較弱。但強調 C40（Beginner/Expert Mode）是**所有其他功能的基礎設施** — 沒有 mode toggle，C36/C46/C47 的內容在初學者面前會顯得過於複雜。因此 Direction A 的價值不僅是「UX 優化」，更是**漸進式揭露（progressive disclosure）的基礎建設**。

**A3: C36 + C46 同 Sprint 的風險**
團隊承認風險不同但可以互補：C36 需要資料工程，C46 需要內容創作。兩者並行可以充分利用 Sprint 的「資料準備期」和「內容創作期」重疊。但如果 C36 的資料源問題在 Sprint 第 1 週確認不可行，團隊會啟動 fallback（改用手動策展 pie chart 替代 treemap）。

**A4: 分組方式**
團隊比較了兩種分組後，認為 PM 的分組（A/B/c）更符合**使用者旅程邏輯**：先讓現有頁面變好（Sprint 12），再增加深度（Sprint 13），最後擴展到教育（Sprint 14）。開發者的技術複用分組雖然效率更高，但可能導致使用者體驗的「跳躍感」— 使用者突然看到 C36 和 C46 同時出現，缺乏漸進式引入。

**A5: 架構債務優先**
團隊確認 Sprint 11 的 D16 + D24 必須在 Sprint 12 開始前完成。Sprint 12 的 C40 開發將依賴 D24（business_card.py 提取）的完成。如果 D16/D24 延遲，C40 的開發會受到影響。團隊建議在 Sprint 12 第 1 天進行**架構債務完成確認 gate**，如果未完成，C40 延後到 Sprint 13。

---

### ⚖️ 第一輪判決：✅ CONFIRMED（附帶條件）

**理由：**
1. 三大方向的分組邏輯（可用性 → 深度分析 → 教育平台）符合使用者旅程，優於純技術複用分組
2. Sprint 12 的「polish」方向需要明確包含 Business Card 頁面資訊層級重排
3. C36 + C46 同 Sprint 的風險可透過 fallback 機制管控

**條件：**
- **條件 1**: Sprint 12 必須包含 Business Card 頁面資訊層級重排（設計師 Risk 1 的緩解措施），額外 4-6h
- **條件 2**: C40 的開發必須在 D24（business_card.py 提取）完成後開始，Sprint 12 第 1 天設架構債務完成確認 gate
- **條件 3**: C36 必須定義明確的 fallback 策略（資料源不足時退化為現有 pie chart），避免 Sprint 13 被 C36 資料問題阻塞

---

## 第二輪挑戰：優先順序挑戰

### 🎯 Challenger 問題

**Q1: Sprint 12（polish）是否應該是第一優先？還是應該先做最高價值的新功能 C46？**

PM 的順序是 A → B → C，理由是「先整合再擴展」。但：
- C46（Moat Analysis）被開發者標記為 **🔴 Highest priority** — 完美的「historian」差異化功能，沒有台版競品有
- Sprint 12 的 polish 工作（C37/C39/C43/C45 QA）本質上是**維護性工作**，不產生新的用戶可感知價值
- 設計師的 Tier 1 清單中，C37 和 C43 是「Must-Have (Next Sprint)」— 但它們已經完工了

> 挑戰：如果目標是「讓產品更好」，為什麼不先做用戶可感知的新價值（C46），而是先做內部 QA？

**Q2: C40 Beginner/Expert Mode 影響所有頁面 — 它真的是「quick win」嗎？**

PM 將 C40 放在 Sprint 12，預估 6-10h。但：
- 開發者明確指出 C40 的**最大風險是 cross-section coupling** — 必須包裝所有 `_render_*` 函數
- 設計師指出 C40 需要**條件渲染邏輯**，影響所有頁面
- 開發者建議使用 `@section_visibility("expert_only")` decorator pattern — 這需要額外的架構工作
- 如果 D24（business_card.py 提取）還未完成，C40 的影響面會更大

> 挑戰：C40 的 6-10h 估計是否包含了「在所有 section 中實作條件渲染」的工作量？還是僅估計了 toggle UI 本身？

**Q3: C47 Education Academy 是最大的單項 — 是否應該拆分到更多 Sprint？**

PM 將 C47 放在 Sprint 14，預估 22-32h。但：
- 開發者建議 C47 拆分：Part 1（scaffold + 7 lessons）和 Part 2（remaining lessons + quiz）
- 設計師給 C47 的 ROI 排名是 **#12（最低）** — 因為 effort 最大
- 內容創作佔 40-50% 工時（9-13h），這是**外部依賴**（需要撰寫者），不是開發團隊能完全控制的

> 挑戰：22-32h 在一個 Sprint 中完成 C47 MVP 是否現實？如果內容創作延遲，是否會阻塞整個 Sprint？

**Q4: 團隊是否考慮過「功能疲勞」（feature fatigue）風險？**

從 Sprint 3 到 Sprint 10，團隊已經交付了 C44、C41、C38、C51、C53-1、C48、C71、C74、C73、C83、C85、C02、C43、C45、C84、D3、D6、D7、D-044、D-048、D6、D-055、D-050、D8/D9/D10、D-057、C103、C101、C98、C34、C105 — 大量功能在短時間內密集交付。

> 挑戰：用戶是否已經被這麼多新功能「淹沒」？Sprint 12-14 是否應該包含一個「用戶反饋收集」階段，而不是繼續構建？

**Q5: Sprint 12 和 Sprint 13 的依賴關係是否被低估？**

- Sprint 12 做 polish + C40
- Sprint 13 做 C36 + C46
- Sprint 14 做 C47

但 C40（mode toggle）直接影響 C36 和 C46 的呈現方式 — 在 beginner mode 下，Revenue Tree 和 Moat Analysis 應該如何簡化？如果 C40 在 Sprint 12 完成，Sprint 13 的 C36/C46 開發需要考慮 beginner mode 的適配。

> 挑戰：Sprint 13 的 C36/C46 是否需要額外的「beginner mode 適配」工作？這是否在 26-34h 的估計中？

---

### 📝 團隊回應（模擬）

**A1: Sprint 12 優先 vs C46 優先**
團隊重新評估後承認 C46 的用戶可感知價值高於 Sprint 12 的 polish 工作。但 Sprint 12 的 C40 是 C36/C46 的基礎設施 — 沒有 mode toggle，C36/C46 在初學者面前的體驗會打折扣。團隊提出**折衷方案**：Sprint 12 可以同時進行 polish + C46 開發（而非等 polish 完成才開始 C46），因為 C46 的開發主要是 service layer + content，不依賴 Business Card 頁面的 polish 狀態。

**A2: C40 的真實工時**
團隊承認 6-10h 的估計主要覆蓋 toggle UI + session_state 管理。在所有 section 中實作條件渲染需要額外 4-6h（auditing all `_render_*` functions + decorator pattern）。修訂後的 C40 估計為 **10-16h**。这也解釋了為什麼開發者將 C40 標記為「worst coupling, best done last」。

**A3: C47 拆分**
團隊同意開發者的建議，將 C47 拆分：
- Sprint 13: C47 Part 1（scaffold + 7 lessons）— 14-18h
- Sprint 14: C47 Part 2（remaining lessons + quiz）— 8-12h
但這意味著 Sprint 13 需要同時做 C36 + C46 + C47 Part 1，工時增加到 40-52h — **超出一個 Sprint 的合理範圍**。

**A4: 功能疲勞**
團隊承認這個風險。設計師的 Risk 1（Feature Overload）某種程度上反映了這個問題。團隊建議在 Sprint 12 中加入「用戶反饋收集機制」— 在 Business Card 頁面加入簡單的反饋按鈕（👍/👎），收集用戶對現有功能的感受。這需要額外 2-4h。

**A5: C40 → C36/C46 的依賴**
團隊確認 C40 的完成會簡化 C36/C46 的 beginner mode 適配 — 因為 C40 建立了 `_mode` key contract 和 decorator pattern。C36/C46 只需要使用 `@section_visibility` 即可。這大約增加 2-3h 的適配工作（已包含在 C36/C46 的估計中）。

---

### ⚖️ 第二輪判決：❌ REJECTED → 需要修訂

**理由：**
1. C40 的工時嚴重低估（6-10h → 10-16h），Sprint 12 的總工時需要修訂
2. Sprint 13 如果同時做 C36 + C46 + C47 Part 1，工時 40-52h 超出合理範圍
3. 功能疲勞風險需要具體緩解措施

**需要修訂的項目：**
- **修訂 1**: C40 工時從 6-10h 調整為 10-16h
- **修訂 2**: C47 必須拆分，但不能將 Part 1 塞入 Sprint 13
- **修訂 3**: Sprint 12 加入用戶反饋收集機制（2-4h）

---

## 第三輪挑戰：目標對齊挑戰

### 🎯 Challenger 問題

**Q1: 這個計劃是否推進「Story first, data second」核心價值？**

Product vision 的 Core Value #1 是「Story first, data second」— 每個分析點都從現實世界的例子開始。

- C36 Revenue Tree：設計師給 CV1 評分 ⭐⭐⭐ — 天然的故事格式（「錢從哪裡來」）
- C46 Moat Analysis：設計師給 CV1 評分 ⭐⭐⭐ — 「城堡與護城河」是純故事
- C47 Education Academy：設計師給 CV1 評分 ⭐⭐⭐ — 每堂課用真實股票例子
- C40 Beginner/Expert：設計師給 CV1 評分 ⭐⭐ — 只是簡化，不是故事

> 挑戰：Sprint 12 的 polish 工作（C37/C39/C43/C45 QA）是否包含「story first」的 QA gate？還是只是功能測試？

**Q2: 這個計劃是否服務「十秒測試」設計原則？**

Product vision 的驗證原則是「十秒測試」— 初學者能在十秒內重述核心概念。

- C37 Key Takeaways：設計師說「**This IS the ten-second test**」— 但已經完工
- C43 Company Snowflake：設計師說「**This IS the ten-second test perfected**」— 但已經完工
- C39 What Changed：設計師給 DP1 評分 ⭐⭐⭐ — 但已經完工
- C45 Valuation Band：設計師給 DP1 評分 ⭐⭐⭐ — 但已經完工

> 挑戰：Sprint 12-14 的**新功能**（C36、C46、C47）中，哪些真正服務於「十秒測試」？C36 的 treemap 可能需要 30 秒才能理解層級結構。C47 的課程是**深度學習**，不是十秒測試。

**Q3: 三個方向之間是否存在矛盾？**

- Direction A 說「讓頁面更簡潔」（C40 beginner mode 只顯示 3-4 個核心指標）
- Direction B 說「增加深度分析」（C36 Revenue Tree + C46 Moat Analysis — 兩個新的深度 section）
- Direction C 說「構建教育平台」（C47 — 全新的頁面）

> 挑戰：Direction A 在**減少**頁面資訊量，Direction B 在**增加**頁面資訊量。這兩個方向是否矛盾？如果 C40 beginner mode 隱藏了 C36 和 C46，那 C36/C46 的價值是否被削弱？

**Q4: 是否存在被忽視的風險？**

- **內容創作瓶頸**：C36（4-6h 內容）+ C46（6-8h 內容）+ C47（9-13h 內容）= **19-27h 純內容創作**。這需要領域專家撰寫，不是開發團隊能獨立完成的。
- **手動策展可擴展性**：C36 和 C46 都只手動策展 top 20。當用戶搜尋 top 20 以外的股票時，會看到**空白或 fallback**。這是否會破壞用戶體驗？
- **用戶引導**：這麼多新功能（C36/C46/C47/C40）同時推出，用戶是否知道它們存在？需要 onboarding 或引導流程。

> 挑戰：19-27h 的內容創作是否有明確的負責人？如果內容創作延遲，Sprint 是否會變成「開發完成但內容空白」？

**Q5: Daniel（客戶）會怎麼看這個計劃？**

根據 product vision.md 和 handoff.md：
- Daniel 的核心要求是「historian, not stock picker」
- Daniel 強調「ten-second test」作為驗證原則
- Daniel 強調「iterative cycle over waterfall」— 每個功能實施後要驗證
- Daniel 要求「content = 40% of effort」for education features

> 挑戰：Daniel 可能會問「為什麼要花 20-30h 在 polish 上，而不是花 20-30h 在用戶研究上？」— 因為 9/12 功能已經 built，但**沒有人驗證過它們是否真的幫助了初學者**。

---

### 📝 團隊回應（模擬）

**A1: Story first QA gate**
團隊同意在 Sprint 12 的 polish 工作中加入「story first」QA gate — 每個已完工功能的內容必須通過「十秒重述測試」：一個初學者能否在十秒內重述每個 bullet point 的核心含義。這需要 2-4h 的 QA 工作。

**A2: 十秒測試與新功能的關係**
團隊承認 C36/C46/C47 不是「十秒測試」的直接載體 — 它們是**深度分析**功能。但它們的**呈現方式**必須通過十秒測試：
- C36 的 treemap 必須有「一句話解釋」— 「這家公司 40% 收入來自晶圓代工」
- C46 的護城河必須有「一句話總結」— 「TSMC 的護城河來自技術領先」
- C47 的每堂課必須有「一句話核心概念」— 「本益比 = 回本年限」

團隊認為這些「一句話解釋」是「十秒測試」在深度分析層面的延伸。

**A3: Direction A 與 Direction B 的矛盾**
團隊承認表面矛盾但認為實際是**互補**：
- Direction A 的 C40 beginner mode 在**初學者首次訪問時**隱藏 C36/C46
- 當用戶**主動探索**（點擊「查看更多」或切換到 expert mode）時，C36/C46 才出現
- 這正是「progressive drill-down」設計原則的實現：先簡潔，再深度

但團隊也承認這需要**明確的資訊架構設計** — C36/C46 在 beginner mode 下是完全隱藏，還是以簡化形式出現？這需要設計師在 Sprint 12 定義。

**A4: 內容創作風險**
團隊承認 19-27h 的內容創作是**最大風險**。緩解措施：
- C36 和 C46 使用 **template-based fallback** — 自動生成基礎內容，手動優化 top 20
- C47 使用 **analogy_engine 複用** — 利用現有的類比引擎生成課程內容的初步版本
- 內容創作與開發**並行** — Sprint 第 1 週開始內容創作，開發同步進行

**A5: Daniel 的觀點**
團隊認為 Daniel 可能會同意這個計劃的方向，但會要求：
- 每個 Sprint 必須有**明確的驗證標準**（不是只是「shipped」）
- Sprint 12 應該包含**用戶測試**（至少 5 個初學者）
- 內容創作必須有**明確的負責人和時間表**

---

### ⚖️ 第三輪判決：✅ CONFIRMED（附帶重大條件）

**理由：**
1. 三個方向整體上對齊「historian」定位 — C36/C46/C47 都是深度分析功能
2. Direction A 與 B 的「矛盾」實際上是 progressive drill-down 的實現
3. 內容創作風險可以透過 template-based fallback 和並行開發緩解

**重大條件：**
- **條件 1**: 每個 Sprint 必須包含**用戶驗證**（至少 5 個初學者測試），而非只是內部 QA
- **條件 2**: 內容創作必須有**明確的負責人、時間表、和 review 流程** — 不能只是「40% of effort」的模糊承諾
- **條件 3**: C36/C46 的 template-based fallback 必須在 Sprint 13 第 1 週完成，確保非 top-20 股票有基本內容
- **條件 4**: Sprint 12 必須定義 C36/C46 在 beginner mode 下的**資訊架構**（完全隱藏 vs 簡化形式）

---

## 最終判決

### ✅ CONFIRMED（附帶修訂）

PM 的初步決策 — 三個方向（Ten-Second Page → Historian's Deep Dive → Education Platform）— **方向正確，但需要以下修訂**：

### 修訂清單

| # | 修訂項目 | 原方案 | 修訂方案 |
|---|---------|--------|---------|
| 1 | **Sprint 12 工時** | 20-30h | **26-38h**（加入資訊層級重排 4-6h + C40 修正 4-6h + 用戶反饋 2-4h） |
| 2 | **C40 工時** | 6-10h | **10-16h**（包含所有 section 的條件渲染 + decorator pattern） |
| 3 | **Sprint 12 gate** | 無 | **架構債務完成確認 gate**（D16/D24 必須完成） |
| 4 | **Sprint 13 範圍** | C36 + C46（26-34h） | **C36 + C46 + C47 內容創作啟動**（30-40h，但 C47 內容創作佔 8-12h） |
| 5 | **Sprint 14 範圍** | C47 MVP（22-32h） | **C47 Part 2 + C40 完善 + 用戶驗證**（20-28h） |
| 6 | **用戶驗證** | 無 | **每個 Sprint 包含 5 人初學者測試** |
| 7 | **內容創作管理** | 40% of effort（模糊） | **明確負責人 + 時間表 + review 流程** |
| 8 | **C36 fallback** | 無 | **資料源不足時退化為現有 pie chart** |
| 9 | **Beginner mode 資訊架構** | 未定義 | **Sprint 12 定義 C36/C46 在 beginner mode 下的呈現方式** |

### 修訂後的 Sprint 計劃

| Sprint | 內容 | 修訂後工時 | 關鍵 Gate |
|--------|------|-----------|-----------|
| **Sprint 12** | C37/C39/C43/C45 QA + 資訊層級重排 + C40 navbar toggle + 用戶反饋機制 | 26-38h | D16/D24 完成確認 |
| **Sprint 13** | C36 Revenue Tree + C46 Moat Analysis + C47 內容創作啟動 | 30-40h | C36 資料源確認（第 1 週） |
| **Sprint 14** | C47 Part 2（remaining lessons + quiz）+ C40 完善 + 用戶驗證 | 20-28h | C47 內容 review 通過 |

**修訂後總工時：~76-106h（3 個 Sprint）**

### Challenger 最終評論

PM 的初步決策在**方向上是正確的** — 先優化現有功能，再構建深度分析，最後擴展到教育平台。這個順序符合「iterative cycle over waterfall」的開發哲學。

但存在三個關鍵問題：
1. **工時估計過於樂觀** — 特別是 C40 的 cross-section coupling 和 C47 的內容創作量
2. **風險管理不足** — C36 資料源、C47 內容創作、C40 全域影響都需要明確的 fallback 和緩解措施
3. **用戶驗證缺失** — 9/12 功能已經 built，但**沒有人被驗證過它們是否真的幫助了初學者**

修訂後的計劃解決了這些問題，但需要團隊在每個 Sprint 中投入額外的時間在**用戶驗證**和**風險管理**上。這是「historian, not stock picker」定位的根本要求 — 不是構建更多功能，而是確保每個功能**真正幫助初學者理解公司**。

---

*Challenge completed: 2026-06-15*  
*Challenger verdict: ✅ CONFIRMED with 9 revisions*
