# Stock Explorer 技術可行性分析報告：C36-C47

> **作者**: System Architect  
> **日期**: 2026-06-14  
> **狀態**: Sprint 11 規劃階段（Sprint 10 ✅ 完成）

---

## 一、執行摘要

12 項新功能候選（C36-C47）中，**8 項已實作完成**（C37、C38、C39、C41、C42、C43、C44、C45），**1 項部分完成**（C40 的簡易/詳細模式已作但無navbar切換），**3 項未開始**（C36、C46、C47）。本報告針對尚未完成的功能進行深度分析，並提出 Sprint 12-14 的功能方向建議。

---

## 二、功能可行性完整表格

### 表 1：已完成功能（既有基礎設施）

| ID | 功能 | 程式可行性 | 架構配合度 | 資料源狀態 | 綜合評級 |
|------|------|-----------|-----------|-----------|---------|
| **C37** | Key Takeaways 重點摘要 | ✅ 已完成 | `key_takeaways.py` + `_render_takeaways()` | 精選 20 檔 + 自動生成 | 🟢 |
| **C38** | Compare Stories 同業比較故事 | ✅ 已完成 | `compare_stories.py` + `_render_compare_stories()` | FinMind 同業資料 + analogy_engine | 🟢 |
| **C39** | Delta Card 最近變化 | ✅ 已完成 | `delta_engine.py` + `_render_deltas()` | 月營收、日股價（既有） | 🟢 |
| **C41** | Read Next 推薦閱讀 | ✅ 已完成 | `_render_read_next()` + `company_facts.yaml` | 同產業查詢 + 精選 facts | 🟢 |
| **C42** | Stock Screener 選股引擎 | ✅ 已完成 | `stock_screener_service.py` + `stock_screener.py` | `BatchAPI` + `get_stock_info()` 全量 | 🟢 |
| **C43** | Snowflake 健康圖 | ✅ 已完成 | `health_scoring.py` + `chart.create_health_snowflake()` | extra_metrics、financial、monthly_revenue | 🟢 |
| **C44** | Risk Analysis 風險分析 | ✅ 已完成 | `risk_analyzer.py`（567行）+ `_render_risk()` | financial、cash_flow、news、institutional | 🟢 |
| **C45** | Valuation Band Chart 估值區間 | ✅ 已完成 | `chart.create_valuation_band_chart(787行)` + `_render_valuation()` | daily_price + financial（TTM EPS） | 🟢 |

### 表 2：待實作/部分完成功能

| ID | 功能 | 預估工時 | 技術可行性 | 架構配合度 | 資料源狀態 | 依賴條件 | 綜合評級 |
|------|------|---------|-----------|-----------|-----------|---------|---------|
| **C36** | Visual Revenue Tree | 10-14h | 🟡 中 | 🟡 需新增 chart + 手動策展 | 🟡 FinMind 營收拆分有限，需手動補足 20 檔 | `chart.py` 擴展 + `company_facts.yaml` 擴展 | 🟡 |
| **C40** | Beginner/Expert Mode Toggle | 10-14h | 🟢 低（已有基礎） | 🟡 需擴大到 navbar + session_state | 🟢 無新資料需求 | 依賴 C105 擴大範圍 | 🟢 |
| **C46** | Moat Analysis 護城河 | 12-16h | 🟡 中 | 🟡 需新增 service + 手動策展 | 🟢 ROE/毛利率等（既有）+ 手動策展 20 檔 | `moat_analyzer.py` + `moat_data.yaml` | 🟡 |
| **C47** | Financial Education Academy | 20-30h | 🔴 高（內容創作量大） | 🟡 需全新 page + content pipeline | 🟢 無新 API 需求，需要 YAML 課程內容 | `academy_service.py` + `academy_lessons.yaml` | 🔴 |

---

## 三、逐項深度分析

### C36: Visual Revenue Tree（視覺化營收樹）

**技術可行性：🟡 Medium**

