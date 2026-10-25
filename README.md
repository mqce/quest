# ギャラリーサイト

インスタレーションアートと小型ロボット作品のギャラリーサイト。

## 🌐 公開URL

- **トップページ**: https://mqce.github.io/quest/
- **アーカイブ**: https://mqce.github.io/quest/archive.html

## ✨ 機能

- **最新作品の表示**: トップページには最新の追加日の作品のみを表示
- **アーカイブページ**: 過去の全作品を追加日ごとにグループ化して表示
- **カードグリッド表示**: 画像・動画サムネイル対応（自動再生、ループ）
- **フィルタリング**: カテゴリ（インスタレーション / 小型ロボット）、出典（Web / X）、お気に入り、タグ検索
- **お気に入り**: 作品にスターマークを付けて管理
- **サムネイル変更**: 作品ごとにサムネイルを追加・変更可能
- **データ永続化**: GitHubトークンで複数デバイス間で同期、またはブラウザのlocalStorageに保存
- **モバイル対応**: レスポンシブデザイン、スマートフォンでも見やすいコンパクトなヘッダー

## 🚀 初回セットアップ（オーナー向け）

### 1. GitHub Pages を有効化

1. リポジトリの **Settings** → **Pages** へ移動
2. **Source** を **GitHub Actions** に変更
3. 保存

これで、`main`ブランチへのpush時に自動デプロイされます。

### 2. GitHub Personal Access Token の作成（オプション）

お気に入りやサムネイル変更を複数デバイス間で同期したい場合：

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens**
2. **Generate new token** をクリック
3. トークン名を設定（例: `Gallery User Data`）
4. **Repository access** で `mqce/quest` を選択
5. **Permissions** で **Contents** を **Read and write** に設定
6. **Generate token** をクリックしてトークンをコピー
7. サイトの⚙️設定パネルを開き、トークンを入力して保存

トークン未設定でも、ブラウザのlocalStorageに保存されます（エクスポート/インポート機能あり）。

## 📦 データ構造

### 作品データ（`data/works.json`）

各作品は以下のフィールドを持ちます：

```json
{
  "id": "unique-id",
  "title": "作品名",
  "artist": "アーティスト名",
  "year": 2026,
  "category": "installation",
  "source": "web",
  "sourceUrl": "https://...",
  "sourceSite": "サイト名",
  "summary": "日本語の説明文",
  "tags": ["タグ1", "タグ2"],
  "thumbnail": "media/image.jpg",
  "addedDate": "2026-01-01"
}
```

#### フィールド説明

- **id**: 一意の識別子（英数字とハイフン）
- **title**: 作品名
- **artist**: アーティスト名
- **year**: 制作年
- **category**: `installation` または `small-robot`
- **source**: `web` または `x`
- **sourceUrl**: 元ページのURL
- **sourceSite**: 出典サイト名
- **summary**: 日本語の説明文
- **tags**: タグの配列（技術要素など）
- **thumbnail**: 画像または動画のパス（`media/` 以下）、またはURL。`null` でプレースホルダー表示
- **candidates**: サムネイル候補の配列（オプション）。各候補は `{ "type": "image"|"video", "src": "...", "origin": "..." }` 形式
  - ユーザーがこの中から好みのサムネイルを選択できます
  - `thumbnail` が `null` で候補がある場合、カードに選択UIが表示されます
- **addedDate**: **このギャラリーサイトへの追加日**（YYYY-MM-DD形式、必須）
  - 作品の元の公開日ではなく、このサイトに追加した日付を記入してください
  - トップページには最新の `addedDate` の作品のみが表示されます

### ユーザーデータ（`data/user.json`）

お気に入りとユーザーが選択したサムネイルを保存：

```json
{
  "favorites": ["work-id-1", "work-id-2"],
  "thumbnails": {
    "work-id": ["media/user-selected-1.jpg", "media/user-selected-2.jpg"]
  }
}
```

