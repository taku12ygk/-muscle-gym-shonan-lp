# マッスルジム湘南 LP

Google広告 / Meta広告 / Instagram広告からの流入を「パーソナルトレーニング・施術/ケアの無料体験予約」に
最大化するためのランディングページ。フレームワーク非依存の素のHTML / CSS / JSのみで構築し、
表示速度・CVRを最優先している。

- `index.html` … LP本体（1ページ完結、ナビゲーションなし）
- `assets/css/style.css` … スタイル一式（ライブラリ不使用）
- `assets/js/main.js` … スクロール演出・固定CTAバー・計測イベント送出（依存ライブラリなし、2.5KB）
- `assets/img/photos/` … 実店舗の撮影写真（Web用に圧縮済み、srcset用に複数サイズを書き出し）
- `privacy.html` / `tokushoho.html` … プライバシーポリシー／特定商取引法に基づく表記（雛形）
- `robots.txt` / `sitemap.xml` … SEO用

すべてのファイルパスは相対パス（`./`）で統一しており、GitHub Pagesのプロジェクトサイト
（`https://<user>.github.io/<repo>/` のようなサブパス配信）でもそのまま動作します。

## 公開前に必ず差し替えるもの

コード内は `○○` やダミードメイン・ダミー電話番号などプレースホルダーのままです。
**店舗名・住所・電話番号・LINE公式アカウントURL・Instagram URL・営業時間はまだ実データが
届いていないため、以下はすべてダミーのままです。** 届き次第、最優先で反映します。

| 項目 | 場所 | 現在の値 |
|---|---|---|
| LINE公式アカウントURL | `index.html` 内 `https://lin.ee/your-line-id`（全CTA共通、`grep -n "lin.ee" index.html`で一覧） | ダミー |
| 電話番号 | `tel:0120000000` / 表示テキスト（header, sticky bar, access, footer, JSON-LD） | ダミー |
| 住所 | JSON-LD (`index.html` head) と `access` セクション、footer | ダミー（○○表記） |
| ドメイン | `<link rel="canonical">`, OGP `og:url`/`og:image`, `robots.txt`, `sitemap.xml` | `musclegym-shonan.example.com` |
| Googleマップ埋め込み | `access__map iframe` の `src` | 藤沢駅の仮埋め込み。実店舗の座標に差し替え |
| Instagram URL | footer, JSON-LD `sameAs` | ダミー |
| `tokushoho.html` | 事業者名・運営責任者・メールアドレス等 | ダミー |
| キャンペーン条件 | `campaign` / `pricing` セクション | 確定情報を反映済み（税込表記・併用可否・終了日・人数制限は未確認のため未記載） |

写真は実店舗の撮影データに差し替え済みです（Unsplash等のストック写真・AI生成画像は不使用）。

## セクション構成

1. Hero
2. 3つの特徴
3. 9月スタート応援キャンペーン（共通特典＋24時間コース／パーソナルコース＋LINE限定特典）
4. 24時間ジム
5. パーソナルトレーニング
6. 施術・ケア（併設PEACE接骨院・リラクゼーション）
7. 施設写真ギャラリー
8. 無料体験の流れ（3ステップ）
9. 料金・キャンペーン条件（詳細＋注記）
10. FAQ
11. アクセス
12. 最終LINE CTA

トレーナー紹介・お客様の声・ビフォーアフター・実績数値のセクションは、宣材写真・モニター写真が
揃っていないため削除しています。将来、実際の素材が揃った段階で追加してください（架空の名前・経歴・
口コミ・写真は使用していません）。

## 計測タグの導入（GTM / GA4 / Meta Pixel / Clarity / Hotjar）

`index.html` の `<head>` 末尾と `</body>` 直前に、コメントアウトされた設置スロットを用意しています。

1. `<head>` 内のGTMスニペットのコメントを外し、`GTM-XXXXXXX` を実際のコンテナIDに差し替える
2. `<body>` 直後にGTMのnoscriptタグ、Meta Pixel・Microsoft Clarity・HotjarのスニペットをID差し替えの上で追加する
3. GA4はGTM経由でのタグ設定を推奨（直接gtag.jsを追加する場合は同じ要領でスロットに追記）

### クリックイベント（GTM側でのトリガー設定用）

`main.js` が全CTAクリックで `window.dataLayer` に以下を自動push します。GTMのカスタムイベントトリガー（イベント名 `cta_click`）でGA4のコンバージョンイベントや広告のコンバージョンタグに接続してください。

```js
{
  event: "cta_click",
  cta_id: "line_hero" | "tel_header" | "line_campaign" | "line_flow" |
          "line_pricing" | "tel_access" | "line_access" | "line_closing" |
          "line_sticky" | "tel_sticky",
  cta_label: "ボタンの表示テキスト",
  cta_href: "遷移先URL"
}
```

`line_*` はLINE公式アカウントへの遷移（無料体験予約）、`tel_*` は電話発信です。
CV計測は基本的に「LINE公式アカウントの友だち追加」をコンバージョンポイントとして、
LINE公式アカウント管理画面 or 計測用リダイレクトURLと組み合わせて計測してください
（`cta_click`はあくまで「導線クリック」であり、友だち追加の確定コンバージョンではない点に注意）。

## 設計方針

- **ナビゲーションを持たない1ページLP**：広告経由の流入は離脱経路を減らすことが最優先のため、ヘッダーにメニューは置いていません。
- **CTAの配置**：Hero直下・キャンペーン直後・料金説明直後・体験の流れ・アクセス・クロージングと、離脱が起きやすい箇所の直前に反復配置。モバイルはスクロール後に固定CTAバーが追従します。
- **CTA文言の統一**：「LINEで無料体験を予約する」に統一し、LINE上で「パーソナルトレーニング」か「施術・ケア」の希望内容を伝えられるよう案内しています。
- **パフォーマンス**：外部ライブラリ・Webフォント不使用。JSは依存ゼロで約2.5KB。画像は`srcset`/`sizes`/`loading="lazy"`/`fetchpriority`を適切に設定し、CLS防止のため`width`/`height`を全画像に指定。写真は圧縮済み（合計 約2.2MB / 21ファイル）。
- **アクセシビリティ**：スキップリンク、フォーカスリング、装飾画像への`alt=""`、FAQはネイティブ`<details>`でJS非依存、コントラスト比はAA基準（本文4.5:1以上）で配色を設計。
- **計測拡張性**：GTM/GA4/Meta Pixel/Clarity/Hotjarを後から追加できるよう、設置スロットとCTAのdata属性を用意済み。

## ローカル確認

```bash
python3 -m http.server 8000
# http://localhost:8000/ にアクセス
```

GitHub Pagesのサブパス環境を再現して確認する場合：

```bash
mkdir -p /tmp/pages-sim/<repo名> && cp -r ./* /tmp/pages-sim/<repo名>/
cd /tmp/pages-sim && python3 -m http.server 8000
# http://localhost:8000/<repo名>/ にアクセス
```
