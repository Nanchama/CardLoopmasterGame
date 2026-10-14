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
- 採用済みアプリアイコンを元データから**再生成せず復元**し、SHA-256で検証
- Service Worker cache: `chronoloop-pwa-v6`

## Netlify
`test-preview` ブランチをNetlifyへ接続する想定です。

Netlifyは `netlify.toml` に従って以下を自動実行します。

1. Pillowをインストール
2. 分割されたHTMLソースを再結合
3. 埋め込みPNGをWebPへ軽量化
4. 採用済みアプリアイコンPNGを元ファイルと一致する状態で復元
5. `dist/` に公開用ファイルを生成

Publish directory は `dist` です。

## 採用済みアプリアイコン
採用された元画像はGitHubに登録済みです。Netlifyビルド時に**バイト単位で復元し、絵を再生成しません**。

- `assets/icon-192.png` — 採用済みPNG（192px）
- `assets/icon-512.part001.b64` ～ `part009.b64` — 512pxの採用済みPNGをBase64分割保存
- `scripts/build.py` が復元しSHA-256を照合して `dist/icon-192.png` と `dist/icon-512.png` を生成します。
- 見た目の再生成・再描画や再圧縮はしません。

## テストデプロイ
- `main` は公開用。編集はまず `test-preview` にコミットします。
- `test-preview` から `main` へのDraft Pull Request #1 を用意しています。NetlifyがGitHubリポジトリと連携され、Deploy Previewを有効にしている場合、Netlify側でプレビューを生成できます。
- PRとは別に `test-preview` のBranch deployを有効にする運用もできます。
- ビルド設定は `netlify.toml`（command / publish=dist）です。
