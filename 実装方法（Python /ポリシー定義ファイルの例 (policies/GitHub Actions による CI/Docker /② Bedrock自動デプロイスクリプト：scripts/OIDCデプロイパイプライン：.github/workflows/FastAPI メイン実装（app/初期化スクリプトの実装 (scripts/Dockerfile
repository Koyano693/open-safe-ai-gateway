FROM python:3.10-slim

WORKDIR /app

# ビルド用依存パッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python依存ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 軽量埋め込みモデルを事前ダウンロード（起動時のモデル初期化遅延を防止）
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# アプリケーションおよびスクリプトのコピー
COPY app/ ./app/
COPY scripts/ ./scripts/

# 非rootユーザーの作成と権限設定
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# Uvicornサーバーの起動（マルチワーカー構成）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
