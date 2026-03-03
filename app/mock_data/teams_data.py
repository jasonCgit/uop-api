# REAL: Replace with MySQL teams table or Directory Service

import random as _random

from .directory_data import DIRECTORY

_random.seed(99)  # Deterministic seeding for team members

_next_team_id = 1

MEMBER_ROLES = [
    "SRE",
    "App Owner",
    "Dev Lead",
    "Engineering Manager",
    "Product Owner",
    "QA Lead",
    "Platform Engineer",
    "Scrum Master",
]


def _build_initial_teams():
    global _next_team_id
    names = [
        "Client Data", "Spectrum Core", "Liquidity Mgmt", "JPMAIM Platform",
        "Portfolio Mgmt", "Trading", "Middle Office", "Transaction Mgmt",
        "Guidelines", "Investment Acctg", "Ref Data", "Tech Shared Svc",
        "Connect Platform", "Party & Account", "Portfolio Holdings",
        "Service Desktop", "IPB Banking", "IPB Execute", "PBA Payments",
        "US Brokerage", "Asset Transfers", "Content", "IPB Core Banking",
        "Mutual Funds", "Core Accounting", "Work Orchestration",
        "Cross Asset Trading", "Lending", "Mortgages", "Portfolio Impl",
        "PM Toolkit", "Mobile Engineering", "Lending Platform", "Branch Tech",
        "Cards Platform", "Data Platform", "Analytics Eng", "Data Governance",
        "Electronic Trading", "FX Technology", "Syndicated Lending",
        "Treasury Tech", "Payments Core", "International Pmts",
        "Digital Platform", "API Platform", "IAM Engineering", "Observability",
        "Cloud Eng", "Network Eng", "HR Technology", "L&D Technology",
        "Container Eng", "Network Automation", "Traffic Eng",
    ]

    # Distribute directory people across teams
    pool = list(DIRECTORY)
    _random.shuffle(pool)
    pool_idx = 0

    teams = []
    for n in names:
        slug = n.lower().replace(" ", "-").replace("&", "and")

        # 2-5 members per team, first one is always SRE
        member_count = _random.randint(2, 5)
        members = []
        for j in range(member_count):
            if pool_idx >= len(pool):
                break
            person = pool[pool_idx]
            pool_idx += 1
            role = "SRE" if j == 0 else _random.choice(MEMBER_ROLES)
            members.append({
                "sid": person["sid"],
                "firstName": person["firstName"],
                "lastName": person["lastName"],
                "email": person["email"],
                "role": role,
            })

        teams.append({
            "id": _next_team_id,
            "name": n,
            "emails": [f"{slug}@jpmchase.com", f"{slug}-oncall@jpmchase.com"],
            "teams_channels": [f"#{slug}-alerts", f"#{slug}-general"],
            "members": members,
        })
        _next_team_id += 1
    return teams


TEAMS = _build_initial_teams()
