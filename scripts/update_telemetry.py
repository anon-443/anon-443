#!/usr/bin/env python3
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", "anon-443")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

FEATURED = [
    "ZTNA-Self-Healing-Network-Architecture",
    "cybershield-sme",
    "Secure-Distributed-File-System-with-AI-Monitoring-Agent",
    "YARA-Strings-Metadata-Static-Malware-Analyzer-Tool",
]


def get_json(url: str):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def repo_data(name: str):
    return get_json(f"https://api.github.com/repos/{urllib.parse.quote(OWNER)}/{urllib.parse.quote(name)}")


def esc(value: object) -> str:
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def badge(x: int, y: int, label: str, value: str, color: str, width: int = 250) -> str:
    return f'''<g transform="translate({x} {y})"><rect width="{width}" height="58" rx="10" fill="#111827" stroke="#334155"/><text x="18" y="23" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" fill="#94A3B8">{esc(label)}</text><text x="18" y="44" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="18" font-weight="700" fill="{color}">{esc(value)}</text></g>'''


def main():
    repos = [repo_data(name) for name in FEATURED]
    public_repos = get_json(f"https://api.github.com/users/{urllib.parse.quote(OWNER)}/repos?per_page=100&type=public")
    total_stars = sum(int(repo.get("stargazers_count", 0)) for repo in repos)
    total_forks = sum(int(repo.get("forks_count", 0)) for repo in repos)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    telemetry = {
        "owner": OWNER,
        "updated_at": updated,
        "public_repositories": len(public_repos),
        "featured_projects": len(repos),
        "featured_stars": total_stars,
        "featured_forks": total_forks,
        "security_domains": 4,
        "threat_signal_families": 4,
        "source": "GitHub repository metadata + documented project capabilities",
        "live_threat_data": False,
    }
    (ASSETS / "telemetry.json").write_text(json.dumps(telemetry, indent=2) + "\n", encoding="utf-8")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 250" role="img" aria-labelledby="title desc"><title id="title">Adeen security telemetry</title><desc id="desc">Daily project-derived security telemetry. Not live Internet threat intelligence.</desc><rect width="820" height="250" rx="18" fill="#070A12" stroke="#334155"/><text x="30" y="38" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="18" font-weight="700" fill="#00D9A6">SECURITY TELEMETRY // DAILY SNAPSHOT</text><text x="30" y="62" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" fill="#F97316">PROJECT-DERIVED SIGNALS · NOT LIVE INTERNET THREAT INTELLIGENCE · UPDATED {esc(updated)}</text>{badge(30, 82, 'PUBLIC REPOSITORIES', len(public_repos), '#00D9A6')}{badge(290, 82, 'FEATURED PROJECTS', len(repos), '#A78BFA')}{badge(550, 82, 'FEATURED STARS', total_stars, '#F97316')}{badge(30, 152, 'SECURITY DOMAINS', 4, '#00D9A6')}{badge(290, 152, 'THREAT SIGNAL FAMILIES', 4, '#E11D48')}{badge(550, 152, 'FEATURED FORKS', total_forks, '#A78BFA')}</svg>'''
    (ASSETS / "security-telemetry.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
