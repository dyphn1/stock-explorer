"""
src/plugins/
Plugin 目錄 — 每個子目錄是一個獨立 Plugin。

目錄結構：
    src/plugins/
    ├── __init__.py          # 套件標記
    ├── business_card/       # 公司名片
    │   └── plugin.py        # BusinessCardPlugin(BasePlugin)
    ├── operation_checkup/   # 營運健檢
    │   └── plugin.py
    └── ...

每個 plugin 目錄必須包含 plugin.py，其中定義一個 BasePlugin 子類。
Registry 會自動掃描此目錄。
"""

# 此文件標記 src/plugins/ 為 Python package。
# PluginRegistry.discover() 會掃描此目錄下的所有子目錄。
