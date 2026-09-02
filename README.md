# マッスルジム湘南 LP

Google広告 / Meta広告 / Instagram広告からの流入を「無料体験予約」「LINE登録」に最大化するための
ランディングページ。フレームワーク非依存の素のHTML / CSS / JSのみで構築し、表示速度・CVRを最優先している。

- `index.html` … LP本体（1ページ完結、ナビゲーションなし）
- `assets/css/style.css` … スタイル一式（ライブラリ不使用）
- `assets/js/main.js` … スクロール演出・固定CTAバー・計測イベント送出（依存ライブラリなし、2.5KB）
- `privacy.html` / `tokushoho.html` … プライバシーポリシー／特定商取引法に基づく表記（雛形）
- `robots.txt` / `sitemap.xml` … SEO用

## 公開前に必ず差し替えるもの

コード内は `○○` やダミードメイン・ダミー電話番号などプレースホルダーのままです。本番公開前に以下を実データに置き換えてください。

| 項目 | 場所 | 現在の値 |
|---|---|---|
| LINE公式アカウントURL | `index.html` 内 `https://lin.ee/your-line-id`（全CTA共通、`grep -n "lin.ee" index.html`で一覧） | ダミー |
| 電話番号 | `tel:0120000000` / 表示テキスト（header, hero下, sticky bar, access, footer, JSON-LD） | ダミー |
| 住所 | JSON-LD (`index.html` head) と `access` セクション、footer | ダミー（○○表記） |
| ドメイン | `<link rel="canonical">`, OGP `og:url`/`og:image`, `robots.txt`, `sitemap.xml` | `musclegym-shonan.example.com` |
| Googleマップ埋め込み | `access__map iframe` の `src` | 藤沢駅の仮埋め込み。実店舗の座標に差し替え |
| Instagram URL | footer, JSON-LD `sameAs` | ダミー |
| 写真 | Unsplashのストック写真（`images.unsplash.com`） | **本番では必ず自社の実写真に差し替えること。** ストック写真は信頼性・独自性を損なうため、初回公開の暫定素材と位置づけてください |
| `tokushoho.html` | 事業者名・運営責任者・メールアドレス等 | ダミー |

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
  cta_id: "line_hero" | "line_follow_hero" | "tel_header" | "line_mid1" | "line_flow" |
          "line_pricing" | "tel_access" | "line_access" | "line_closing" |
          "line_follow_closing" | "line_sticky" | "tel_sticky",
  cta_label: "ボタンの表示テキスト",
  cta_href: "遷移先URL"
}
```

`line_*` はLINE公式アカウントへの遷移（無料体験予約 or LINE登録）、`tel_*` は電話発信です。
CV計測は基本的に「LINE公式アカウントの友だち追加」をコンバージョンポイントとして、
LINE公式アカウント管理画面 or 計測用リダイレクトURLと組み合わせて計測してください
（`cta_click`はあくまで「導線クリック」であり、友だち追加の確定コンバージョンではない点に注意）。

## 設計方針

- **ナビゲーションを持たない1ページLP**：広告経由の流入は離脱経路を減らすことが最優先のため、ヘッダーにメニューは置いていません。
- **CTAの配置**：Hero直下・共感セクション後・ソリューション読了後・ギャラリー後・ステップ後・料金後・アクセスセクション・クロージングと、離脱が起きやすい箇所の直前に反復配置。モバイルはスクロール後に固定CTAバーが追従します。
- **LINE导線を主軸に**：「無料体験予約」と「LINE登録」を同一導線（LINE公式アカウントの友だち追加）に統合することで、フォーム入力の摩擦をゼロにしています。電話は補助導線です。
- **パフォーマンス**：外部ライブラリ・Webフォント不使用。JSは依存ゼロで約2.5KB。画像は`srcset`/`sizes`/`loading="lazy"`/`fetchpriority`を適切に設定し、CLS防止のため`width`/`height`を全画像に指定。
- **アクセシビリティ**：スキップリンク、フォーカスリング、装飾画像への`alt=""`、FAQはネイティブ`<details>`でJS非依存、コントラスト比はAA基準（本文4.5:1以上）で配色を設計。
- **計測拡張性**：GTM/GA4/Meta Pixel/Clarity/Hotjarを後から追加できるよう、設置スロットとCTAのdata属性を用意済み。

## ローカル確認

```bash
python3 -m http.server 8000
# http://localhost:8000/ にアクセス
```
