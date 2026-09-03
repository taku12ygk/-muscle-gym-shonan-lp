# マッスルジム湘南 LP

Google広告 / Meta広告 / Instagram広告からの流入を「パーソナルトレーニング・施術/ケアの無料体験予約」に
最大化するためのランディングページ。フレームワーク非依存の素のHTML / CSS / JSのみで構築し、
表示速度・CVRを最優先している。

- `index.html` … LP本体（1ページ完結、ナビゲーションなし）
- `assets/css/style-20260904.css` … スタイル一式（ライブラリ不使用）
- `assets/js/main-20260903.js` … スクロール演出・固定CTAバー・計測イベント送出（依存ライブラリなし、2.5KB）
- `assets/img/photos/` … 実店舗の撮影写真（Web用に圧縮済み、srcset用に複数サイズを書き出し）
- `privacy.html` / `tokushoho.html` … プライバシーポリシー／特定商取引法に基づく表記（雛形）
- `robots.txt` / `sitemap.xml` … SEO用

すべてのファイルパスは相対パス（`./`）で統一しており、GitHub Pagesのプロジェクトサイト
（`https://<user>.github.io/<repo>/` のようなサブパス配信）でもそのまま動作します。

CSS/JSのファイル名には更新日（`-20260903`）を付けています。デザイン修正を配信した際に
ブラウザ・CDNの古いキャッシュが新CSSへ切り替わらない事象が発生したため、クエリパラメータ
ではなくファイル名自体を変更してキャッシュを確実に更新する方式にしています。次回デザインを
更新する際も、`style.css`/`main.js`を直接上書きするのではなく、新しい日付を付けたファイル名
（例：`style-20261001.css`）を作成し、全HTMLの参照先を更新してください。

## 店舗情報（確定・反映済み）

以下は確定情報として全ページに反映済みです。

| 項目 | 値 |
|---|---|
| 店舗名 | マッスルジム湘南店（英語表記: MUSCLE GYM SHONAN） |
| 住所 | 〒251-0025 神奈川県藤沢市鵠沼石上1-5-21 やませビル鵠沼2F（藤沢駅南口から徒歩3分） |
| ジム電話番号 | 0466-54-8588（`tel:0466548588`） |
| PEACE接骨院・リラクゼーション電話番号 | 0466-28-4040（`tel:0466284040`） |
| LINE公式アカウント | https://lin.ee/5dk5BNG |
| Instagram | https://www.instagram.com/musclegym_shonan/ |
| 本LPの公開URL | https://taku12ygk.github.io/-muscle-gym-shonan-lp/（`canonical` / OGP / JSON-LD `url` / `robots.txt` / `sitemap.xml` はこのURLを使用） |
| 公式サイト（別ドメイン） | https://musclegym-shonan.jp/（footerの「公式サイト」リンク先、JSON-LD `sameAs` として参照。canonical等には使用しない） |
| ジム営業時間 | 24時間エリア：24時間利用可能／スタッフ受付：平日10:00〜22:00・土曜10:00〜18:00（水・日休み） |
| PEACE接骨院・リラクゼーション営業時間 | 月・火・木・金 10:00〜14:00／16:00〜22:00、土曜・祝日 10:00〜14:00／15:00〜18:00（水・日休み） |
| 運営会社 | 株式会社同心会（`tokushoho.html` 事業者名） |
| 運営責任者 | 澤田 勝（`tokushoho.html` 運営責任者） |
| 問い合わせメール | musclegymsyonan@gmail.com（`mailto:musclegymsyonan@gmail.com`。footer/access/privacy/tokushoho/JSON-LDに反映） |

現在の運営会社は株式会社同心会です。事業譲渡後にFifth Core株式会社へ変更予定とのことですが、
**譲渡完了までは株式会社同心会のまま**とし、Fifth Core株式会社は一切記載していません。

本LPは現在GitHub Pages（`https://taku12ygk.github.io/-muscle-gym-shonan-lp/`）で公開・確認しており、
`canonical`/OGP/JSON-LD `url`/`robots.txt`/`sitemap.xml`はこのURLを採用しています。
`https://musclegym-shonan.jp/` は別ドメインの公式サイトとして扱い、footerの「公式サイト」リンクと
JSON-LD `sameAs` からのみ参照しています。GitHub Pagesの独自ドメイン設定（CNAME）は変更していません
（このリポジトリに`CNAME`ファイルは存在しません）。将来、公式ドメインへ本LPを移行する際は、
`canonical`/OGP/JSON-LD `url`/`robots.txt`/`sitemap.xml`を新しいURLに差し替えてください。

## 9月限定キャンペーン（確定条件）

- 受付期間：〜2026年9月30日、人数制限なし
- 価格はすべて税込表記
- 他のキャンペーン・特典との併用不可（`campaign`セクション・`pricing`セクションの両方に注記を明記）
- 全コース共通：入会金0円（税込）／事務手数料0円（税込）／無料体験実施中
- 24時間コース：最初の2ヶ月間 月額2,980円（税込）／3ヶ月目以降は通常料金／6ヶ月継続契約／接骨院の選べる2回券付き
- パーソナルコース：最初の2ヶ月間 追加セット料金0円（パーソナル料金は別途）／パーソナル料金だけで利用可能／「パーソナル＋24時間」「パーソナル＋接骨院」から選択可能
- 公式LINE限定特典：公式LINEからのお問い合わせで初月月会費半額（税込）／他の特典との併用不可

## 公開前に確認が必要なもの

現時点で未確定の項目はありません。プライバシーポリシーの制定日も2026年9月3日として
`privacy.html`に反映済みです。

写真は実店舗の撮影データに差し替え済みです（Unsplash等のストック写真・AI生成画像は不使用）。

## セクション構成

1. Hero
2. 3つの特徴
3. 9月限定キャンペーン（共通特典＋24時間コース／パーソナルコース＋LINE限定特典）
4. 24時間ジム
5. パーソナルトレーニング
6. 施術・ケア（併設PEACE接骨院・リラクゼーション）
7. 施設写真ギャラリー
8. 無料体験の流れ（3ステップ）
9. 料金について（要約＋「9月限定キャンペーン」への案内リンクのみ。詳細は3.に集約）
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

`main-20260903.js` が全CTAクリックで `window.dataLayer` に以下を自動push します。GTMのカスタムイベントトリガー（イベント名 `cta_click`）でGA4のコンバージョンイベントや広告のコンバージョンタグに接続してください。

```js
{
  event: "cta_click",
  cta_id: "line_hero" | "tel_header" | "line_campaign" | "line_flow" |
          "line_pricing" | "tel_access" | "tel_access_peace" | "mail_access" |
          "map_access" | "line_access" | "line_closing" | "line_sticky" | "tel_sticky",
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
- **アクセス欄の地図**：`google.com/maps?q=...&output=embed`形式のAPIキー不要な簡易iframe埋め込みは、環境によって読み込めず灰色のエラー表示になる不具合が実機で確認されたため使用していません。住所は`access__list`に常時テキスト表示し、地図の代わりに常に確実に表示される静的カード（`.access__map-card`）を設置。`maps.app.goo.gl`の短縮リンクで地図アプリを直接開ける「Googleマップで開く」ボタンを配置しています。実際の地図をページ内に埋め込みたい場合は、Googleマップの「地図を共有または埋め込む」→「地図を埋め込む」で発行される公式の`maps/embed?pb=...`形式のiframeコードをご提供いただければ差し替えます。

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
