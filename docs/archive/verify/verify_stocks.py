"""
自動化驗證：測試三支代表性股票 (2330, 2454, 1101) 的資料管道
驗證所有 FinMind API 呼叫、資料處理、圖表生成是否正常運作
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from src.data.finmind_client import FinMindClient
from src.services.chart import (
    create_revenue_pie_chart,
    create_revenue_trend_chart,
    create_price_chart,
    create_funnel_chart,
    create_institutional_chart,
)
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
)
from src.services.news_summarizer import summarize_news, get_news_impact_level

STOCKS = [
    ("2330", "台積電", "半導體業"),
    ("2454", "聯發科", "半導體業"),
    ("1101", "台泥", "建材營造"),
]

results = []


def test_stock(client, stock_id, stock_name, industry):
    """測試單一股票的所有資料管道"""
    errors = []
    warnings = []
    info = []

    # 1. 股票基本資訊
    try:
        stock_info = client.get_stock_info(stock_id)
        if len(stock_info) == 0:
            errors.append("找不到股票基本資訊")
            return errors, warnings, info
        info.append(f"✅ 基本資訊: {stock_info.iloc[0]['stock_name']} / {stock_info.iloc[0]['industry_category']}")
    except Exception as e:
        errors.append(f"基本資訊錯誤: {e}")
        return errors, warnings, info

    # 2. 最新價格
    try:
        latest_price = client.get_latest_price(stock_id)
        if latest_price:
            info.append(f"✅ 最新價格: {latest_price['close']:,.0f} ({latest_price['date']})")
        else:
            warnings.append("無最新價格資料")
    except Exception as e:
        warnings.append(f"價格錯誤: {e}")

    # 3. PER/PBR
    try:
        latest_per_pbr = client.get_latest_per_pbr(stock_id)
        if latest_per_pbr:
            per = latest_per_pbr.get("PER")
            pbr = latest_per_pbr.get("PBR")
            dy = latest_per_pbr.get("dividend_yield")
            info.append(f"✅ PER/PBR: PER={per}, PBR={pbr}, 殖利率={dy}")
        else:
            warnings.append("無 PER/PBR 資料")
    except Exception as e:
        warnings.append(f"PER/PBR 錯誤: {e}")

    # 4. 月營收
    try:
        monthly_revenue = client.get_monthly_revenue(stock_id)
        if len(monthly_revenue) > 0:
            latest_rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            info.append(f"✅ 月營收: {len(monthly_revenue)} 筆, 最新={latest_rev:,.0f} 億")
        else:
            warnings.append("無月營收資料")
    except Exception as e:
        warnings.append(f"月營收錯誤: {e}")

    # 5. 日收盤價
    try:
        daily_price = client.get_daily_price(stock_id)
        if len(daily_price) > 0:
            info.append(f"✅ 日收盤價: {len(daily_price)} 筆")
        else:
            warnings.append("無日收盤價資料")
    except Exception as e:
        warnings.append(f"日收盤價錯誤: {e}")

    # 6. 損益表
    try:
        financial = client.get_financial_statement(stock_id)
        if len(financial) > 0:
            info.append(f"✅ 損益表: {len(financial)} 筆")
        else:
            warnings.append("無損益表資料")
    except Exception as e:
        warnings.append(f"損益表錯誤: {e}")

    # 7. 資產負債表
    try:
        balance_sheet = client.get_balance_sheet(stock_id)
        if len(balance_sheet) > 0:
            info.append(f"✅ 資產負債表: {len(balance_sheet)} 筆")
        else:
            warnings.append("無資產負債表資料")
    except Exception as e:
        warnings.append(f"資產負債表錯誤: {e}")

    # 8. 新聞
    try:
        news = client.get_news(stock_id)
        if len(news) > 0:
            info.append(f"✅ 新聞: {len(news)} 筆")
        else:
            warnings.append("無新聞資料")
    except Exception as e:
        warnings.append(f"新聞錯誤: {e}")

    # 9. 三大法人
    try:
        institutional = client.get_institutional_investors(stock_id)
        if len(institutional) > 0:
            info.append(f"✅ 三大法人: {len(institutional)} 筆")
        else:
            warnings.append("無三大法人資料")
    except Exception as e:
        warnings.append(f"三大法人錯誤: {e}")

    # 10. 營收組成分析
    try:
        revenue_items = analyze_revenue_breakdown(financial, stock_id, industry)
        if revenue_items:
            items_str = ", ".join([f"{item['name']}({item['value']:.0f}%)" for item in revenue_items])
            info.append(f"✅ 營收組成: {items_str}")
        else:
            warnings.append("營收組成為空")
    except Exception as e:
        warnings.append(f"營收組成錯誤: {e}")

    # 11. 一句話定位
    try:
        one_liner = get_one_liner(stock_id, stock_name, industry)
        info.append(f"✅ 一句話定位: {one_liner[:50]}...")
    except Exception as e:
        warnings.append(f"一句話定位錯誤: {e}")

    # 12. 圖表生成
    try:
        if revenue_items:
            fig = create_revenue_pie_chart(revenue_items, f"{stock_name} 營收來源")
            info.append("✅ 圓餅圖生成成功")
    except Exception as e:
        warnings.append(f"圓餅圖錯誤: {e}")

    try:
        if len(monthly_revenue) > 0:
            fig = create_revenue_trend_chart(monthly_revenue, f"{stock_name} 月營收趨勢")
            info.append("✅ 營收趨勢圖生成成功")
    except Exception as e:
        warnings.append(f"營收趨勢圖錯誤: {e}")

    try:
        if len(daily_price) > 0:
            fig = create_price_chart(daily_price, f"{stock_name} 股價走勢")
            info.append("✅ 股價走勢圖生成成功")
    except Exception as e:
        warnings.append(f"股價走勢圖錯誤: {e}")

    try:
        if len(institutional) > 0:
            fig = create_institutional_chart(institutional, f"{stock_name} 三大法人")
            info.append("✅ 三大法人圖生成成功")
    except Exception as e:
        warnings.append(f"三大法人圖錯誤: {e}")

    # 13. 生活化比喻
    try:
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            analogy = get_per_analogy(per)
            info.append(f"✅ PER 比喻: {analogy[:40]}...")
    except Exception as e:
        warnings.append(f"PER 比喻錯誤: {e}")

    try:
        if len(monthly_revenue) > 0:
            rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            analogy = get_revenue_analogy(rev, industry)
            info.append(f"✅ 營收比喻: {analogy[:40]}...")
    except Exception as e:
        warnings.append(f"營收比喻錯誤: {e}")

    # 14. 新聞摘要
    try:
        if len(news) > 0:
            title = news.iloc[0]["title"]
            summary = summarize_news(title, stock_name)
            impact = get_news_impact_level(title)
            info.append(f"✅ 新聞摘要: [{impact}] {summary[:50]}...")
    except Exception as e:
        warnings.append(f"新聞摘要錯誤: {e}")

    return errors, warnings, info


def main():
    print("=" * 60)
    print("股識 Stock Explorer — 自動化驗證報告")
    print("測試股票: 2330 台積電, 2454 聯發科, 1101 台泥")
    print("=" * 60)

    try:
        client = FinMindClient(cache_dir=".cache")
    except Exception as e:
        print(f"❌ FinMind Client 初始化失敗: {e}")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0

    for stock_id, stock_name, industry in STOCKS:
        print(f"\n{'─' * 50}")
        print(f"📊 測試 {stock_id} {stock_name} ({industry})")
        print(f"{'─' * 50}")

        errors, warnings, info = test_stock(client, stock_id, stock_name, industry)

        for i in info:
            print(f"  {i}")
        for w in warnings:
            print(f"  ⚠️  {w}")
        for e in errors:
            print(f"  ❌ {e}")

        total_errors += len(errors)
        total_warnings += len(warnings)

    print(f"\n{'=' * 60}")
    print(f"總結: {total_errors} 個錯誤, {total_warnings} 個警告")
    if total_errors == 0:
        print("✅ 所有核心功能通過驗證！")
    else:
        print("❌ 有錯誤需要修復")
    print(f"{'=' * 60}")

    return total_errors == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