- **favorites**: お気に入りに追加した作品のID配列
- **thumbnails**: 各作品でユーザーが選択したサムネイルの配列（複数選択時はスライドショー表示）

## 🤖 ボットによる作品追加方法

### 手順

1. 作品データを `data/works.json` に追加（配列の末尾に追記）
2. サムネイル画像・動画を `media/` ディレクトリに配置
3. 変更をコミット＆プッシュ

### 例：新しい作品を追加

```bash
# 1. 画像をダウンロード
curl -o media/new-work.jpg "https://example.com/image.jpg"

# 2. works.json に追記（jq 使用例）
# ⚠️ addedDate には必ず今日の日付（YYYY-MM-DD）を記入してください
TODAY=$(date +%Y-%m-%d)
jq '. += [{
  "id": "new-work",
  "title": "新作品",
  "artist": "アーティスト名",
  "year": 2026,
  "category": "installation",
  "source": "web",
  "sourceUrl": "https://example.com/work",
  "sourceSite": "Example Site",
  "summary": "作品の説明",
  "tags": ["Arduino", "モーター"],
  "thumbnail": "media/new-work.jpg",
  "addedDate": "'"$TODAY"'"
}]' data/works.json > data/works.tmp.json && mv data/works.tmp.json data/works.json

# 3. コミット＆プッシュ
git add data/works.json media/new-work.jpg
git commit -m "Add new work: 新作品"
git push
```

### 重要：addedDate について

- `addedDate` には**必ず**作品を追加した日付を記入してください
- トップページには最新の `addedDate` の作品のみが表示されます
- 過去の作品はアーカイブページ（archive.html）で日付ごとにグループ化されて表示されます

### サムネイルについて

- **対応形式**: JPEG, PNG, GIF, WebP（画像）、MP4, WebM（動画）
- **推奨サイズ**: 幅 800px 程度（アスペクト比 5:3）
- **動画**: 自動再生、ミュート、ループで表示されます
- **デフォルトサムネイル**: 作品に `thumbnail` フィールドが設定されている場合、それが表示されます
- **サムネイル選択機能**:
  - すべての作品カードに「変更」ボタンが表示されます
  - ボタンをクリックすると、サムネイル選択モーダルが開きます
  - モーダルには自動サムネイル（設定されている場合）と `candidates` 配列のすべての候補が表示されます
  - 複数のサムネイルを選択でき、選択順にスライドショーで表示されます
  - ユーザーが選択したサムネイルは `data/user.json` の `thumbnails` に保存されます
  - ユーザーの選択は自動サムネイルよりも優先されます
  - URLから画像を追加することもできます
- **サムネイル未設定の作品**: `thumbnail: null` の場合、「サムネイル未設定 — 候補から選ぶ」プレースホルダーが表示されます

## 🛠️ 開発

このサイトは静的HTML + JavaScript のみで動作します。ビルドステップは不要です。

### ローカルで確認

```bash
# 簡易HTTPサーバーを起動
python3 -m http.server 8000

# ブラウザで http://localhost:8000/ を開く
```

### ファイル構成

```
.
├── index.html          # トップページ（最新作品）
├── archive.html        # アーカイブページ（全作品）
├── data/
│   ├── works.json      # 作品データ
│   └── user.json       # ユーザーデータ（お気に入り等）
├── media/              # サムネイル画像・動画
│   ├── work1.jpg
│   ├── work2.mp4
│   └── ...
└── .github/
    └── workflows/
        └── deploy.yml  # GitHub Pages デプロイ設定
```

## 📝 作品データ

現在26作品を登録済み：

- **2026-10-22 追加**: 21作品
  - 小型ロボット: 12作品
  - インスタレーション: 9作品
- **2026-10-24 追加**: 5作品
  - Whirly Loops, G16, Who is jumping, Jack?, SHAPE SHIFT, Snailtube

トップページには最新の追加日（2026-10-24）の5作品が表示されます。
過去の作品はアーカイブページで閲覧できます。

## 📄 ライセンス

サイトコードはオープンソース。各作品の著作権は各アーティストに帰属します。
