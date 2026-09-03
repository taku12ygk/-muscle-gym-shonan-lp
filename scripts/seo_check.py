#!/usr/bin/env python3
"""
SEOチェックスクリプト（マッスルジム湘南店LP）

PRを作成・更新するたびにGitHub Actionsから実行され、以下を確認します。
  - title / meta description / H1 / canonical / viewport の有無
  - 画像のalt属性の有無
  - 内部リンク（相対パス）が実際に存在するファイルを指しているか
  - robots.txt / sitemap.xml の整合性

デザイン・文章・画像そのものは一切変更しません。読み取りのみを行うチェックです。

標準ライブラリのみで動作します（追加インストール不要）。
"""

from __future__ import annotations

import sys
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# チェック対象のHTMLファイル（検索エンジンに見せたいページ）
HTML_FILES = ["index.html", "privacy.html", "tokushoho.html"]

# title / description の推奨文字数（日本語は全角想定のざっくり目安）
TITLE_MIN, TITLE_MAX = 10, 65
DESC_MIN, DESC_MAX = 50, 160


@dataclass
class PageIssues:
    path: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class SeoHTMLParser(HTMLParser):
    """必要なタグだけを拾う、超シンプルなHTMLパーサー。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta_description = None
        self.meta_robots = None
        self.has_viewport = False
        self.canonical_href = None
        self.h1_texts: list[str] = []
        self._in_h1 = False
        self._h1_buf = ""
        self.images: list[dict] = []
        self.links: list[dict] = []  # <a href> のみ

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attrs_d.get("name") or "").lower()
            if name == "description":
                self.meta_description = attrs_d.get("content", "")
            elif name == "robots":
                self.meta_robots = attrs_d.get("content", "")
            elif name == "viewport":
                self.has_viewport = True
        elif tag == "link":
            if (attrs_d.get("rel") or "").lower() == "canonical":
                self.canonical_href = attrs_d.get("href")
        elif tag == "h1":
            self._in_h1 = True
            self._h1_buf = ""
        elif tag == "img":
            self.images.append(attrs_d)
        elif tag == "a":
            if attrs_d.get("href"):
                self.links.append(attrs_d)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
            self.h1_texts.append(self._h1_buf.strip())

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_h1:
            self._h1_buf += data


def check_html_file(rel_path: str) -> PageIssues:
    issues = PageIssues(path=rel_path)
    full_path = ROOT / rel_path
    if not full_path.exists():
        issues.errors.append("ファイルが見つかりません。")
        return issues

    html = full_path.read_text(encoding="utf-8")
    parser = SeoHTMLParser()
    parser.feed(html)

    # title
    title = (parser.title or "").strip()
    if not title:
        issues.errors.append("titleタグ（ページタイトル）がありません。")
    elif not (TITLE_MIN <= len(title) <= TITLE_MAX):
        issues.warnings.append(
            f"titleの文字数が目安（{TITLE_MIN}〜{TITLE_MAX}文字）から外れています（現在{len(title)}文字）。"
        )

    # description（noindexページは必須ではないため警告のみ）
    desc = (parser.meta_description or "").strip()
    is_noindex = "noindex" in (parser.meta_robots or "").lower()
    if not desc:
        if not is_noindex:
            issues.errors.append("meta descriptionがありません。")
        else:
            issues.warnings.append("meta descriptionがありません（noindexページのため必須ではありません）。")
    elif not (DESC_MIN <= len(desc) <= DESC_MAX):
        issues.warnings.append(
            f"descriptionの文字数が目安（{DESC_MIN}〜{DESC_MAX}文字）から外れています（現在{len(desc)}文字）。"
        )

    # H1
    if len(parser.h1_texts) == 0:
        issues.errors.append("見出し（H1）がありません。")
    elif len(parser.h1_texts) > 1:
        issues.errors.append(f"見出し（H1）が{len(parser.h1_texts)}個あります（1ページに1個が基本です）。")

    # canonical（noindexページは必須ではないため警告のみ）
    if not parser.canonical_href:
        if not is_noindex:
            issues.errors.append("canonicalタグがありません。")
        else:
            issues.warnings.append("canonicalタグがありません（noindexページのため必須ではありません）。")
    elif not parser.canonical_href.startswith("http"):
        issues.warnings.append("canonicalが絶対URL（https://から始まるURL）になっていません。")

    # viewport
    if not parser.has_viewport:
        issues.errors.append("viewportの指定がなく、スマホでの表示が崩れる可能性があります。")

    # 画像alt
    missing_alt = [img.get("src", "(srcなし)") for img in parser.images if "alt" not in img]
    if missing_alt:
        issues.errors.append(
            "alt（画像の説明文）が設定されていない画像があります: " + ", ".join(missing_alt)
        )

    # 内部リンク切れチェック（相対パスのみ。外部サイト・電話・メール・アンカーは対象外）
    broken = []
    for a in parser.links:
        href = a["href"]
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        target = (full_path.parent / href.split("#")[0]).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            continue  # リポジトリ外は対象外
        if not target.exists():
            broken.append(href)
    if broken:
        issues.errors.append("リンク切れの可能性がある内部リンク: " + ", ".join(broken))

    return issues


def check_robots_and_sitemap() -> PageIssues:
    issues = PageIssues(path="robots.txt / sitemap.xml")

    robots_path = ROOT / "robots.txt"
    sitemap_path = ROOT / "sitemap.xml"

    if not robots_path.exists():
        issues.errors.append("robots.txtがありません。")
    else:
        robots_text = robots_path.read_text(encoding="utf-8")
        if "Sitemap:" not in robots_text:
            issues.warnings.append("robots.txtにSitemapの記載がありません。")

    if not sitemap_path.exists():
        issues.errors.append("sitemap.xmlがありません。")
    else:
        try:
            tree = ET.parse(sitemap_path)
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [el.text for el in tree.getroot().findall("sm:url/sm:loc", ns)]
            if not locs:
                issues.errors.append("sitemap.xmlにURLが1件も登録されていません。")
            for loc in locs:
                if not loc or not loc.startswith("https://"):
                    issues.errors.append(f"sitemap.xml内のURLが不正です: {loc}")
        except ET.ParseError as e:
            issues.errors.append(f"sitemap.xmlの形式が壊れています: {e}")

    return issues


def main() -> int:
    all_issues: list[PageIssues] = []
    for rel_path in HTML_FILES:
        if (ROOT / rel_path).exists():
            all_issues.append(check_html_file(rel_path))
    all_issues.append(check_robots_and_sitemap())

    total_errors = sum(len(p.errors) for p in all_issues)
    total_warnings = sum(len(p.warnings) for p in all_issues)

    lines = ["# 🔍 SEO自動チェック結果\n"]
    if total_errors == 0 and total_warnings == 0:
        lines.append("問題は見つかりませんでした ✅\n")
    for p in all_issues:
        if not p.errors and not p.warnings:
            continue
        lines.append(f"## {p.path}")
        for e in p.errors:
            lines.append(f"- ❌ **要対応**: {e}")
        for w in p.warnings:
            lines.append(f"- ⚠️ 参考: {w}")
        lines.append("")

    lines.append(f"\n合計: ❌ 要対応 {total_errors}件 / ⚠️ 参考 {total_warnings}件")
    lines.append(
        "\n> ⚠️の項目は「今後の改善候補」であり、マージを妨げるものではありません。"
        "❌の項目のみ確認をお願いします。"
    )

    report = "\n".join(lines)
    print(report)

    summary_path = Path("GITHUB_STEP_SUMMARY_LOCAL.md" if not __import__("os").environ.get("GITHUB_STEP_SUMMARY") else __import__("os").environ["GITHUB_STEP_SUMMARY"])
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(report + "\n")

    # レポート本文をPRコメント用ファイルとしても保存
    (ROOT / "seo_report.md").write_text(report, encoding="utf-8")

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
