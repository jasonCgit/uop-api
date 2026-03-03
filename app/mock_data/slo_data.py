# REAL: Replace with SLO Monitoring Platform API

DEPLOYMENT_OVERRIDES = {
    # Connect OS (88180) — 6 components across 18 deployments
    # Components: connect-portal, connect-cloud-gw, connect-auth-svc, connect-home-app-na, connect-home-app-apac, connect-home-app-emea
    "connect-os": [
        {"id": "112224", "deployment_id": "112224", "label": "Connect OS Critical Applications and Services AWS - Global (xSwiss)", "cpof": True,  "rto": 4,    "component_ids": ["connect-cloud-gw", "connect-auth-svc", "connect-portal"]},
        {"id": "111848", "deployment_id": "111848", "label": "Connect OS Mobile AWS - Global",                                     "cpof": False, "rto": 8,    "component_ids": ["connect-portal"]},
        {"id": "110175", "deployment_id": "110175", "label": "Connect OS Internet Facing Applications and Services Gaia Cloud Foundry - NA", "cpof": True, "rto": 4, "component_ids": ["connect-home-app-na", "connect-auth-svc"]},
        {"id": "103719", "deployment_id": "103719", "label": "Connect OS Legacy Infrastructure - NA",                              "cpof": False, "rto": 24,   "component_ids": ["connect-home-app-na"]},
        {"id": "103720", "deployment_id": "103720", "label": "Connect Desktop - DEV",                                              "cpof": False, "rto": None, "component_ids": []},
        {"id": "103721", "deployment_id": "103721", "label": "Connect Desktop - UAT",                                              "cpof": False, "rto": None, "component_ids": []},
        {"id": "103722", "deployment_id": "103722", "label": "Connect Desktop - PROD",                                             "cpof": True,  "rto": 4,    "component_ids": ["connect-portal", "connect-cloud-gw"]},
        {"id": "103723", "deployment_id": "103723", "label": "Connect Desktop - Global Link",                                      "cpof": False, "rto": 12,   "component_ids": []},
        {"id": "104739", "deployment_id": "104739", "label": "Connect OS WordPress CMS Gaia Cloud Foundry - NA",                   "cpof": False, "rto": 24,   "component_ids": []},
        {"id": "108750", "deployment_id": "108750", "label": "Connect OS AI Machine Learning",                                     "cpof": False, "rto": 12,   "component_ids": []},
        {"id": "109718", "deployment_id": "109718", "label": "Connect OS Critical Applications and Services Gaia Cloud Foundry - Global", "cpof": True, "rto": 4, "component_ids": ["connect-cloud-gw", "connect-auth-svc"]},
        {"id": "109719", "deployment_id": "109719", "label": "Connect OS Mobile Gaia Cloud Foundry - Global",                      "cpof": False, "rto": 8,    "component_ids": ["connect-portal"]},
        {"id": "109720", "deployment_id": "109720", "label": "Connect OS Non-Critical Applications and Services Gaia Cloud Foundry - Global", "cpof": False, "rto": 24, "component_ids": []},
        {"id": "109739", "deployment_id": "109739", "label": "Connect OS Swiss Applications and Services Gaia Cloud Foundry - SwissNet", "cpof": True, "rto": 4, "component_ids": ["connect-auth-svc"]},
        {"id": "111835", "deployment_id": "111835", "label": "Connect OS Gaia Oracle Services - Global",                           "cpof": False, "rto": 12,   "component_ids": []},
        {"id": "111836", "deployment_id": "111836", "label": "Connect OS User Metrics Elastic/Cassandra - Global",                 "cpof": False, "rto": 24,   "component_ids": []},
        {"id": "61867",  "deployment_id": "61867",  "label": "Connect OS Legacy Infrastructure - Asia",                            "cpof": False, "rto": 24,   "component_ids": ["connect-home-app-apac"]},
        {"id": "61868",  "deployment_id": "61868",  "label": "Connect OS Legacy Infrastructure - EMEA",                            "cpof": False, "rto": 24,   "component_ids": ["connect-home-app-emea"]},
    ],
    # Advisor Connect (90176) — 10 components across 10 deployments
    # Components: connect-profile-svc, connect-coverage-app, connect-notification, connect-data-sync,
    #             connect-doc-svc, connect-pref-svc, connect-audit-svc, active-advisory, ipbol-account, ipbol-doc-domain
    "advisor-connect": [
        {"id": "109974", "deployment_id": "109974", "label": "Advisor Connect Suite - NA - AWS",       "cpof": True,  "rto": 4,    "component_ids": ["connect-profile-svc", "connect-coverage-app", "connect-notification", "connect-data-sync"]},
        {"id": "112169", "deployment_id": "112169", "label": "ADVISOR CONNECT AWS - NA",               "cpof": True,  "rto": 4,    "component_ids": ["connect-coverage-app", "ipbol-account", "ipbol-doc-domain"]},
        {"id": "102024", "deployment_id": "102024", "label": "ADVISOR CONNECT - EMEA",                 "cpof": True,  "rto": 8,    "component_ids": ["connect-profile-svc", "connect-doc-svc"]},
        {"id": "102025", "deployment_id": "102025", "label": "ADVISOR CONNECT - Asia",                 "cpof": False, "rto": 8,    "component_ids": ["connect-profile-svc", "connect-pref-svc"]},
        {"id": "102026", "deployment_id": "102026", "label": "ADVISOR CONNECT - US",                   "cpof": True,  "rto": 4,    "component_ids": ["connect-coverage-app", "connect-notification", "active-advisory"]},
        {"id": "104948", "deployment_id": "104948", "label": "JPMS Advisor Connect Deployment",        "cpof": False, "rto": 12,   "component_ids": ["active-advisory", "connect-audit-svc"]},
        {"id": "109355", "deployment_id": "109355", "label": "ADVISOR CONNECT - Swiss AWS",            "cpof": True,  "rto": 4,    "component_ids": ["connect-profile-svc", "connect-pref-svc"]},
        {"id": "62056",  "deployment_id": "62056",  "label": "Tool for Reaching and Acquiring Clients (TRAC)", "cpof": False, "rto": 24, "component_ids": ["connect-data-sync", "connect-doc-svc"]},
        {"id": "114650", "deployment_id": "114650", "label": "ADVISOR CONNECT AWS - AP",               "cpof": False, "rto": 8,    "component_ids": ["connect-profile-svc", "connect-notification"]},
        {"id": "115060", "deployment_id": "115060", "label": "ADVISOR CONNECT AWS - EU",               "cpof": False, "rto": 8,    "component_ids": ["connect-profile-svc", "connect-doc-svc", "connect-audit-svc"]},
    ],
    # Spectrum Portfolio Management Equities (90215) — 14 components across 5 deployments
    # Components: spieq-ui-service, spieq-api-gateway, spieq-trade-service, spieq-portfolio-svc,
    #             spieq-pricing-engine, spieq-risk-service, spieq-order-router, spieq-market-data,
    #             spieq-compliance-svc, spieq-settlement-svc, spieq-audit-trail, spieq-notif-svc,
    #             payment-gateway, email-notification
    "spectrum-portfolio-management-(equities)": [
        {"id": "64958",  "deployment_id": "64958",  "label": "Spectrum PI - Equities Deployment",           "cpof": True,  "rto": 4,  "component_ids": ["spieq-ui-service", "spieq-api-gateway", "spieq-trade-service", "spieq-portfolio-svc", "spieq-order-router"]},
        {"id": "103262", "deployment_id": "103262", "label": "Spectrum PI - Equities - Deployment",         "cpof": False, "rto": 8,  "component_ids": ["spieq-pricing-engine", "spieq-risk-service", "spieq-market-data"]},
        {"id": "109606", "deployment_id": "109606", "label": "Spectrum PI - Equities PSF",                  "cpof": True,  "rto": 4,  "component_ids": ["spieq-compliance-svc", "spieq-settlement-svc", "payment-gateway"]},
        {"id": "110724", "deployment_id": "110724", "label": "Spectrum PI - Equities GKP Config Server",    "cpof": False, "rto": 12, "component_ids": ["spieq-audit-trail", "spieq-notif-svc", "email-notification"]},
        {"id": "112256", "deployment_id": "112256", "label": "Spectrum PI - Equities Dep 5",                "cpof": False, "rto": 24, "component_ids": []},
    ],
}


