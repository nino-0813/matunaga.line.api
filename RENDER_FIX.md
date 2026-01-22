# Renderデプロイエラーの解決方法

## 問題
Python 3.13で`aiohttp`のビルドが失敗するエラー

## 解決方法

### 方法1: RenderダッシュボードでPythonバージョンを確認

1. Renderダッシュボードでサービスを開く
2. **Settings**タブを開く
3. **Python Version**が正しく設定されているか確認
   - `3.11.0` または `3.12.0` に設定されていることを確認
4. もし`3.13`になっている場合は、手動で変更できない場合があります

### 方法2: 環境変数でPythonバージョンを指定（推奨）

1. Renderダッシュボードでサービスを開く
2. **Environment**タブを開く
3. 新しい環境変数を追加：
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.0`
4. **Save Changes**をクリック
5. **Manual Deploy** → **Deploy latest commit** を実行

### 方法3: サービスを削除して再作成

もし上記の方法で解決しない場合：

1. Renderダッシュボードでサービスを削除
2. 新しいWebサービスを作成
3. 同じリポジトリを接続
4. 設定時に**Runtime**でPythonバージョンを確認（`runtime.txt`が読み込まれるはず）

### 方法4: runtime.txtの確認

`runtime.txt`に以下が記載されていることを確認：
```
python-3.11.0
```

もし異なる場合は、修正してGitHubにプッシュしてください。

## 現在の状態

- `runtime.txt`は`python-3.11.0`に設定済み
- GitHubにプッシュ済み

## 次のステップ

1. Renderダッシュボードで**Manual Deploy** → **Deploy latest commit**を実行
2. まだエラーが出る場合は、環境変数`PYTHON_VERSION=3.11.0`を追加
3. それでも解決しない場合は、サービスを削除して再作成

