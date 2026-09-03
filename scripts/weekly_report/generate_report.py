#!/usr/bin/env python3
"""
週次レポート生成スクリプト（マッスルジム湘南店LP）

毎週月曜9:00（日本時間）にGitHub Actionsから自動実行される想定です。
GA4（サイトの利用状況）とSearch Console（検索結果での表示・クリック状況）を取得し、
分かりやすい日本語のレポート（weekly_report.md）を作成します。

【安全設計】
Google連携に必要なSecrets（GOOGLE_SERVICE_ACCOUNT_JSON / GA4_PROPERTY_ID / GSC_SITE_URL）が
まだ設定されていない場合は、エラーで止まらず「まだ準備中です」というメッセージを出して
正常終了します（毎週失敗メールが届くようなことはありません）。

このスクリプト自身がGoogleへ何かを書き込むことはありません（読み取り専用の権限のみ使用）。
"""

from __future__ import annotations

import datetime
import json
import os
import sys


def env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def write_status(status: str) -> None:
    with open("weekly_report_status.txt", "w", encoding="utf-8") as f:
        f.write(status)


def main() -> int:
    sa_json = env("GOOGLE_SERVICE_ACCOUNT_JSON")
    ga4_property_id = env("GA4_PROPERTY_ID")
    gsc_site_url = env("GSC_SITE_URL")

    missing = [
        name
        for name, value in [
            ("GOOGLE_SERVICE_ACCOUNT_JSON", sa_json),
            ("GA4_PROPERTY_ID", ga4_property_id),
            ("GSC_SITE_URL", gsc_site_url),
        ]
        if not value
    ]
    if missing:
        print("Google連携の設定（GitHub Secrets）がまだ登録されていないため、今回は取得をスキップしました。")
        print("未設定の項目: " + ", ".join(missing))
        print("設定方法は docs/google-setup-guide.md を参照してください。")
        write_status("skipped")
        return 0

    try:
        creds_info = json.loads(sa_json)
    except json.JSONDecodeError as e:
        print(f"GOOGLE_SERVICE_ACCOUNT_JSON の内容がJSONとして読み取れませんでした: {e}")
        write_status("skipped")
        return 0

    from google.oauth2 import service_account
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )
    from googleapiclient.discovery import build

    scopes = [
        "https://www.googleapis.com/auth/analytics.readonly",
        "https://www.googleapis.com/auth/webmasters.readonly",
    ]
    credentials = service_account.Credentials.from_service_account_info(creds_info, scopes=scopes)

    today = datetime.date.today()
    end = today - datetime.timedelta(days=1)  # 昨日まで（当日分は未確定のため除外）
    start = end - datetime.timedelta(days=6)  # 直近7日間
    date_range_label = f"{start.isoformat()} 〜 {end.isoformat()}"

    # ---------------- GA4：イベント別の発生回数 ----------------
    ga_lines: list[str] = []
    try:
        client = BetaAnalyticsDataClient(credentials=credentials)
        request = RunReportRequest(
            property=f"properties/{ga4_property_id}",
            date_ranges=[DateRange(start_date=start.isoformat(), end_date=end.isoformat())],
            dimensions=[Dimension(name="eventName")],
            metrics=[Metric(name="eventCount")],
        )
        response = client.run_report(request)
        rows = sorted(response.rows, key=lambda r: -int(r.metric_values[0].value))
        for row in rows:
            ga_lines.append(f"- {row.dimension_values[0].value}: {row.metric_values[0].value}件")
        if not ga_lines:
            ga_lines.append("（対象期間のデータがありませんでした）")
    except Exception as e:  # noqa: BLE001 — レポート生成自体は止めない
        ga_lines = [f"⚠️ GA4データの取得中にエラーが発生しました: {e}"]

    # ---------------- Search Console：検索キーワード上位10件 ----------------
    gsc_lines: list[str] = []
    try:
        service = build("searchconsole", "v1", credentials=credentials)
        body = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": ["query"],
            "rowLimit": 10,
        }
        result = service.searchanalytics().query(siteUrl=gsc_site_url, body=body).execute()
        rows = result.get("rows", [])
        if rows:
            for r in rows:
                query = r["keys"][0]
                impressions = int(r.get("impressions", 0))
                clicks = int(r.get("clicks", 0))
                position = r.get("position", 0)
                gsc_lines.append(
                    f"- 「{query}」: 表示 {impressions}回 / クリック {clicks}回 / 平均掲載順位 {position:.1f}位"
                )
        else:
            gsc_lines.append("（対象期間のデータがありませんでした）")
    except Exception as e:  # noqa: BLE001
        gsc_lines = [f"⚠️ Search Consoleデータの取得中にエラーが発生しました: {e}"]

    report = f"""# 📊 マッスルジム湘南店LP 週次レポート

対象期間: {date_range_label}（直近7日間）

## サイト上でのイベント発生回数（GA4）

{chr(10).join(ga_lines)}

LINEボタン・電話ボタン・Googleマップボタンなどのクリック件数は、`cta_click`イベントの
`cta_id`ごとの内訳として確認できます（GTM設定後に反映されます）。

## 検索結果での表示・クリック状況（Search Console／検索キーワード上位10件）

{chr(10).join(gsc_lines)}

「藤沢市 ジム」「藤沢市 ジム 24時間」「藤沢市 ジム 安い」「湘南 ジム おすすめ」
「マッスルジム 藤沢」「マッスルジム 湘南」等のキーワードでの表示順位の変化に注目してください。

---
このレポートは毎週月曜 9:00（日本時間）に自動生成されます。
数値の意味や見方は `docs/google-setup-guide.md` を参照してください。
"""

    with open("weekly_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    write_status("ok")
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
