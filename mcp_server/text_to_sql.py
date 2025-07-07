#!/usr/bin/env python3
"""
自然言語をSQLに変換するモジュール
"""

import json
import os
import sqlite3
from typing import Any, Dict, List, Optional

import openai


class TextToSQLConverter:
    """自然言語からSQLを生成するクラス"""

    def __init__(self, db_path: str = "company_data.db"):
        self.db_path = db_path
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.schema_info = self._get_schema_info()

    def _get_schema_info(self) -> Dict[str, Any]:
        """データベースのスキーマ情報を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        schema_info = {"tables": {}, "sample_data": {}}

        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]

            # テーブルの構造を取得
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            schema_info["tables"][table_name] = {
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default": col[4],
                        "primary_key": bool(col[5]),
                    }
                    for col in columns
                ]
            }

            # サンプルデータを取得（最初の3行）
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            sample_rows = cursor.fetchall()

            schema_info["sample_data"][table_name] = [
                dict(zip([col[1] for col in columns], row)) for row in sample_rows
            ]

        conn.close()
        return schema_info

    def _build_schema_prompt(self) -> str:
        """スキーマ情報をプロンプト用の文字列に変換"""
        prompt = "データベーススキーマ情報:\n\n"

        for table_name, table_info in self.schema_info["tables"].items():
            prompt += f"テーブル: {table_name}\n"
            prompt += "カラム:\n"
            for col in table_info["columns"]:
                prompt += f"  - {col['name']} ({col['type']})"
                if col["primary_key"]:
                    prompt += " [主キー]"
                if col["not_null"]:
                    prompt += " [NOT NULL]"
                prompt += "\n"

            # サンプルデータを追加
            if table_name in self.schema_info["sample_data"]:
                prompt += "サンプルデータ:\n"
                for i, row in enumerate(self.schema_info["sample_data"][table_name]):
                    prompt += f"  {i+1}. {row}\n"

            prompt += "\n"

        return prompt

    async def convert_to_sql(self, natural_language_query: str) -> Dict[str, Any]:
        """自然言語をSQLに変換"""
        schema_prompt = self._build_schema_prompt()

        system_prompt = f"""あなたは自然言語をSQLに変換するエキスパートです。
        
{schema_prompt}

以下のルールに従ってSQLを生成してください：
1. 与えられたスキーマ情報のみを使用してください
2. 日本語の自然言語クエリを正確なSQLに変換してください
3. 安全なSQLのみを生成してください（DELETE、UPDATE、DROP等は禁止）
4. SELECTクエリのみを生成してください
5. 曖昧な表現の場合は、LIKE演算子を使用してください

レスポンスは以下のJSON形式で返してください：
{{
    "sql": "生成されたSQLクエリ",
    "explanation": "SQLクエリの説明",
    "confidence": "信頼度（0.0-1.0）"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": natural_language_query},
                ],
                temperature=0.1,
                max_tokens=500,
            )

            result = json.loads(response.choices[0].message.content)

            # SQLの安全性チェック
            if self._is_safe_sql(result.get("sql", "")):
                return result
            else:
                return {
                    "sql": None,
                    "explanation": "安全でないSQLクエリが検出されました",
                    "confidence": 0.0,
                    "error": "セキュリティ上の理由でSQLの実行が拒否されました",
                }

        except Exception as e:
            return {"sql": None, "explanation": f"SQL生成エラー: {str(e)}", "confidence": 0.0, "error": str(e)}

    def _is_safe_sql(self, sql: str) -> bool:
        """SQLの安全性をチェック"""
        if not sql:
            return False

        sql_upper = sql.upper().strip()

        # 危険なSQL文をチェック
        dangerous_keywords = [
            "DELETE",
            "UPDATE",
            "INSERT",
            "DROP",
            "CREATE",
            "ALTER",
            "TRUNCATE",
            "REPLACE",
            "MERGE",
            "EXEC",
            "EXECUTE",
        ]

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False

        # SELECTで始まることを確認
        if not sql_upper.startswith("SELECT"):
            return False

        return True

    async def execute_sql(self, sql: str) -> Dict[str, Any]:
        """SQLを実行して結果を返す"""
        if not self._is_safe_sql(sql):
            return {"success": False, "error": "安全でないSQLクエリです", "data": None}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(sql)
            rows = cursor.fetchall()

            # カラム名を取得
            columns = [description[0] for description in cursor.description]

            # 結果を辞書のリストに変換
            result_data = [dict(zip(columns, row)) for row in rows]

            conn.close()

            return {"success": True, "data": result_data, "row_count": len(result_data), "columns": columns}

        except Exception as e:
            return {"success": False, "error": str(e), "data": None}

    async def query_with_natural_language(self, query: str) -> Dict[str, Any]:
        """自然言語でクエリを実行（変換+実行）"""
        # SQL生成
        sql_result = await self.convert_to_sql(query)

        if not sql_result.get("sql"):
            return {
                "success": False,
                "natural_language_query": query,
                "sql_generation": sql_result,
                "execution_result": None,
            }

        # SQL実行
        execution_result = await self.execute_sql(sql_result["sql"])

        return {
            "success": execution_result["success"],
            "natural_language_query": query,
            "sql_generation": sql_result,
            "execution_result": execution_result,
        }


# テスト用の関数
async def test_converter():
    """テスト用の関数"""
    converter = TextToSQLConverter()

    test_queries = [
        "開発部の従業員を全て表示して",
        "年収が700万円以上の従業員を検索",
        "進行中のプロジェクトの一覧を見せて",
        "田中という名前の従業員を探して",
    ]

    for query in test_queries:
        print(f"\n=== クエリ: {query} ===")
        result = await converter.query_with_natural_language(query)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_converter())
