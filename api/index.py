import sys
import os
from io import BytesIO

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel用のエントリーポイント
# VercelのPythonランタイムは関数形式のhandlerを期待します
def handler(request):
    """
    VercelのRequestオブジェクトをWSGI環境変数に変換してFlaskアプリを実行
    """
    # リクエストボディを取得
    body = request.body
    if isinstance(body, str):
        body = body.encode('utf-8')
    elif body is None:
        body = b''
    
    # WSGI環境変数を作成
    environ = {
        'REQUEST_METHOD': request.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': request.path,
        'QUERY_STRING': request.query_string or '',
        'CONTENT_TYPE': request.headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
        'SERVER_NAME': request.host.split(':')[0] if ':' in request.host else request.host,
        'SERVER_PORT': '443',
        'HTTP_HOST': request.host,
    }
    
    # ヘッダーを環境変数に追加
    for key, value in request.headers.items():
        env_key = f'HTTP_{key.upper().replace("-", "_")}'
        environ[env_key] = value
    
    # レスポンスを保存する変数
    response_status = [None]
    response_headers = [None]
    response_body = []
    
    def start_response(status, headers):
        response_status[0] = status
        response_headers[0] = headers
    
    # Flaskアプリを呼び出す
    try:
        result = app(environ, start_response)
        for chunk in result:
            if isinstance(chunk, str):
                chunk = chunk.encode('utf-8')
            response_body.append(chunk)
    except Exception as e:
        import traceback
        traceback.print_exc()
        response_status[0] = '500 Internal Server Error'
        response_headers[0] = [('Content-Type', 'text/plain')]
        response_body = [f'Error: {str(e)}'.encode('utf-8')]
    
    # ステータスコードを取得
    status_code = 200
    if response_status[0]:
        status_code = int(response_status[0].split()[0])
    
    # ヘッダーを辞書に変換
    headers_dict = {}
    if response_headers[0]:
        for key, value in response_headers[0]:
            headers_dict[key] = value
    
    # ボディを結合
    body_bytes = b''.join(response_body)
    
    # Responseオブジェクトを作成（Vercelの形式に合わせる）
    # VercelのPythonランタイムは辞書形式のレスポンスを期待します
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': body_bytes.decode('utf-8') if body_bytes else ''
    }

