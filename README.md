# ギャラリーサイト

インスタレーションアートと小型ロボット作品のギャラリーサイト。

## 🌐 公開URL

https://mqce.github.io/quest/

## ✨ 機能

- **カードグリッド表示**: 画像・動画サムネイル対応（自動再生、ループ）
- **フィルタリング**: カテゴリ（インスタレーション / 小型ロボット）、出典（Web / X）、お気に入り、タグ検索
- **お気に入り**: 作品にスターマークを付けて管理
- **サムネイル変更**: 作品ごとにサムネイルを追加・変更可能
- **データ永続化**: GitHubトークンで複数デバイス間で同期、またはブラウザのlocalStorageに保存
- **モバイル対応**: レスポンシブデザイン

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
- **addedDate**: 追加日（YYYY-MM-DD形式）

### ユーザーデータ（`data/user.json`）

お気に入りとサムネイル上書きを保存：

```json
{
  "favorites": ["work-id-1", "work-id-2"],
  "thumbnailOverrides": {
    "work-id": "media/override-image.jpg"
  }
}
```

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
  "addedDate": "2026-10-22"
}]' data/works.json > data/works.tmp.json && mv data/works.tmp.json data/works.json

# 3. コミット＆プッシュ
git add data/works.json media/new-work.jpg
git commit -m "Add new work: 新作品"
git push
```

### サムネイルについて

- **対応形式**: JPEG, PNG, GIF, WebP（画像）、MP4, WebM（動画）
- **推奨サイズ**: 幅 800px 程度（アスペクト比 5:3）
- **動画**: 自動再生、ミュート、ループで表示されます
- **プレースホルダー**: `thumbnail` を `null` にすると、オーナーが後から追加できるプレースホルダーが表示されます

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
├── index.html          # メインHTML
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

## 📝 シードデータ

初期データとして21作品を登録済み：

- **小型ロボット**: 12作品（Sesame, TongDou, BugBot, NeuroMouse, TN-24, Rover, ダイアル・ナイツ、AtomDog、猫型ロボット、Stack-Chan Minimal、Chibi Ram、Meridian）
- **インスタレーション**: 9作品（Organism + Excitable Chaos, Plasticity of Mirrors, Wallaby Kinetic, Pixel Chord, Together, Circus, 機械仕掛けのススキ, Birds In Flight, 舞台作品「模#2」）

画像未設定の作品（Organism + Excitable Chaos, Plasticity of Mirrors, Circus）はプレースホルダー表示され、サイト上から追加可能です。

## 📄 ライセンス

サイトコードはオープンソース。各作品の著作権は各アーティストに帰属します。
