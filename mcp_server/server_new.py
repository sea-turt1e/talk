#!/usr/bin/env python3
"""
MCPサーバーサンプルコード（最新版）
会社データベースから情報を取得するMCPサーバー
"""

import json
import os
import sqlite3
from typing import Any, Dict, List

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from text_to_sql import TextToSQLConverter

load_dotenv()

# サーバーインスタンスを作成
mcp = FastMCP("company-data-server")


# データベースパス（絶対パス）
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "company_data.db")

# Text-to-SQLコンバータのインスタンスを作成
text_to_sql_converter = TextToSQLConverter(db_path=DB_PATH)


def get_db_connection():
    """データベース接続を取得"""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file '{DB_PATH}' not found. Please run 'python database.py' first.")
    return sqlite3.connect(DB_PATH)


@mcp.tool()
def search_employees(department: str = None, position: str = None, name: str = None) -> Dict[str, Any]:
    """従業員を検索する"""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM employees WHERE 1=1"
    params = []

    if department:
        query += " AND department = ?"
        params.append(department)

    if position:
        query += " AND position = ?"
        params.append(position)

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")

    cursor.execute(query, params)
    rows = cursor.fetchall()

    employees = []
    for row in rows:
        employees.append(
            {
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "position": row[3],
                "salary": row[4],
                "hire_date": row[5],
            }
        )

    conn.close()
    return {
        "search_criteria": {"department": department, "position": position, "name": name},
        "result_count": len(employees),
        "employees": employees,
    }


@mcp.tool()
def get_project_status(status: str = None) -> Dict[str, Any]:
    """プロジェクトの状態を取得する"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if status:
        cursor.execute("SELECT * FROM projects WHERE status = ?", (status,))
    else:
        cursor.execute("SELECT * FROM projects")

    rows = cursor.fetchall()

    projects = []
    for row in rows:
        projects.append(
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "start_date": row[3],
                "end_date": row[4],
                "status": row[5],
            }
        )

    conn.close()
    return {"status_filter": status or "all", "project_count": len(projects), "projects": projects}


@mcp.tool()
def get_employee_count(department: str = None) -> Dict[str, Any]:
    """従業員数を取得する"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if department:
        cursor.execute("SELECT COUNT(*) FROM employees WHERE department = ?", (department,))
        count = cursor.fetchone()[0]
        result = {"department": department, "count": count}
    else:
        cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
        rows = cursor.fetchall()

        total_cursor = conn.cursor()
        total_cursor.execute("SELECT COUNT(*) FROM employees")
        total_count = total_cursor.fetchone()[0]

        result = {"total_count": total_count, "by_department": {}}

        for row in rows:
            result["by_department"][row[0]] = row[1]

    conn.close()
    return result


@mcp.tool()
async def natural_language_query(query: str) -> Dict[str, Any]:
    """自然言語でデータベースを検索する"""
    result = await text_to_sql_converter.query_with_natural_language(query)
    return result


@mcp.resource("company://employees")
def get_employees() -> str:
    """全従業員情報を取得"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    employees = []
    for row in rows:
        employees.append(
            {
                "id": row[0],
                "name": row[1],
                "department": row[2],
                "position": row[3],
                "salary": row[4],
                "hire_date": row[5],
            }
        )

    conn.close()
    return json.dumps(employees, ensure_ascii=False, indent=2)


@mcp.resource("company://projects")
def get_projects() -> str:
    """全プロジェクト情報を取得"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()

    projects = []
    for row in rows:
        projects.append(
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "start_date": row[3],
                "end_date": row[4],
                "status": row[5],
            }
        )

    conn.close()
    return json.dumps(projects, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
