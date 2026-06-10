import os
import sqlite3
import re
from datetime import datetime
from pathlib import Path

DB_PATH = "memory.db"
DOCS_DIR = "docs"

def init_db(conn):
    cursor = conn.cursor()
    # 建立文件索引表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doc_index (
            file_path TEXT PRIMARY KEY,
            category TEXT,
            title TEXT,
            summary TEXT,
            last_modified TIMESTAMP
        )
    ''')
    conn.commit()

def parse_markdown(file_path):
    title = "Untitled"
    summary = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 擷取第一個 # 開頭的作為標題
            title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            
            # 抓取前 100 字作為摘要 (過濾掉 metadata、空行、標題)
            lines = [line.strip() for line in content.split('\n') 
                     if line.strip() and not line.startswith('#') and not line.startswith('---') and not line.startswith('name:') and not line.startswith('description:')]
            if lines:
                summary = ' '.join(lines)[:100] + '...'
                
    except Exception as e:
        pass
    return title, summary

def build_index():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    cursor = conn.cursor()
    
    # 清空重建，確保沒有幽靈檔案 (Desync 防護)
    cursor.execute("DELETE FROM doc_index")
    
    docs_path = Path(DOCS_DIR)
    count = 0
    for md_file in docs_path.rglob('*.md'):
        category = md_file.parent.name
        filepath_str = str(md_file.as_posix())
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
        
        title, summary = parse_markdown(md_file)
        
        cursor.execute('''
            INSERT INTO doc_index (file_path, category, title, summary, last_modified)
            VALUES (?, ?, ?, ?, ?)
        ''', (filepath_str, category, title, summary, mtime))
        count += 1
        
    conn.commit()
    
    print(f"✅ SQLite Memory Index built successfully! {count} files indexed into {DB_PATH}.\n")
    print("🔍 [TEST QUERY] System Architect looking for UI/UX related decisions:")
    print("-" * 80)
    
    # 測試：模擬 Agent 查詢所有在 decisions 裡面且標題跟 UI 或是 Design 有關的歷史決策
    query = """
        SELECT category, title, summary, file_path 
        FROM doc_index 
        WHERE category = 'decisions' 
          AND (title LIKE '%Design%' OR file_path LIKE '%ui%' OR file_path LIKE '%ux%')
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    if not results:
        # 如果沒搜到，退而求其次印出部分內容
        cursor.execute("SELECT category, title, file_path FROM doc_index WHERE category IN ('decisions', 'architecture') LIMIT 5")
        results = cursor.fetchall()
        for row in results:
            print(f"[{row[0].upper()}] {row[1]}\n   -> Path: {row[2]}\n")
    else:
        for row in results:
            print(f"[{row[0].upper()}] {row[1]}")
            print(f"   -> Summary: {row[2]}")
            print(f"   -> Path: {row[3]}\n")
        
    conn.close()

if __name__ == "__main__":
    build_index()
