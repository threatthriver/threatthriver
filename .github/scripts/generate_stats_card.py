#!/usr/bin/env python3
"""Generate a custom, editorial-style GitHub stats SVG card.

Design language mirrors oxpid.in: big numbers, small letterspaced
caption labels, thin vertical dividers, lots of whitespace, monochrome
on a warm off-white background.

Run in CI with env GITHUB_TOKEN and USERNAME set. Falls back to the
public REST/GraphQL API; writes assets/stats.svg.
"""
import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

USERNAME = os.environ.get("USERNAME", "threatthriver")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")

# Theme (OXPID-inspired)
BG = "#FCF9FB"
INK = "#2E2E38"       # near-black for big numbers
SUB = "#8A8A9C"       # muted caption text
ACCENT = "#B893C7"    # purple accent
LINE = "#E6E1EC"      # hairline dividers


def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "stats-card-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def rest(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "User-Agent": "stats-card-generator",
            **({"Authorization": f"bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_stats():
    stats = {
        "contributions": 0,
        "commits": 0,
        "prs": 0,
        "issues": 0,
        "stars": 0,
        "repos": 0,
        "followers": 0,
    }

    # REST fallbacks (work without a token for public data)
    try:
        user = rest(f"/users/{USERNAME}")
        stats["repos"] = user.get("public_repos", 0)
        stats["followers"] = user.get("followers", 0)
    except Exception as e:
        print("user rest failed:", e)

    try:
        total_stars = 0
        page = 1
        while True:
            repos = rest(f"/users/{USERNAME}/repos?per_page=100&page={page}&type=owner")
            if not repos:
                break
            total_stars += sum(r.get("stargazers_count", 0) for r in repos)
            if len(repos) < 100:
                break
            page += 1
        stats["stars"] = total_stars
    except Exception as e:
        print("repos rest failed:", e)

    # GraphQL for the richer numbers (needs a token)
    if TOKEN:
        q = """
        query($login: String!) {
          user(login: $login) {
            contributionsCollection {
              totalCommitContributions
              restrictedContributionsCount
              contributionCalendar { totalContributions }
            }
            pullRequests { totalCount }
            issues { totalCount }
          }
        }
        """
        try:
            data = gql(q, {"login": USERNAME})
            u = data["data"]["user"]
            cc = u["contributionsCollection"]
            stats["contributions"] = cc["contributionCalendar"]["totalContributions"]
            stats["commits"] = (
                cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
            )
            stats["prs"] = u["pullRequests"]["totalCount"]
            stats["issues"] = u["issues"]["totalCount"]
        except Exception as e:
            print("graphql failed:", e)

    return stats


def fmt(n):
    return f"{n:,}"


def build_svg(stats):
    W, H = 820, 300
    pad = 56

    # Four primary stat columns (the hero row, OXPID style)
    primary = [
        (fmt(stats["contributions"]), "TOTAL CONTRIBUTIONS"),
        (fmt(stats["commits"]), "COMMITS"),
        (fmt(stats["stars"]), "STARS EARNED"),
        (fmt(stats["prs"]), "PULL REQUESTS"),
    ]

    # Secondary smaller row
    secondary = [
        (fmt(stats["repos"]), "REPOSITORIES"),
        (fmt(stats["issues"]), "ISSUES"),
        (fmt(stats["followers"]), "FOLLOWERS"),
    ]

    col_w = (W - pad * 2) / 4
    sec_w = (W - pad * 2) / 3

    now = datetime.now(timezone.utc).strftime("%b %d, %Y")

    parts = []
    parts.append(
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'fill="none" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="GitHub stats for {USERNAME}">'
    )

    # Fonts
    parts.append(
        "<style>"
        f".big{{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;"
        f"font-weight:700;fill:{INK};font-size:46px;letter-spacing:-1px}}"
        f".unit{{font-family:'Segoe UI',Arial,sans-serif;font-weight:600;"
        f"fill:{ACCENT};font-size:16px}}"
        f".cap{{font-family:'Segoe UI',Arial,sans-serif;font-weight:600;"
        f"fill:{SUB};font-size:9.5px;letter-spacing:2.5px}}"
        f".mid{{font-family:'Segoe UI',Arial,sans-serif;font-weight:700;"
        f"fill:{INK};font-size:30px;letter-spacing:-0.5px}}"
        f".brand{{font-family:'Segoe UI',Arial,sans-serif;font-weight:700;"
        f"fill:{INK};font-size:13px;letter-spacing:3px}}"
        f".meta{{font-family:'Segoe UI',Arial,sans-serif;font-weight:500;"
        f"fill:{SUB};font-size:10px;letter-spacing:1.5px}}"
        "</style>"
    )

    # Background + border
    parts.append(
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
        f'fill="{BG}" stroke="{LINE}"/>'
    )

    # Header: brand + run-style meta
    parts.append(f'<text x="{pad}" y="48" class="brand">GITHUB · {USERNAME.upper()}</text>')
    parts.append(f'<text x="{W-pad}" y="48" text-anchor="end" class="meta">UPDATED {now.upper()}</text>')
    parts.append(f'<line x1="{pad}" y1="66" x2="{W-pad}" y2="66" stroke="{LINE}"/>')

    # Primary row
    row_y = 150
    for i, (val, cap) in enumerate(primary):
        x = pad + col_w * i
        if i > 0:
            parts.append(
                f'<line x1="{x-0.5:.1f}" y1="100" x2="{x-0.5:.1f}" y2="178" stroke="{LINE}"/>'
            )
        tx = x + 24
        parts.append(f'<text x="{tx:.1f}" y="{row_y}" class="big">{val}</text>')
        parts.append(f'<text x="{tx:.1f}" y="{row_y+26}" class="cap">{cap}</text>')

    # Divider between rows
    parts.append(f'<line x1="{pad}" y1="208" x2="{W-pad}" y2="208" stroke="{LINE}"/>')

    # Secondary row
    srow_y = 258
    for i, (val, cap) in enumerate(secondary):
        x = pad + sec_w * i
        if i > 0:
            parts.append(
                f'<line x1="{x-0.5:.1f}" y1="226" x2="{x-0.5:.1f}" y2="280" stroke="{LINE}"/>'
            )
        tx = x + 24
        parts.append(f'<text x="{tx:.1f}" y="{srow_y}" class="mid">{val}</text>')
        parts.append(f'<text x="{tx:.1f}" y="{srow_y+22}" class="cap">{cap}</text>')

    parts.append("</svg>")
    return "".join(parts)


def main():
    stats = fetch_stats()
    # Allow seeding/overriding any stat via env (e.g. SEED_CONTRIBUTIONS=1625)
    force_seed = os.environ.get("FORCE_SEED") == "1"
    for key in list(stats.keys()):
        env_val = os.environ.get(f"SEED_{key.upper()}")
        if env_val and (force_seed or not stats[key]):
            try:
                stats[key] = int(env_val)
            except ValueError:
                pass
    print("stats:", stats)
    svg = build_svg(stats)
    os.makedirs("assets", exist_ok=True)
    with open("assets/stats.svg", "w") as f:
        f.write(svg)
    print("wrote assets/stats.svg")


if __name__ == "__main__":
    main()
