# MCPサーバー デモプロジェクト

会社データベースからMCPサーバーを使って情報を取得するサンプルプロジェクトです。

## 概要

このプロジェクトは、Model Context Protocol (MCP)を使用して、SQLiteデータベースから従業員情報とプロジェクト情報を取得するサーバーを実装しています。

## 主な機能

- 従業員情報の検索
- プロジェクト状態の取得
- 従業員数のカウント
- データの一覧表示

## ファイル構成

```
.
├── CLAUDE.md           # プロジェクト設定
├── README.md           # このファイル
├── requirements.txt    # Python依存関係
├── database.py         # データベース初期化スクリプト
├── server.py           # MCPサーバーメインコード
└── slides.md           # LT用スライド（marp形式）
```

## セットアップ手順

### 1. Python環境の準備

```bash
# pyenv virtualenvで仮想環境を作成
pyenv virtualenv 3.11.7 mcp-demo
pyenv local mcp-demo

# 依存関係をインストール
pip install -r requirements.txt
```

### 2. データベースの初期化

```bash
# サンプルデータを含むSQLiteデータベースを作成
python database.py
```

実行後、以下のファイルが作成されます：
- `company_data.db` - SQLiteデータベースファイル

### 3. MCPサーバーの起動

```bash
# MCPサーバーを起動
python server.py
```

## データベース構造

### 従業員テーブル (employees)
| カラム名 | 型 | 説明 |
|---------|---|------|
| id | INTEGER | 従業員ID（主キー） |
| name | TEXT | 従業員名 |
| department | TEXT | 所属部署 |
| position | TEXT | 役職 |
| salary | INTEGER | 年収 |
| hire_date | TEXT | 入社日 |

### プロジェクトテーブル (projects)
| カラム名 | 型 | 説明 |
|---------|---|------|
| id | INTEGER | プロジェクトID（主キー） |
| name | TEXT | プロジェクト名 |
| description | TEXT | 説明 |
| start_date | TEXT | 開始日 |
| end_date | TEXT | 終了日 |
| status | TEXT | 状態 |

## 利用可能なリソース

1. **company://employees** - 全従業員情報
2. **company://projects** - 全プロジェクト情報

## 利用可能なツール

1. **search_employees** - 従業員検索
   - `department`: 部署名で検索
   - `position`: 役職で検索
   - `name`: 名前で検索

2. **get_project_status** - プロジェクト状態取得
   - `status`: 状態で検索（オプション）

3. **get_employee_count** - 従業員数取得
   - `department`: 部署名（オプション）

## スライドの表示

marpを使用してスライドを表示します：

```bash
# marpをインストール（未インストールの場合）
npm install -g @marp-team/marp-cli

# スライドをHTMLに変換
marp slides.md --html

# またはPDFに変換
marp slides.md --pdf
```

## 使用技術

- **Python 3.11.7** - プログラミング言語
- **SQLite** - データベース
- **MCP (Model Context Protocol)** - AI連携プロトコル
- **marp** - プレゼンテーション作成

## トラブルシューティング

### データベースファイルが見つからないエラー
```
データベースファイル 'company_data.db' が見つかりません。
```
→ `python database.py` を実行してデータベースを初期化してください。

### MCPライブラリのインストールエラー
```
pip install mcp==1.0.0
```
→ 正確なバージョンを確認してrequirements.txtを更新してください。

## 参考資料

- [MCP公式ドキュメント](https://github.com/modelcontextprotocol/servers)
- [marp公式サイト](https://marp.app/)
- [SQLite公式ドキュメント](https://sqlite.org/docs.html)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。