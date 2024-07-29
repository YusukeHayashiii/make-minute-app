<div id="top"></div>

## 使用技術一覧

<!-- シールド一覧 -->
<!-- 該当するプロジェクトの中から任意のものを選ぶ-->
<p style="display: inline">
  <img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
  <img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
</p>

## 目次

1. [プロジェクトについて](#プロジェクトについて)
2. [環境](#環境)
3. [ディレクトリ構成](#ディレクトリ構成)
4. [開発環境構築](#開発環境構築)

<!-- READMEの作成方法のドキュメントのリンク -->
<br />

<!-- プロジェクト名を記載 -->

## プロジェクト名

議事録自動作成アプリ

<!-- プロジェクトについて -->

## プロジェクトについて

AIが文字起こしデータから議事録を作成してくれるアプリのリポジトリ

<!-- プロジェクトの概要を記載 -->

  <p align="left">
    <br />
    <!-- プロジェクト詳細にBacklogのWikiのリンク -->
    <a href="Backlogのwikiリンク"><strong>プロジェクト詳細 »</strong></a>
    <br />
    <br />

<p align="right">(<a href="#top">トップへ</a>)</p>

## 環境

<!-- 言語、フレームワーク、ミドルウェア、インフラの一覧とバージョンを記載 -->

| 言語・フレームワーク  | バージョン |
| --------------------- | ---------- |
| Python                | 3.12.4     |

Pythonのライブラリのバージョンは requirements.txt を参照してください

<p align="right">(<a href="#top">トップへ</a>)</p>

## ディレクトリ構成

```bash
.
├── .devcontainer
│   ├── devcontainer.json
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env(クローン後自分で作成する必要あり)
├── app.py
├── .env(クローン後自分で作成する必要あり)
├── .gitignore
├── README.md
├── .streamlit
│   └── config.toml
├── prompt
│   └── make_minute.yaml
├── st_components
│   ├── st_config.py
│   ├── st_file_upload.py
│   ├── st_home_page.py
│   ├── st_make_minute.py
│   └── st_session_states.py
└── utils
    └── functions.py
```


<p align="right">(<a href="#top">トップへ</a>)</p>

## 開発環境構築

<!-- コンテナの作成方法、パッケージのインストール方法など、開発環境構築に必要な情報を記載 -->

### コンテナの作成と起動

.env ファイルを以下の環境変数例と[環境変数の一覧](#環境変数の一覧)を元に作成

- ルートディレクトリの.envファイル

```.env
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_API_ENDPOINT=xxx
AZURE_API_VERSION=xxx
OPENAI_ENGINE_LLM=xxx
```

- /.devcontainer配下の.envファイル

```.env
COMPOSE_PROJECT_NAME=your_project_name
```

.env ファイルを作成後、VScodeのコマンドパレットを開き、「開発コンテナー：コンテナーで再度開く」を押しコンテナを起動

### 動作確認

http://localhost:7001 にアクセスできるか確認(環境によってIPアドレスが異なる場合あり)
アクセスできたら成功

### コンテナの停止

VSCodeの画面を閉じるか、コマンドパレットを開き「開発コンテナー：フォルダーをローカルで再度開く」を押すと停止できます。

### 環境変数の一覧

| 変数名                 | 役割                                        |
| ---------------------- | ----------------------------------------- |
| COMPOSE_PROJECT_NAME      | コンテナ名                               |
| AZURE_OPENAI_API_KEY      | Azure OpenAIのAPIキー                   |
| AZURE_OPENAI_API_ENDPOINT | Azure OpenAIのエンドポイント              |
| AZURE_API_VERSION         | モデルのバージョン                        |
| OPENAI_ENGINE_LLM         | モデルのデプロイ名                        |

<p align="right">(<a href="#top">トップへ</a>)</p>
