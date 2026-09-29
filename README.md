# CardLoopmasterGame / Chronoloop

六十干支カード占い「Chronoloop」のPWAソースです。

## 構成
- `src/index.part*.txt` — アプリ本体HTMLをGitHub転送用に分割したソース
- `scripts/build.py` — HTML再結合、埋め込みPNG→WebP軽量化、Chronoloopアイコン生成
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
- 採用した「金色の無限マーク＋紫のコンパス」モチーフでPWAアイコンを生成
- Service Worker cache: `chronoloop-pwa-v6`

## Netlify
`test-preview` ブランチをNetlifyへ接続する想定です。

Netlifyは `netlify.toml` に従って以下を自動実行します。

1. Pillowをインストール
2. 分割されたHTMLソースを再結合
3. 埋め込みPNGをWebPへ軽量化
4. PWAアイコンを生成
5. `dist/` に公開用ファイルを生成

Publish directory は `dist` です。
