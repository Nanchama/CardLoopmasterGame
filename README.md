# CardLoopmasterGame / Chronoloop

六十干支カード占い「Chronoloop」のPWAソースです。

## 構成
- `src/index.part*.txt` — アプリ本体HTMLをGitHub転送用に分割したソース
- `scripts/build.py` — HTML再結合、埋め込みPNG→WebP軽量化、採用アイコン優先出力
- `manifest.webmanifest` — PWA設定
- `service-worker.js` — オフラインキャッシュ
- `robots.txt` — 検索エンジンのクロール抑制
- `netlify.toml` — Netlifyビルド設定
- `requirements.txt` — Netlifyビルド用Python依存関係

## 現在の仕様
- iPhone Safe Area対応
- ハンバーガーメニュー「ショートカット追加」
- ホーム画面追加の案内
- 機内モード対応
- Netlify下部表示の誤タップ対策余白
- noindex / robots.txt
- ビルド時にスプラッシュ・タイトル埋め込みPNGをWebP化
- `assets/icon-192.png` と `assets/icon-512.png` があれば採用済み画像を変更せず公開用フォルダへコピー。未登録の場合は仮アイコンを生成（※採用デザインとは異なる）
- Service Worker cache: `chronoloop-pwa-v6`

## Netlify
`test-preview` ブランチをNetlifyへ接続する想定です。

Netlifyは `netlify.toml` に従って以下を自動実行します。

1. Pillowをインストール
2. 分割されたHTMLソースを再結合
3. 埋め込みPNGをWebPへ軽量化
4. `assets/` に採用アイコンがあればそのままコピー、未登録の場合は仮アイコンを生成
5. `dist/` に公開用ファイルを生成

Publish directory は `dist` です。

## 採用済みアプリアイコンの反映（未完了）
現在、画像本体のバイナリデータはまだGitHubに登録されていません。
`test-preview` ブランチの `assets/` に下記の2ファイルを追加してください。
- `assets/icon-192.png` — SHA-256: `6590aea2ab0cf10a76797d4cc651869cfdadf54f90eb50b0c62360b3e66e2c3f`
- `assets/icon-512.png` — SHA-256: `9c46b45412696c659fb60cad19745cbb21f322152259cf0e0c32ada3884c4c28`

追加後は再ビルドすると、採用画像をそのままホーム画面アイコンに使います。
