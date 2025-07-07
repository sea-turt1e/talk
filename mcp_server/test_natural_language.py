#!/usr/bin/env python3
"""
自然言語検索機能のテストスクリプト
"""

import asyncio
import json
import os
from text_to_sql import TextToSQLConverter


async def test_natural_language_search():
    """自然言語検索機能のテスト"""
    
    # データベースの存在確認
    if not os.path.exists("company_data.db"):
        print("データベースが見つかりません。python database.py を実行してください。")
        return
    
    # OpenAI APIキーの確認
    if not os.getenv("OPENAI_API_KEY"):
        print("OpenAI APIキーが設定されていません。")
        print("以下のコマンドで設定してください：")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # コンバーターのインスタンス作成
    converter = TextToSQLConverter()
    
    # テストクエリのリスト
    test_queries = [
        "開発部の従業員を全て表示して",
        "年収が700万円以上の従業員を検索",
        "進行中のプロジェクトの一覧を見せて",
        "田中という名前の従業員を探して",
        "人事部の従業員数を教えて",
        "完了したプロジェクトは何個ありますか？"
    ]
    
    print("=== 自然言語検索機能のテスト ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"テスト {i}: {query}")
        print("-" * 50)
        
        try:
            result = await converter.query_with_natural_language(query)
            
            # 結果の表示
            print(f"成功: {result['success']}")
            
            if result['success']:
                sql_info = result['sql_generation']
                print(f"生成されたSQL: {sql_info.get('sql', 'なし')}")
                print(f"説明: {sql_info.get('explanation', 'なし')}")
                print(f"信頼度: {sql_info.get('confidence', 'なし')}")
                
                execution_result = result['execution_result']
                if execution_result and execution_result.get('success'):
                    print(f"結果件数: {execution_result.get('row_count', 0)}")
                    if execution_result.get('data'):
                        print("データ:")
                        for row in execution_result['data'][:3]:  # 最初の3件のみ表示
                            print(f"  {row}")
                        if len(execution_result['data']) > 3:
                            print(f"  ... (他 {len(execution_result['data']) - 3} 件)")
                else:
                    print(f"実行エラー: {execution_result.get('error', '不明なエラー')}")
            else:
                print(f"エラー: {result.get('sql_generation', {}).get('error', '不明なエラー')}")
                
        except Exception as e:
            print(f"例外が発生しました: {e}")
        
        print("\n" + "="*60 + "\n")
    
    print("テスト完了")


if __name__ == "__main__":
    asyncio.run(test_natural_language_search())