| 維度 | 評估 |
|------|------|
| **Service Layer** | 需在 `chart.py` 新增 `create_revenue_treemap()` 函數。Plotly Express 原生支援 `treemap` 和 `sunburst`，技術無風險 |
| **Data Layer** | **關鍵瓶頸**：FinMind API 無提供客戶/產品線層級的營收拆分資料。現有 `monthly_revenue` 只有總營收 |
| **Content** | 需手動策展 top 20 檔的階層式營收資料（類似 `company_facts.yaml`），預估內容創作 4-6h |
| **Presentation** | 需在 `_financial.py` 新增 `_render_revenue_tree()` + `_sections/__init__.py` 註冊 |
| **Architectural Fit** | 完全符合分層架構。新 chart function 在 service，渲染在 presentation |

**風險**：資料源不足是最大風險。FinMind 的 `taiwan_stock_financial_statement` 雖有損益表明細，但客戶層級資料需從年報手動整理。

**建議方案**：Phase 1 用手動策展的 YAML（top 20 檔）+ fallback 到現有 pie chart；Phase 2 考慮爬蟲自動化。

---

### C40: Beginner/Expert Mode Toggle（新手/專家模式切換）

**技術可行性：🟢 Low（基本已完成）**

| 維度 | 評估 |
|------|------|
| **目前狀態** | C105 已實現 `簡易/詳細` toggle（在 `_main.py` 內 `st.toggle`），功能等同 C40 |
| **Gap 分析** | C40 描述的是 navbar 層級的全局切換 + 更激進的簡化（只顯示 3-4 個核心指標） |
| **Service Layer** | 無需新 service |
| **Presentation** | 需將 toggle 從 card 頁面提升到 navbar（`_helpers.py` 或 sidebar），影響所有頁面 |
| **Architectural Fit** | Router 層級 session_state 管理，符合架構規範 |

**風險**：幾乎無技術風險。主要工作為 UX 範圍擴大和 session_state 影響面的測試。

**建議**：將 C105 重新定位為 C40 的 MVP，Sprint 12 完成 navbar 整合。

---

### C46: Moat Analysis（護城河分析）

**技術可行性：🟡 Medium**

| 維度 | 評估 |
|------|------|
| **Service Layer** | 需新增 `moat_analyzer.py`，分析五大護城河類型（技術、品牌、成本、網路效應、轉換成本）。可複用 `analogy_engine` 做類比 |
| **Data Layer** | 量化指標：ROE、毛利率趨勢、市場佔有率（既有 FinMind 資料）。質化分析需手動策展 |
| **Content** | 需新增 `moat_data.yaml`（top 20 檔護城河描述）。內容創作約 6-8h |
| **Presentation** | 新增 `_render_moat()` section 或 standalone page |
| **Architectural Fit** | 完全符合分層架構 |

**風險**：護城河本質是質化分析，無法完全自動化。需手動策展 + template-based fallback。

**建議方案**：Phase 1 手動 20 檔 + template（基於 ROE/毛利率/資本支出自動判斷護城河類型）；Phase 2 擴展到全市場。

---

### C47: Financial Education Academy（財金教育學院）

**技術可行性：🔴 High Risk / High Effort**

| 維度 | 評估 |
|------|------|
| **Service Layer** | 需新增 `academy_service.py`（課程管理、進度追蹤、quiz 引擎） |
| **Data Layer** | 大量結構化課程內容（`academy_lessons.yaml`），預估 10-15 課，每課 2000-3000 字。內容創作 8-12h |
| **Presentation** | 全新 standalone page `academy_page.py`（類似 `stock_screener.py` 結構），含課程列表、內容渲染、互動 quiz |
| **State Management** | 需 session_state 追蹤學習進度 |
| **Architectural Fit** | 獨立頁面，router 層級管理。需注意 content 與邏輯分離 |

**風險**：
1. **內容創作量大**（佔 40-50% 工時）：需要撰寫高品質的财教內容
2. **互動設計複雜**：quiz 系統、進度追蹤需額外 UI 元件
3. **維護成本高**：課程內容需持續更新

**建議**：Phase 1 MVP 為 5 課結構化課程 + 靜態渲染（無 quiz）；Phase 2 加入互動元素。

---

## 四、基礎設施需求分析

### 現有基礎設施即可支援
- C36（部分）：`chart.py` + `company_facts.yaml`
- C40：C105 已實作，只需擴展
- C46（量化部分）：`analogy_engine.py` + 既有 metrics

### 需要新增的基礎設施

