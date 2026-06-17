# ADR-005: i18n 使用 YAML 單一檔案 per locale

## 狀態
已接受

## 日期
2026-06-14

## 背景

專案目前有 3,146 處 hardcoded 中文字串散佈在 93 個 Python 檔案中。需要建立國際化（i18n）機制。

## 決策

使用 **YAML 單一檔案 per locale** 的方式管理翻譯字串。

## 架構

```
src/core/i18n.py          # i18n 核心模組（唯一出入口）
locales/
├── zh-TW.yaml            # 繁體中文（預設）
└── en.yaml               # 英文
```

**不使用資料夾分類**（如 `locales/zh-TW/ui.yaml`）——單一檔案 per locale 是最簡單的方案。未來如果超過 500 行再拆分。

## 命名規範

```
<module>.<submodule>.<component>.<purpose>
```

範例：
- `pages.business_card.title` — 名片頁標題
- `pages.router.nav_label` — 導航標籤
- `errors.no_data` — 無數據錯誤

## 使用方式

```python
from src.core.i18n import t

# 基本使用
st.markdown(t("pages.business_card.title"))

# 帶參數
st.markdown(t("pages.stock.price", price=100))
```

## 替代方案

| 方案 | 不選原因 |
|------|----------|
| Python dict | 無法與程式碼分離，不易維護 |
| JSON | 不支援註解，可讀性較差 |
| 資料庫 | MVP 階段過度設計 |
| 多檔案 per locale | 增加查找成本 |

## 後果

- ✅ 簡單易維護
- ✅ 可切換語言
- ⚠️ 需要將 3,146 處 hardcoded 字串逐一替換
- ⚠️ 需要團隊紀律：新增 UI 字串必須用 `t()`
