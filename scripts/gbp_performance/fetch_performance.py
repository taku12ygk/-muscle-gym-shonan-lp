#!/usr/bin/env python3
"""
Googleビジネスプロフィール パフォーマンス取得スクリプト（骨格・未接続）

【現在の状態】
このスクリプトはまだ週次レポートのワークフローには組み込まれておらず、
GitHub Actionsから自動実行されることもありません（設計の土台のみ）。

理由や有効化までの流れは同フォルダの README.md を参照してください。

【将来、有効化する際の使い方（イメージ）】
必要なSecretsをGitHubに登録した上で、このスクリプトを実行すると、
直近28日間の「表示回数・電話クリック・経路検索・サイトクリック」等を取得し、
weekly_report.md と同様の形式でレポートに追記できるようにする想定です。

  - GOOGLE_SERVICE_ACCOUNT_JSON … GA4/Search Consoleと共通のサービスアカウント鍵
    （Businessプロフィールの「管理者」として追加されていること）
  - GBP_ACCOUNT_ID … ビジネスプロフィールのアカウントID
  - GBP_LOCATION_ID … 店舗（ロケーション）ID

このスクリプトはGoogleビジネスプロフィールへの投稿・返信・変更は一切行いません
（読み取り専用のスコープのみを使用する設計です）。
"""

from __future__ import annotations

import os
import sys

# 読み取り専用スコープ（将来、認証を有効化する際に使用）
SCOPES = ["https://www.googleapis.com/auth/business.manage"]

# 取得予定の指標（Business Profile Performance API の daily metrics）
METRICS = [
    "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH",
    "BUSINESS_IMPRESSIONS_MOBILE_SEARCH",
    "BUSINESS_IMPRESSIONS_DESKTOP_MAPS",
    "BUSINESS_IMPRESSIONS_MOBILE_MAPS",
    "CALL_CLICKS",
    "BUSINESS_DIRECTION_REQUESTS",
    "WEBSITE_CLICKS",
]


def env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def main() -> int:
    print("Googleビジネスプロフィールの自動取得は、まだ有効化されていません。")
    print("有効化までの流れは scripts/gbp_performance/README.md を参照してください。")

    required = ["GOOGLE_SERVICE_ACCOUNT_JSON", "GBP_ACCOUNT_ID", "GBP_LOCATION_ID"]
    missing = [name for name in required if not env(name)]
    if missing:
        print("未設定の項目（申請・承認後に登録予定）: " + ", ".join(missing))

    # NOTE: 承認・Secrets登録が完了したら、ここでGBP APIを呼び出す処理を実装します。
    # 例:
    #   from google.oauth2 import service_account
    #   from googleapiclient.discovery import build
    #   credentials = service_account.Credentials.from_service_account_info(..., scopes=SCOPES)
    #   service = build("businessprofileperformance", "v1", credentials=credentials)
    #   service.locations().fetchMultiDailyMetricsTimeSeries(...)
    # 口コミ取得・返信は別APIかつ「返信の自動投稿は行わない」方針を維持してください。

    return 0


if __name__ == "__main__":
    sys.exit(main())