| 需求 | 用途 | 優先度 | 預估工時 |
|------|------|--------|---------|
| `data/moat_data.yaml` | 護城河手動策展資料 | P2 | 6-8h（內容）|
| `data/academy_lessons.yaml` | 教育學院課程內容 | P3 | 8-12h（內容）|
| `services/moat_analyzer.py` | 護城河分析邏輯 | P2 | 6-8h（開發）|
| `services/academy_service.py` | 課程管理邏輯 | P3 | 4-6h（開發）|
| `pages/academy_page.py` | 教育學院頁面 | P3 | 6-8h（開發）|
| `services/chart.py` 擴展 | `create_revenue_treemap()` | P2 | 4-6h（開發）|

### 不需要變更的既有服務
- `finmind_client.py`：無需新 API 方法
- `_router_base.py`：資料載入模式已支援
- `health_scoring.py`：C43 已完成，可複用
- `risk_analyzer.py`：C44 已完成，可複用
- `key_takeaways.py`：C37 已完成，可複用

---

## 五、架構影響評估

### 無需架構變更
所有候選功能均可納入現有的四層架構（Presentation → Router → Service → Data）。

### 建議的微調

#### 5.1 策展資料集中管理
目前手動策展資料分散在 `company_facts.yaml`、`key_takeaways._KEY_TAKEAWAYS`（hardcode）中。建議：

```
data/
  curated/
    company_facts.yaml      # Did You Know facts
    revenue_breakdown.yaml  # C36 營收樹資料（新增）
    moat_analysis.yaml      # C46 護城河資料（新增）
    academy_lessons.yaml    # C47 課程內容（新增）
```

**影響**：低風險，僅為資料組織調整。`company_facts.yaml` 可保留並向後相容。

#### 5.2 Page 層級的模式切換上下文
C40 擴大到 navbar 後，需要在 router 層級傳遞 `expert_mode` 到所有 page。建議在 `_router_base.get_stock_data()` 中加入 `mode` 參數：

```python
data["_mode"] = st.session_state.get("expert_mode", "beginner")
```

**影響**：極低風險，僅為 dict 新增 key。

#### 5.3 Content Feature 的開發規範
C36、C46、C47 都需要大量手動內容。建議建立內容開發規範：
- 每個 content feature 需建立對應 YAML 資料檔
- YAML 結構需經 designer + domain expert review
- 開發工時的 40% 預算給內容創作（handoff.md 已規定）

---

## 六、功能方向提案（Sprint 12-14）

### Direction D: Revenue Deep Dive + Moat（Sprint 12）
**主題**：營收結構可視化 + 競爭優勢分析

| Sprint | 功能 | 預估工時 | 優先度 |
|--------|------|---------|--------|
| Sprint 12 | C36 Visual Revenue Tree | 10-14h | P2 |
| Sprint 12 | C40 Navbar Mode Toggle 擴展 | 4-6h | P2 |
| Sprint 12 | C46 Moat Analysis | 12-16h | P2 |

**理由**：
- C36 + C46 都屬於「公司本質深度分析」主題，和現有 business card page 高度整合
- C36 的 treemap chart 和 C46 的護城河分析共同構成「公司競爭力全貌」
- 兩者都依賴手動策展，可併行開發資料檔
- C40 extension 工時小但 UX 影響大，可作為 Sprint 12 的「quick win」

**技術風險**：低-中。最大風險為手動策展資料的品質和完整性。

---

### Direction E: Education Platform Foundation（Sprint 13）
**主題**：結構化財金教育內容平台

| Sprint | 功能 | 預估工時 | 優先度 |
|--------|------|---------|--------|
| Sprint 13 | C47 Financial Education Academy MVP | 20-30h | P2 |

**MVP 範圍**：
- 5 堂結構性課程（「什麼是股票？」「營收vs獲利」「ROE的意義」「本益比怎麼看」「什麼是股息？」）
- 每課以真實台股為例（reuse analogy engine）
- 靜態渲染（無 quiz/interactive），聚焦內容品質
- Standalone page 含課程列表 + 內容頁

**理由**：
- 競品分析顯示 Investopedia Academy / Stockopedia Academy 證明市場需求
- 無任何台灣競品有結構化學習路徑
- 與 Stock Explorer「歷史學家」定位完美契合
- 內容創作工時大，獨立一個 Sprint 確保品質

**技術風險**：中。主要風險在內容開發進度和品質控制。

---

