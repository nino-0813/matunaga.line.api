import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel用のエントリーポイント
# VercelのPythonランタイムはWSGIアプリケーションを直接エクスポートできます
handler = app