# Mock SLO data per app slug — critical/warning apps get explicit data; healthy apps use default
APP_SLO_DATA = {
    # Critical apps
    "morgan-money":                             {"target": 99.9,  "current": 99.12, "error_budget": 12, "trend": "down",   "burn_rate": "4.2x",  "breach_eta": "6h",   "status": "critical"},
    "quantum":                                  {"target": 99.9,  "current": 98.9,  "error_budget": 8,  "trend": "down",   "burn_rate": "5.8x",  "breach_eta": "3h",   "status": "critical"},
    "jedi---j.p.-morgan-etf-data-intelligence": {"target": 99.9,  "current": 99.2,  "error_budget": 15, "trend": "down",   "burn_rate": "3.5x",  "breach_eta": "8h",   "status": "critical"},
    "order-decision-engine":                    {"target": 99.9,  "current": 98.5,  "error_budget": 5,  "trend": "down",   "burn_rate": "8.2x",  "breach_eta": "2h",   "status": "critical"},
    "awm-entitlements-aka-weave":               {"target": 99.9,  "current": 99.0,  "error_budget": 10, "trend": "down",   "burn_rate": "4.5x",  "breach_eta": "5h",   "status": "critical"},
    "pam:-gwm-party-and-account-maintenance":   {"target": 99.9,  "current": 99.15, "error_budget": 14, "trend": "down",   "burn_rate": "3.8x",  "breach_eta": "7h",   "status": "critical"},
    "murex":                                    {"target": 99.9,  "current": 99.3,  "error_budget": 18, "trend": "down",   "burn_rate": "3.1x",  "breach_eta": "12h",  "status": "critical"},
    "omni-core-accounting-(omnitrust)":         {"target": 99.9,  "current": 98.8,  "error_budget": 7,  "trend": "down",   "burn_rate": "6.1x",  "breach_eta": "4h",   "status": "critical"},
    # Warning apps
    "am-pmt-routing-service":                   {"target": 99.0,  "current": 98.8,  "error_budget": 42, "trend": "stable", "burn_rate": "1.2x",  "breach_eta": "72h",  "status": "warning"},
    "info-hub-and-data-oversight":              {"target": 99.5,  "current": 99.2,  "error_budget": 35, "trend": "down",   "burn_rate": "1.5x",  "breach_eta": "48h",  "status": "warning"},
    "gm-solutions-bmt-research-hb-desktop":     {"target": 99.0,  "current": 98.6,  "error_budget": 30, "trend": "down",   "burn_rate": "2.0x",  "breach_eta": "24h",  "status": "warning"},
    "ops-party":                                {"target": 99.0,  "current": 98.7,  "error_budget": 38, "trend": "stable", "burn_rate": "1.1x",  "breach_eta": None,   "status": "warning"},
    "salerio":                                  {"target": 99.0,  "current": 98.5,  "error_budget": 28, "trend": "down",   "burn_rate": "1.8x",  "breach_eta": "36h",  "status": "warning"},
    "onesentinel":                              {"target": 99.0,  "current": 98.4,  "error_budget": 25, "trend": "down",   "burn_rate": "2.2x",  "breach_eta": "18h",  "status": "warning"},
    "acey-eagle-stari":                         {"target": 99.0,  "current": 98.9,  "error_budget": 45, "trend": "stable", "burn_rate": "0.9x",  "breach_eta": None,   "status": "warning"},
    "meridian-data-services-platform":          {"target": 99.0,  "current": 98.7,  "error_budget": 32, "trend": "down",   "burn_rate": "1.6x",  "breach_eta": "40h",  "status": "warning"},
    "ipb-payments":                             {"target": 99.0,  "current": 98.8,  "error_budget": 40, "trend": "stable", "burn_rate": "1.0x",  "breach_eta": None,   "status": "warning"},
    "ipb-brokerage":                            {"target": 99.0,  "current": 98.6,  "error_budget": 33, "trend": "down",   "burn_rate": "1.7x",  "breach_eta": "38h",  "status": "warning"},
    "global-security-transfer":                 {"target": 99.0,  "current": 98.5,  "error_budget": 29, "trend": "down",   "burn_rate": "1.9x",  "breach_eta": "30h",  "status": "warning"},
    "wm-swift-middleware":                      {"target": 99.0,  "current": 98.4,  "error_budget": 26, "trend": "down",   "burn_rate": "2.1x",  "breach_eta": "20h",  "status": "warning"},
    "pb-loan-origination-system":               {"target": 99.0,  "current": 98.7,  "error_budget": 35, "trend": "stable", "burn_rate": "1.3x",  "breach_eta": None,   "status": "warning"},
    # Non-AWM critical/warning apps
    "credit-card-processing-engine":            {"target": 99.99, "current": 99.82, "error_budget": 9,  "trend": "down",   "burn_rate": "5.0x",  "breach_eta": "4h",   "status": "critical"},
    "consumer-lending-gateway":                 {"target": 99.9,  "current": 99.5,  "error_budget": 38, "trend": "down",   "burn_rate": "1.4x",  "breach_eta": "48h",  "status": "warning"},
    "analytics-workbench":                      {"target": 99.0,  "current": 98.6,  "error_budget": 32, "trend": "stable", "burn_rate": "1.3x",  "breach_eta": None,   "status": "warning"},
    "trade-execution-engine":                   {"target": 99.9,  "current": 99.4,  "error_budget": 28, "trend": "down",   "burn_rate": "2.0x",  "breach_eta": "24h",  "status": "warning"},
    "corporate-treasury-portal":                {"target": 99.5,  "current": 99.1,  "error_budget": 35, "trend": "down",   "burn_rate": "1.5x",  "breach_eta": "36h",  "status": "warning"},
    "real-time-payments-gateway":               {"target": 99.99, "current": 99.75, "error_budget": 6,  "trend": "down",   "burn_rate": "7.2x",  "breach_eta": "2h",   "status": "critical"},
    "enterprise-monitoring-platform":           {"target": 99.9,  "current": 99.5,  "error_budget": 40, "trend": "stable", "burn_rate": "1.1x",  "breach_eta": None,   "status": "warning"},
    "network-automation-suite":                 {"target": 99.9,  "current": 99.4,  "error_budget": 30, "trend": "down",   "burn_rate": "1.8x",  "breach_eta": "30h",  "status": "warning"},
}