### Direction F: Advanced Narrative + Automation（Sprint 14+，可選）
**主題**：進階敘事功能 + 自動化資料更新

可包含但不限於：
- C36 Phase 2：上傳年度報告自動解析營收拆分（需要 PDF parser）
- C46 Phase 2：全市場自動化護城河評分
- C47 Phase 2：互動 quiz + 學習進度追蹤

**理由**：這些是長期方向，需要更多基礎設施建設，適合在 Sprint 14+ 討論。

---

## 七、功能排序：技術風險 vs. 價值矩陣

```
高價值 │  C43 ✅    C46 🎯
       │  C44 ✅    C36 🎯
       │  C42 ✅    C47 📋
       │  C38 ✅    
       │  C37 ✅    C40 🔧
低價值 │  C39 ✅    C41 ✅
       └──────────────────
        低風險      高風險
```

| 象限 | 功能 | 建議 |
|------|------|------|
| 🟢 高價值/低風險（已完成）| C37、C38、C42、C43、C44、C45 | 持續維護，監控測試覆蓋 |
| 🎯 高價值/中風險（推薦）| C36、C46 | **Sprint 12 優先開發** |
| 🔧 中價值/低風險（推薦）| C40 | **Sprint 12 附帶完成** |
| 📋 高價值/高風險（計劃）| C47 | **Sprint 13 獨立開發** |

---

## 八、十大風險與建議

### 🔴 高風險

1. **C36 資料源不足**: FinMind 無客戶層級營收拆分。**建議**：Phase 1 手動策展 top-20，Phase 2 爬蟲或半自動解析
2. **C47 內容創作量大**: 20-30h 中 40-50% 是內容。**建議**：Sprint 13 獨立開發 + 內容先行（第 1-2 週撰寫，第 3-4 週開發）
3. **全量股票 API 速率限制**: C42 已遇過 rate limit（已有 fallback）。**建議**：Sprint 12 強化 `BatchAPI` 的 rate limit handling

### 🟡 中風險

4. **手動策展資料的擴展性**: C36/C46 手動策展僅 top-20。**建議**：建立 template-based fallback（基於量化指標自動生成）
5. **C40 navbar 切換的全域影響**: 所有 page 需配合。**建議**：Sprint 12 開始前先建立存取規範（`_mode` key contract）
6. **C46 護城河分析的客觀性**: 質化分析可能有偏見。**建議**：僅描述可量化事實，維持歷史學家語態

### 🟢 低風險

7. **Plotly treemap 效能**: 20 節點的 treemap 無效能問題
8. **YAML 資料檔的版本控制**: 需加入 code review 流程
9. **Sprint 並行開發**: C36 和 C46 可在同一 Sprint，資料檔可並行製作
10. **架構相容性**: 所有功能均可在四層架構內完成，無需重構

---

## 九、Sprint 建議

### Sprint 12（建議）— Revenue Deep Dive + Moat
| Item | 工時 | 類型 |
|------|------|------|
| C36 Visual Revenue Tree | 12h（開發 8h + 內容 4h）| Feature |
| C46 Moat Analysis | 14h（開發 8h + 內容 6h）| Feature |
| C40 Navbar Mode Toggle | 5h | Enhancement |
| **Total** | **~31h** | |

### Sprint 13（建議）— Education Platform Alpha
| Item | 工時 | 類型 |
|------|------|------|
| C47 Education Academy MVP | 25h（開發 12h + 內容 13h）| Feature |
| **Total** | **~25h** | |

### Sprint 14+（可選）— Advanced Features
- C36 Phase 2：自動營收拆分
- C46 Phase 2：全市場護城河
- C47 Phase 2：互動 quiz + 進度追蹤

---

## 十、結論

Stock Explorer 的現有架構健全（L0: 91/91, L1: 18/18），C36-C47 中的 8 項已完成並達設計 A 級。剩餘 4 項均可在不下層架構的情況下實作，其中：

- **優先開發**：C36 + C46（公司本質深度分析，高差異化價值）
- **快速完成**：C40 擴展（已 80% 完工）
- **獨立 Sprint**：C47（教育平台，內容為王）

全部 12 項功能的程式風險均為 🟡 以下，真正的挑戰在於手動策展內容的品質與時程控制。建議維持 content = 40% of effort 的原則。
