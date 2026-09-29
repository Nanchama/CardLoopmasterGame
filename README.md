# CardLoopmasterGame / Chronoloop

六十干支カード占い「Chronoloop」のPWAソースです。

## 構成
- `src/index.part*.txt` — アプリHTMLをGitHub転送用に分割したソース
- `assets/icon-512.b64.part*.txt` — 採用済みアプリアイコンのBase64分割ソース
- `scripts/build.py` — HTML再結合、埋め込みPNG→WebP軽量化、アイコン生成
- `manifest.webmanifest` — PWA設定
- `service-worker.js` — オフラインキャッシュ
- `robots.txt` — 検索エンジンのクロール抑制
- `netlify.toml` — Netlifyビルド設定

## 現在の仕様
- iPhone Safe Area対応
- ハンバーガーメニュー「ショートカット追加」
- ホーム画面追加の案内
- 機内モード対応
- Netlify下部表示の誤タップ対策余白
- noindex / robots.txt
- ビルド時にスプラッシュ・タイトル埋め込みPNGをWebP化
- 採用済みChronoloopアイコン
- Service Worker cache: `chronoloop-pwa-v6`

## Netlify
`test-preview` ブランチをNetlifyへ接続する想定です。
`netlify.toml` に従い、ビルド後の `dist/` を公開します。
