# ADR-006: 瀏覽器返回按鈕支援

## 狀態
已接受

## 日期
2026-06-12

## 背景

使用者點擊瀏覽器返回按鈕時，頁面沒有正確回到上一頁，而是直接關閉應用程式。這是因為 Streamlit 的 `st.session_state` 與瀏覽器 URL 不同步。

## 決策

使用 `st.query_params` 與 `st.session_state` 雙向同步，實現瀏覽器返回按鈕支援。

## 實作方式

```python
# URL → session（頁面載入時）
def sync_url_to_session():
    params = st.query_params
    if "page" in params:
        st.session_state["page"] = params["page"]
    if "stock_id" in params:
        st.session_state["stock_id"] = params["stock_id"]

# session → URL（導航時）
def navigate_to(page: str, stock_id: str = None):
    st.session_state["page"] = page
    if stock_id:
        st.session_state["stock_id"] = stock_id
    st.query_params["page"] = page
    if stock_id:
        st.query_params["stock_id"] = stock_id
    st.rerun()
```

## 理由

1. **使用者預期**：瀏覽器返回按鈕應該要能正常運作
2. **可分享性**：URL 包含頁面狀態，可以分享連結
3. **簡單性**：不需要額外的路由套件

## 後果

- ✅ 瀏覽器返回/前進按鈕正常運作
- ✅ 可透過 URL 分享特定頁面
- ⚠️ 需要每個導航操作都同時更新 session 和 query_params
