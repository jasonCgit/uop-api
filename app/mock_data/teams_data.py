# REAL: Replace with MySQL teams table or Directory Service

_next_team_id = 1


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
    teams = []
    for n in names:
        slug = n.lower().replace(" ", "-").replace("&", "and")
        teams.append({
            "id": _next_team_id,
            "name": n,
            "emails": [f"{slug}@jpmchase.com", f"{slug}-oncall@jpmchase.com"],
            "teams_channels": [f"#{slug}-alerts", f"#{slug}-general"],
        })
        _next_team_id += 1
    return teams

TEAMS = _build_initial_teams()
