#!/usr/bin/env python3
"""
データベース初期化スクリプト
"""

import sqlite3
import os

def init_database():
    """サンプルデータベースを初期化"""
    # データベースファイルを作成
    db_path = "company_data.db"
    
    # 既存のデータベースがある場合は削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # データベース接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 従業員テーブルを作成
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary INTEGER NOT NULL,
            hire_date TEXT NOT NULL
        )
    """)
    
    # プロジェクトテーブルを作成
    cursor.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            start_date TEXT NOT NULL,
            end_date TEXT,
            status TEXT NOT NULL
        )
    """)
    
    # サンプルデータを挿入
    employees_data = [
        (1, "山田太郎", "開発部", "シニアエンジニア", 8000000, "2020-04-01"),
        (2, "佐藤花子", "開発部", "テックリード", 9500000, "2018-07-15"),
        (3, "田中一郎", "営業部", "営業マネージャー", 7500000, "2019-01-10"),
        (4, "鈴木美咲", "人事部", "人事スペシャリスト", 6500000, "2021-03-01"),
        (5, "高橋健太", "開発部", "ジュニアエンジニア", 5000000, "2022-04-01")
    ]
    
    projects_data = [
        (1, "ECサイト刷新", "既存ECサイトのフルリニューアル", "2023-01-01", "2023-12-31", "進行中"),
        (2, "モバイルアプリ開発", "新しいモバイルアプリケーションの開発", "2023-06-01", "2024-03-31", "進行中"),
        (3, "データ分析基盤構築", "ビッグデータ分析のためのインフラ構築", "2022-10-01", "2023-05-31", "完了"),
        (4, "セキュリティ強化", "システム全体のセキュリティ向上", "2023-04-01", "2023-09-30", "完了"),
        (5, "AI チャットボット", "カスタマーサポート用AIチャットボット", "2023-08-01", "2024-02-29", "進行中")
    ]
    
    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", employees_data)
    cursor.executemany("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)", projects_data)
    
    # 変更を保存
    conn.commit()
    conn.close()
    
    import sys
    sys.stderr.write(f"Database '{db_path}' initialized successfully\n")
    sys.stderr.write(f"Employees: {len(employees_data)}\n")
    sys.stderr.write(f"Projects: {len(projects_data)}\n")

if __name__ == "__main__":
    init_database()