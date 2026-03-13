# REAL: Replace with ERMA/V12 Knowledge Graph API + Dynatrace

NODES = [
    # Core platform services
    {"id": "api-gateway",          "label": "API-GATEWAY",                               "status": "healthy",  "team": "Platform",    "sla": "99.99%", "incidents_30d": 0},
    {"id": "meridian-query",       "label": "MERIDIAN~~SERVICE-QUERY~V1",                "status": "critical", "team": "Trading",     "sla": "99.5%",  "incidents_30d": 7},
    {"id": "meridian-order",       "label": "MERIDIAN~~SERVICE-ORDER~V1",                "status": "warning",  "team": "Trading",     "sla": "99.5%",  "incidents_30d": 3},
    {"id": "sb-service-order",     "label": "SPRINGBOOT (PROD) SERVICE-ORDER",           "status": "healthy",  "team": "Orders",      "sla": "99.0%",  "incidents_30d": 0},
    {"id": "sb-service-query",     "label": "SPRINGBOOT (PROD) SERVICE-QUERY",           "status": "healthy",  "team": "Orders",      "sla": "99.0%",  "incidents_30d": 0},
    {"id": "active-advisory",      "label": "ACTIVE-ADVISORY",                           "status": "healthy",  "team": "Advisory",    "sla": "99.0%",  "incidents_30d": 1},
    {"id": "ipbol-account",        "label": "IPBOL-ACCOUNT-SERVICES",                    "status": "critical", "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 4},
    {"id": "ipbol-account-green",  "label": "IPBOL-ACCOUNT-SERVICES#GREEN",              "status": "healthy",  "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ipbol-contact-sync",   "label": "IPBOL-CONTACT-SYNC_OFFLINE-NOTIFICATIONS",  "status": "healthy",  "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ipbol-doc-delivery",   "label": "IPBOL-DOC-DELIVERY#GREEN",                  "status": "healthy",  "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ipbol-doc-domain",     "label": "IPBOL-DOC-DOMAIN",                          "status": "critical", "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 4},
    {"id": "ipbol-doc-domain-g",   "label": "IPBOL-DOC-DOMAIN#GREEN",                    "status": "healthy",  "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ipbol-investments",    "label": "IPBOL-INVESTMENTS-SERVICES",                "status": "warning",  "team": "IPBOL",       "sla": "99.0%",  "incidents_30d": 3},
    {"id": "ipbol-manager-auth",   "label": "IPBOL-MANAGER-AUTH#GREEN",                  "status": "healthy",  "team": "IPBOL",       "sla": "99.5%",  "incidents_30d": 0},
    {"id": "payment-gateway",      "label": "PAYMENT-GATEWAY-API",                       "status": "critical", "team": "Payments",    "sla": "99.99%", "incidents_30d": 8},
    {"id": "email-notification",   "label": "EMAIL-NOTIFICATION-SERVICE",                "status": "critical", "team": "Messaging",   "sla": "99.5%",  "incidents_30d": 5},
    {"id": "auth-service",         "label": "AUTH-SERVICE-V2",                           "status": "healthy",  "team": "Security",    "sla": "99.99%", "incidents_30d": 0},
    {"id": "cache-layer",          "label": "REDIS-CACHE-CLUSTER",                       "status": "healthy",  "team": "Platform",    "sla": "99.9%",  "incidents_30d": 1},
    {"id": "db-primary",           "label": "POSTGRES-DB-PRIMARY",                       "status": "critical", "team": "Database",    "sla": "99.99%", "incidents_30d": 9},
    {"id": "db-replica",           "label": "POSTGRES-DB-REPLICA",                       "status": "warning",  "team": "Database",    "sla": "99.9%",  "incidents_30d": 2},
    {"id": "message-queue",        "label": "KAFKA-MESSAGE-QUEUE",                       "status": "healthy",  "team": "Platform",    "sla": "99.9%",  "incidents_30d": 1},
    {"id": "data-pipeline",        "label": "DATA-PIPELINE-SERVICE",                     "status": "warning",  "team": "Data",        "sla": "99.0%",  "incidents_30d": 3},

    # SPIEQ cluster (Spectrum Portfolio Mgmt - Equities)
    {"id": "spieq-ui-service",       "label": "SPIEQ-UI-SERVICE",               "status": "healthy",  "team": "SPIEQ Platform",   "sla": "99.9%",  "incidents_30d": 1},
    {"id": "spieq-api-gateway",      "label": "SPIEQ-API-GATEWAY",              "status": "warning",  "team": "SPIEQ Platform",   "sla": "99.99%", "incidents_30d": 4},
    {"id": "spieq-trade-service",    "label": "SPIEQ-TRADE-SERVICE",            "status": "critical", "team": "SPIEQ Trading",    "sla": "99.9%",  "incidents_30d": 6},
    {"id": "spieq-portfolio-svc",    "label": "SPIEQ-PORTFOLIO-SERVICE",         "status": "healthy",  "team": "SPIEQ Trading",    "sla": "99.5%",  "incidents_30d": 1},
    {"id": "spieq-pricing-engine",   "label": "SPIEQ-PRICING-ENGINE",           "status": "warning",  "team": "SPIEQ Quant",      "sla": "99.9%",  "incidents_30d": 3},
    {"id": "spieq-risk-service",     "label": "SPIEQ-RISK-SERVICE",             "status": "critical", "team": "SPIEQ Risk",       "sla": "99.99%", "incidents_30d": 5},
    {"id": "spieq-order-router",     "label": "SPIEQ-ORDER-ROUTER",             "status": "healthy",  "team": "SPIEQ Trading",    "sla": "99.9%",  "incidents_30d": 1},
    {"id": "spieq-market-data",      "label": "SPIEQ-MARKET-DATA-FEED",         "status": "warning",  "team": "SPIEQ Quant",      "sla": "99.9%",  "incidents_30d": 3},
    {"id": "spieq-compliance-svc",   "label": "SPIEQ-COMPLIANCE-SERVICE",       "status": "healthy",  "team": "SPIEQ Compliance", "sla": "99.5%",  "incidents_30d": 0},
    {"id": "spieq-settlement-svc",   "label": "SPIEQ-SETTLEMENT-SERVICE",       "status": "warning",  "team": "SPIEQ Settlement", "sla": "99.5%",  "incidents_30d": 2},
    {"id": "spieq-audit-trail",      "label": "SPIEQ-AUDIT-TRAIL",              "status": "healthy",  "team": "SPIEQ Compliance", "sla": "99.0%",  "incidents_30d": 0},
    {"id": "spieq-notif-svc",        "label": "SPIEQ-NOTIFICATION-SERVICE",     "status": "healthy",  "team": "SPIEQ Platform",   "sla": "99.5%",  "incidents_30d": 1},

    # CONNECT cluster (Advisor Connect + Connect OS)
    {"id": "connect-portal",          "label": "CONNECT-PORTAL",                  "status": "healthy",  "team": "Connect Platform",  "sla": "99.9%",  "incidents_30d": 0},
    {"id": "connect-cloud-gw",        "label": "CONNECT-CLOUD-GATEWAY",           "status": "warning",  "team": "Connect Platform",  "sla": "99.99%", "incidents_30d": 1},
    {"id": "connect-profile-svc",     "label": "CONNECT-SERVICE-PROFILE-SERVICE", "status": "warning",  "team": "Connect Identity",  "sla": "99.5%",  "incidents_30d": 2},
    {"id": "connect-auth-svc",        "label": "CONNECT-AUTH-SERVICE",            "status": "healthy",  "team": "Connect Identity",  "sla": "99.99%", "incidents_30d": 0},
    {"id": "connect-notification",    "label": "CONNECT-NOTIFICATION-SERVICE",    "status": "warning",  "team": "Connect Messaging", "sla": "99.5%",  "incidents_30d": 2},
    {"id": "connect-data-sync",       "label": "CONNECT-DATA-SYNC-SERVICE",      "status": "healthy",  "team": "Connect Data",      "sla": "99.0%",  "incidents_30d": 1},
    {"id": "connect-coverage-app",    "label": "CONNECT-COVERAGE-APP",            "status": "critical", "team": "Connect CRM",       "sla": "99.5%",  "incidents_30d": 5},
    {"id": "connect-home-app-na",     "label": "CONNECT-HOME-APP-NA",             "status": "healthy",  "team": "Connect Platform",  "sla": "99.9%",  "incidents_30d": 0},
    {"id": "connect-home-app-apac",   "label": "CONNECT-HOME-APP-APAC",           "status": "warning",  "team": "Connect Platform",  "sla": "99.9%",  "incidents_30d": 2},
    {"id": "connect-home-app-emea",   "label": "CONNECT-HOME-APP-EMEA",           "status": "healthy",  "team": "Connect Platform",  "sla": "99.9%",  "incidents_30d": 1},
    {"id": "connect-team-mgr",        "label": "CONNECT-TEAM-MANAGER",            "status": "healthy",  "team": "Connect HR",        "sla": "99.5%",  "incidents_30d": 0},
    {"id": "connect-search-svc",      "label": "CONNECT-SEARCH-SERVICE",          "status": "healthy",  "team": "Connect Platform",  "sla": "99.0%",  "incidents_30d": 1},
    {"id": "connect-pref-svc",        "label": "CONNECT-PREFERENCES-SERVICE",     "status": "healthy",  "team": "Connect Identity",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "connect-audit-svc",       "label": "CONNECT-AUDIT-SERVICE",           "status": "healthy",  "team": "Connect Compliance", "sla": "99.0%", "incidents_30d": 0},
    {"id": "connect-doc-svc",         "label": "CONNECT-DOCUMENT-SERVICE",        "status": "warning",  "team": "Connect Documents", "sla": "99.5%",  "incidents_30d": 2},
    {"id": "connect-session-svc",     "label": "CONNECT-SESSION-SERVICE",         "status": "healthy",  "team": "Connect Identity",  "sla": "99.9%",  "incidents_30d": 0},
    {"id": "connect-config-svc",      "label": "CONNECT-CONFIG-SERVICE",          "status": "healthy",  "team": "Connect Platform",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "connect-metrics-svc",     "label": "CONNECT-METRICS-COLLECTOR",       "status": "healthy",  "team": "Connect Observability", "sla": "99.0%", "incidents_30d": 0},

    # MORGAN MONEY cluster (16649) - Ultra Simple (3 nodes)
    {"id": "mm-ui",               "label": "MORGAN-MONEY-UI",              "status": "healthy",  "team": "Client Data",       "sla": "99.9%",  "incidents_30d": 0},
    {"id": "mm-api",              "label": "MORGAN-MONEY-API",             "status": "warning",  "team": "Client Data",       "sla": "99.5%",  "incidents_30d": 3},
    {"id": "mm-data-svc",         "label": "MORGAN-MONEY-DATA-SERVICE",    "status": "critical", "team": "Client Data",       "sla": "99.9%",  "incidents_30d": 8},

    # PANDA cluster (35115) - Simple (4 nodes)
    {"id": "panda-gateway",       "label": "PANDA-GATEWAY",               "status": "healthy",  "team": "Client Data",       "sla": "99.9%",  "incidents_30d": 0},
    {"id": "panda-data-svc",      "label": "PANDA-DATA-SERVICE",          "status": "healthy",  "team": "Client Data",       "sla": "99.5%",  "incidents_30d": 1},
    {"id": "panda-cache-svc",     "label": "PANDA-CACHE-SERVICE",         "status": "warning",  "team": "Client Data",       "sla": "99.0%",  "incidents_30d": 2},
    {"id": "panda-export-svc",    "label": "PANDA-EXPORT-SERVICE",        "status": "healthy",  "team": "Client Data",       "sla": "99.0%",  "incidents_30d": 0},

    # QUANTUM cluster (91001) - Medium (7 nodes)
    {"id": "quantum-portal",         "label": "QUANTUM-PORTAL",              "status": "healthy",  "team": "JPMAIM Platform",   "sla": "99.9%",  "incidents_30d": 0},
    {"id": "quantum-api-gw",         "label": "QUANTUM-API-GATEWAY",         "status": "warning",  "team": "JPMAIM Platform",   "sla": "99.99%", "incidents_30d": 3},
    {"id": "quantum-portfolio-svc",  "label": "QUANTUM-PORTFOLIO-SERVICE",   "status": "critical", "team": "JPMAIM Platform",   "sla": "99.9%",  "incidents_30d": 6},
    {"id": "quantum-analytics-svc",  "label": "QUANTUM-ANALYTICS-ENGINE",    "status": "warning",  "team": "JPMAIM Platform",   "sla": "99.5%",  "incidents_30d": 2},
    {"id": "quantum-report-svc",     "label": "QUANTUM-REPORT-SERVICE",      "status": "healthy",  "team": "JPMAIM Platform",   "sla": "99.0%",  "incidents_30d": 0},
    {"id": "quantum-data-lake",      "label": "QUANTUM-DATA-LAKE",           "status": "critical", "team": "JPMAIM Platform",   "sla": "99.9%",  "incidents_30d": 5},
    {"id": "quantum-auth-svc",       "label": "QUANTUM-AUTH-SERVICE",        "status": "healthy",  "team": "JPMAIM Platform",   "sla": "99.99%", "incidents_30d": 0},

    # ORDER DECISION ENGINE cluster (81884) - Medium (8 nodes)
    {"id": "ode-router",          "label": "ODE-ORDER-ROUTER",             "status": "warning",  "team": "Trading",           "sla": "99.9%",  "incidents_30d": 3},
    {"id": "ode-rule-engine",     "label": "ODE-RULE-ENGINE",              "status": "healthy",  "team": "Trading",           "sla": "99.5%",  "incidents_30d": 0},
    {"id": "ode-market-feed",     "label": "ODE-MARKET-DATA-FEED",         "status": "warning",  "team": "Trading",           "sla": "99.9%",  "incidents_30d": 4},
    {"id": "ode-risk-check",      "label": "ODE-RISK-VALIDATION",          "status": "critical", "team": "Trading",           "sla": "99.99%", "incidents_30d": 7},
    {"id": "ode-exec-svc",        "label": "ODE-EXECUTION-SERVICE",        "status": "critical", "team": "Trading",           "sla": "99.9%",  "incidents_30d": 5},
    {"id": "ode-audit-log",       "label": "ODE-AUDIT-LOG",                "status": "healthy",  "team": "Trading",           "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ode-notif-svc",       "label": "ODE-NOTIFICATION-SERVICE",     "status": "healthy",  "team": "Trading",           "sla": "99.5%",  "incidents_30d": 1},
    {"id": "ode-reconcile-svc",   "label": "ODE-RECONCILIATION-SERVICE",   "status": "warning",  "team": "Trading",           "sla": "99.5%",  "incidents_30d": 2},

    # CREDIT CARD PROCESSING ENGINE cluster (45440) - Complex (11 nodes)
    {"id": "ccpe-ingress",        "label": "CCPE-TRANSACTION-INGRESS",     "status": "healthy",  "team": "Cards Platform",    "sla": "99.99%", "incidents_30d": 0},
    {"id": "ccpe-auth-svc",       "label": "CCPE-AUTHORIZATION-SERVICE",   "status": "warning",  "team": "Cards Platform",    "sla": "99.99%", "incidents_30d": 3},
    {"id": "ccpe-fraud-engine",   "label": "CCPE-FRAUD-DETECTION-ENGINE",  "status": "critical", "team": "Cards Platform",    "sla": "99.99%", "incidents_30d": 5},
    {"id": "ccpe-ledger-svc",     "label": "CCPE-LEDGER-SERVICE",          "status": "critical", "team": "Cards Platform",    "sla": "99.99%", "incidents_30d": 4},
    {"id": "ccpe-limit-svc",      "label": "CCPE-CREDIT-LIMIT-SERVICE",    "status": "warning",  "team": "Cards Platform",    "sla": "99.9%",  "incidents_30d": 2},
    {"id": "ccpe-notif-svc",      "label": "CCPE-CUSTOMER-NOTIFICATIONS",  "status": "healthy",  "team": "Cards Platform",    "sla": "99.5%",  "incidents_30d": 0},
    {"id": "ccpe-dispute-svc",    "label": "CCPE-DISPUTE-HANDLER",         "status": "healthy",  "team": "Cards Platform",    "sla": "99.5%",  "incidents_30d": 1},
    {"id": "ccpe-rewards-svc",    "label": "CCPE-REWARDS-PROCESSING",      "status": "healthy",  "team": "Cards Platform",    "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ccpe-settlement-svc", "label": "CCPE-SETTLEMENT-SERVICE",      "status": "warning",  "team": "Cards Platform",    "sla": "99.9%",  "incidents_30d": 2},
    {"id": "ccpe-report-svc",     "label": "CCPE-REPORTING-SERVICE",       "status": "healthy",  "team": "Cards Platform",    "sla": "99.0%",  "incidents_30d": 0},
    {"id": "ccpe-archive-svc",    "label": "CCPE-DATA-ARCHIVAL",           "status": "healthy",  "team": "Cards Platform",    "sla": "99.0%",  "incidents_30d": 0},

    # WEAVE / AWM ENTITLEMENTS cluster (102987) - Complex (12 nodes)
    {"id": "weave-gateway",       "label": "WEAVE-GATEWAY",                "status": "healthy",  "team": "Tech Shared Svc",   "sla": "99.99%", "incidents_30d": 0},
    {"id": "weave-policy-engine", "label": "WEAVE-POLICY-ENGINE",          "status": "critical", "team": "Tech Shared Svc",   "sla": "99.99%", "incidents_30d": 9},
    {"id": "weave-role-svc",      "label": "WEAVE-ROLE-SERVICE",           "status": "warning",  "team": "Tech Shared Svc",   "sla": "99.9%",  "incidents_30d": 3},
    {"id": "weave-user-store",    "label": "WEAVE-USER-DIRECTORY",         "status": "critical", "team": "Tech Shared Svc",   "sla": "99.99%", "incidents_30d": 7},
    {"id": "weave-audit-svc",     "label": "WEAVE-AUDIT-SERVICE",          "status": "healthy",  "team": "Tech Shared Svc",   "sla": "99.0%",  "incidents_30d": 0},
    {"id": "weave-sync-svc",      "label": "WEAVE-IDENTITY-SYNC",         "status": "warning",  "team": "Tech Shared Svc",   "sla": "99.5%",  "incidents_30d": 2},
    {"id": "weave-token-svc",     "label": "WEAVE-TOKEN-SERVICE",          "status": "healthy",  "team": "Tech Shared Svc",   "sla": "99.99%", "incidents_30d": 0},
    {"id": "weave-consent-svc",   "label": "WEAVE-CONSENT-SERVICE",        "status": "healthy",  "team": "Tech Shared Svc",   "sla": "99.5%",  "incidents_30d": 0},
    {"id": "weave-admin-portal",  "label": "WEAVE-ADMIN-PORTAL",           "status": "healthy",  "team": "Tech Shared Svc",   "sla": "99.9%",  "incidents_30d": 1},
    {"id": "weave-report-svc",    "label": "WEAVE-COMPLIANCE-REPORTS",     "status": "warning",  "team": "Tech Shared Svc",   "sla": "99.0%",  "incidents_30d": 2},
    {"id": "weave-cache-layer",   "label": "WEAVE-DISTRIBUTED-CACHE",      "status": "healthy",  "team": "Tech Shared Svc",   "sla": "99.9%",  "incidents_30d": 0},
    {"id": "weave-event-bus",     "label": "WEAVE-EVENT-BUS",              "status": "critical", "team": "Tech Shared Svc",   "sla": "99.9%",  "incidents_30d": 4},

    # REAL-TIME PAYMENTS GATEWAY cluster (62100) - Very Complex (15 nodes)
    {"id": "rtpg-ingress-lb",     "label": "RTPG-INGRESS-LB",             "status": "healthy",  "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 0},
    {"id": "rtpg-api-gw",         "label": "RTPG-API-GATEWAY",            "status": "warning",  "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 3},
    {"id": "rtpg-validation-svc", "label": "RTPG-VALIDATION-SERVICE",     "status": "healthy",  "team": "Payments Core",     "sla": "99.9%",  "incidents_30d": 1},
    {"id": "rtpg-routing-engine", "label": "RTPG-ROUTING-ENGINE",         "status": "critical", "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 6},
    {"id": "rtpg-sanctions-svc",  "label": "RTPG-SANCTIONS-SCREENING",    "status": "warning",  "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 2},
    {"id": "rtpg-aml-svc",        "label": "RTPG-AML-CHECK-SERVICE",      "status": "healthy",  "team": "Payments Core",     "sla": "99.9%",  "incidents_30d": 0},
    {"id": "rtpg-fx-converter",   "label": "RTPG-FX-CONVERTER",           "status": "warning",  "team": "Payments Core",     "sla": "99.9%",  "incidents_30d": 3},
    {"id": "rtpg-clearing-svc",   "label": "RTPG-CLEARING-ENGINE",        "status": "critical", "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 5},
    {"id": "rtpg-settlement-svc", "label": "RTPG-SETTLEMENT-ENGINE",      "status": "critical", "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 4},
    {"id": "rtpg-ledger-svc",     "label": "RTPG-CORE-LEDGER",            "status": "warning",  "team": "Payments Core",     "sla": "99.99%", "incidents_30d": 2},
    {"id": "rtpg-notif-svc",      "label": "RTPG-NOTIFICATION-DISPATCH",  "status": "healthy",  "team": "Payments Core",     "sla": "99.5%",  "incidents_30d": 0},
    {"id": "rtpg-audit-svc",      "label": "RTPG-AUDIT-TRAIL",            "status": "healthy",  "team": "Payments Core",     "sla": "99.0%",  "incidents_30d": 0},
    {"id": "rtpg-recon-svc",      "label": "RTPG-RECONCILIATION",         "status": "healthy",  "team": "Payments Core",     "sla": "99.5%",  "incidents_30d": 1},
    {"id": "rtpg-archive-svc",    "label": "RTPG-DATA-ARCHIVAL",          "status": "healthy",  "team": "Payments Core",     "sla": "99.0%",  "incidents_30d": 0},
    {"id": "rtpg-monitor-svc",    "label": "RTPG-HEALTH-MONITOR",         "status": "warning",  "team": "Payments Core",     "sla": "99.9%",  "incidents_30d": 2},

    # DIGITAL CHANNELS PLATFORM cluster (77777) - Sparse graph (14 nodes, mostly disconnected)
    # Simulates live data where dependency edges are not yet mapped
    {"id": "dcp-web-portal",       "label": "DCP-WEB-PORTAL",              "status": "healthy",  "team": "Digital Channels",  "sla": "99.9%",  "incidents_30d": 0},
    {"id": "dcp-api-gateway",      "label": "DCP-API-GATEWAY",             "status": "warning",  "team": "Digital Channels",  "sla": "99.99%", "incidents_30d": 2},
    {"id": "dcp-auth-svc",         "label": "DCP-AUTH-SERVICE",            "status": "healthy",  "team": "Digital Channels",  "sla": "99.99%", "incidents_30d": 0},
    {"id": "dcp-content-svc",      "label": "DCP-CONTENT-SERVICE",         "status": "healthy",  "team": "Digital Channels",  "sla": "99.5%",  "incidents_30d": 1},
    {"id": "dcp-search-svc",       "label": "DCP-SEARCH-SERVICE",          "status": "healthy",  "team": "Digital Channels",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "dcp-notification-svc", "label": "DCP-NOTIFICATION-SERVICE",    "status": "warning",  "team": "Digital Channels",  "sla": "99.5%",  "incidents_30d": 3},
    {"id": "dcp-analytics-svc",    "label": "DCP-ANALYTICS-ENGINE",        "status": "healthy",  "team": "Digital Channels",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "dcp-media-svc",        "label": "DCP-MEDIA-SERVICE",           "status": "healthy",  "team": "Digital Channels",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "dcp-config-svc",       "label": "DCP-CONFIG-SERVICE",          "status": "healthy",  "team": "Digital Channels",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "dcp-cache-svc",        "label": "DCP-CACHE-SERVICE",           "status": "healthy",  "team": "Digital Channels",  "sla": "99.9%",  "incidents_30d": 0},
    {"id": "dcp-session-svc",      "label": "DCP-SESSION-SERVICE",         "status": "healthy",  "team": "Digital Channels",  "sla": "99.9%",  "incidents_30d": 0},
    {"id": "dcp-preference-svc",   "label": "DCP-PREFERENCE-SERVICE",      "status": "healthy",  "team": "Digital Channels",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "dcp-audit-svc",        "label": "DCP-AUDIT-SERVICE",           "status": "healthy",  "team": "Digital Channels",  "sla": "99.0%",  "incidents_30d": 0},
    {"id": "dcp-mobile-bff",       "label": "DCP-MOBILE-BFF",              "status": "critical", "team": "Digital Channels",  "sla": "99.9%",  "incidents_30d": 4},
]

# ── Health Indicator Types ────────────────────────────────────────────────────
INDICATOR_TYPES = [
    "Process Group",
    "Service",
    "Synthetic",
]

COMPONENT_INDICATOR_MAP = {
    # Synthetic - UI services, portals, frontends (synthetic monitors)
    "connect-portal": "Synthetic", "spieq-ui-service": "Synthetic",
    "mm-ui": "Synthetic", "quantum-portal": "Synthetic",
    "weave-admin-portal": "Synthetic", "connect-home-app-na": "Synthetic",
    "connect-home-app-apac": "Synthetic", "connect-home-app-emea": "Synthetic",
    # Service - API gateways, query/order services
    "api-gateway": "Service", "spieq-api-gateway": "Service", "connect-cloud-gw": "Service",
    "panda-gateway": "Service", "quantum-api-gw": "Service", "rtpg-api-gw": "Service",
    "ode-router": "Service", "rtpg-ingress-lb": "Service", "ccpe-ingress": "Service",
    "weave-gateway": "Service", "meridian-query": "Service", "meridian-order": "Service",
    "sb-service-order": "Service", "sb-service-query": "Service", "mm-api": "Service",
    # Process Group - databases, caches, queues, data stores
    "db-primary": "Process Group", "db-replica": "Process Group",
    "cache-layer": "Process Group", "message-queue": "Process Group",
    "quantum-data-lake": "Process Group", "weave-cache-layer": "Process Group",
    "weave-event-bus": "Process Group", "rtpg-archive-svc": "Process Group",
    "ccpe-archive-svc": "Process Group", "panda-cache-svc": "Process Group",
    # Service - auth, fraud, validation, risk, compliance
    "auth-service": "Service", "connect-auth-svc": "Service",
    "ccpe-auth-svc": "Service", "ccpe-fraud-engine": "Service",
    "spieq-risk-service": "Service", "ode-risk-check": "Service",
    "rtpg-validation-svc": "Service", "rtpg-sanctions-svc": "Service",
    "rtpg-aml-svc": "Service", "weave-policy-engine": "Service",
    "weave-token-svc": "Service", "quantum-auth-svc": "Service",
    "ipbol-manager-auth": "Service", "spieq-compliance-svc": "Service",
    "weave-consent-svc": "Service",
    # Service - trade execution, routing, payments, settlement, clearing
    "spieq-trade-service": "Service", "payment-gateway": "Service",
    "ode-exec-svc": "Service", "rtpg-routing-engine": "Service",
    "rtpg-clearing-svc": "Service", "rtpg-settlement-svc": "Service",
    "ccpe-ledger-svc": "Service", "ccpe-settlement-svc": "Service",
    "ccpe-limit-svc": "Service", "ccpe-rewards-svc": "Service",
    "ccpe-dispute-svc": "Service", "spieq-settlement-svc": "Service",
    "spieq-order-router": "Service", "spieq-pricing-engine": "Service",
    "rtpg-ledger-svc": "Service", "rtpg-fx-converter": "Service",
    "mm-data-svc": "Service", "quantum-portfolio-svc": "Service",
    # Process Group - data sync, pipelines, profiles, integrations
    "data-pipeline": "Process Group", "connect-data-sync": "Process Group",
    "connect-profile-svc": "Service", "ipbol-account": "Service",
    "ipbol-account-green": "Service", "ipbol-doc-domain": "Service",
    "ipbol-doc-domain-g": "Service", "ipbol-doc-delivery": "Service",
    "ipbol-contact-sync": "Process Group", "ipbol-investments": "Process Group",
    "connect-coverage-app": "Process Group", "active-advisory": "Service",
    "spieq-market-data": "Process Group", "ode-market-feed": "Process Group",
    "spieq-portfolio-svc": "Synthetic", "panda-data-svc": "Process Group",
    "panda-export-svc": "Process Group", "quantum-analytics-svc": "Service",
    "weave-role-svc": "Service", "weave-user-store": "Process Group",
    "weave-sync-svc": "Process Group", "connect-team-mgr": "Service",
    "connect-search-svc": "Service", "connect-pref-svc": "Process Group",
    "connect-session-svc": "Service", "connect-config-svc": "Process Group",
    "connect-doc-svc": "Service", "ode-rule-engine": "Service",
    "ode-reconcile-svc": "Service", "rtpg-recon-svc": "Service",
    # Process Group - audit, notification, reporting, monitoring
    "email-notification": "Process Group", "spieq-audit-trail": "Process Group",
    "spieq-notif-svc": "Service", "connect-notification": "Service",
    "connect-audit-svc": "Synthetic", "connect-metrics-svc": "Process Group",
    "ode-audit-log": "Process Group", "ode-notif-svc": "Service",
    "ccpe-notif-svc": "Service", "ccpe-report-svc": "Service",
    "weave-audit-svc": "Process Group", "weave-report-svc": "Service",
    "quantum-report-svc": "Service", "rtpg-notif-svc": "Service",
    "rtpg-audit-svc": "Process Group", "rtpg-monitor-svc": "Process Group",
    # Digital Channels Platform
    "dcp-web-portal": "Synthetic", "dcp-api-gateway": "Service",
    "dcp-auth-svc": "Service", "dcp-mobile-bff": "Service",
}


# (source, target) means source DEPENDS ON target
EDGES_RAW = [
    # Core platform edges
    ("api-gateway",       "meridian-query"),
    ("api-gateway",       "meridian-order"),
    ("api-gateway",       "payment-gateway"),
    ("api-gateway",       "auth-service"),
    ("meridian-query",    "sb-service-order"),
    ("meridian-query",    "sb-service-query"),
    ("meridian-query",    "active-advisory"),
    ("meridian-query",    "ipbol-account"),
    ("meridian-query",    "ipbol-account-green"),
    ("meridian-query",    "ipbol-contact-sync"),
    ("meridian-query",    "ipbol-doc-delivery"),
    ("meridian-query",    "ipbol-doc-domain"),
    ("meridian-query",    "ipbol-doc-domain-g"),
    ("meridian-query",    "ipbol-investments"),
    ("meridian-query",    "ipbol-manager-auth"),
    ("meridian-query",    "auth-service"),
    ("meridian-query",    "cache-layer"),
    ("meridian-order",    "sb-service-order"),
    ("meridian-order",    "auth-service"),
    ("meridian-order",    "payment-gateway"),
    ("meridian-order",    "email-notification"),
    ("meridian-order",    "message-queue"),
    ("payment-gateway",   "db-primary"),
    ("payment-gateway",   "cache-layer"),
    ("payment-gateway",   "email-notification"),
    ("ipbol-account",     "db-primary"),
    ("ipbol-investments", "db-primary"),
    ("ipbol-doc-domain",  "db-primary"),
    ("email-notification","message-queue"),
    ("data-pipeline",     "db-replica"),
    ("data-pipeline",     "message-queue"),

    # SPIEQ cluster
    ("spieq-ui-service",       "spieq-api-gateway"),
    ("spieq-api-gateway",      "spieq-trade-service"),
    ("spieq-api-gateway",      "spieq-portfolio-svc"),
    ("spieq-api-gateway",      "spieq-pricing-engine"),
    ("spieq-api-gateway",      "auth-service"),
    ("spieq-api-gateway",      "spieq-compliance-svc"),
    ("spieq-api-gateway",      "spieq-market-data"),
    ("spieq-trade-service",    "spieq-risk-service"),
    ("spieq-trade-service",    "spieq-pricing-engine"),
    ("spieq-trade-service",    "db-primary"),
    ("spieq-trade-service",    "message-queue"),
    ("spieq-trade-service",    "spieq-order-router"),
    ("spieq-trade-service",    "spieq-settlement-svc"),
    ("spieq-trade-service",    "spieq-audit-trail"),
    ("spieq-pricing-engine",   "cache-layer"),
    ("spieq-pricing-engine",   "spieq-market-data"),
    ("spieq-portfolio-svc",    "db-primary"),
    ("spieq-portfolio-svc",    "cache-layer"),
    ("spieq-risk-service",     "db-primary"),
    ("spieq-risk-service",     "cache-layer"),
    ("spieq-risk-service",     "spieq-market-data"),
    ("spieq-order-router",     "message-queue"),
    ("spieq-order-router",     "spieq-risk-service"),
    ("spieq-market-data",      "cache-layer"),
    ("spieq-market-data",      "db-replica"),
    ("spieq-compliance-svc",   "db-primary"),
    ("spieq-compliance-svc",   "spieq-audit-trail"),
    ("spieq-settlement-svc",   "db-primary"),
    ("spieq-settlement-svc",   "message-queue"),
    ("spieq-audit-trail",      "db-replica"),
    ("spieq-notif-svc",        "message-queue"),

    # CONNECT cluster - Advisor Connect (connect-profile-svc) dependencies
    ("connect-profile-svc",    "db-primary"),
    ("connect-profile-svc",    "connect-data-sync"),
    ("connect-profile-svc",    "connect-coverage-app"),
    ("connect-profile-svc",    "cache-layer"),
    ("connect-profile-svc",    "connect-pref-svc"),
    ("connect-profile-svc",    "connect-audit-svc"),
    ("connect-profile-svc",    "connect-notification"),
    ("connect-coverage-app",   "db-primary"),
    ("connect-coverage-app",   "connect-notification"),
    ("connect-coverage-app",   "cache-layer"),
    ("connect-coverage-app",   "connect-doc-svc"),
    ("connect-pref-svc",       "db-replica"),
    ("connect-pref-svc",       "cache-layer"),
    ("connect-audit-svc",      "db-replica"),
    ("connect-audit-svc",      "message-queue"),
    ("connect-doc-svc",        "db-primary"),
    ("connect-doc-svc",        "connect-data-sync"),
    ("connect-data-sync",      "db-replica"),
    ("connect-notification",   "message-queue"),

    # CONNECT cluster - Connect OS (connect-cloud-gw) dependencies
    ("connect-portal",           "connect-cloud-gw"),
    ("connect-cloud-gw",         "connect-profile-svc"),
    ("connect-cloud-gw",         "connect-auth-svc"),
    ("connect-cloud-gw",         "connect-notification"),
    ("connect-cloud-gw",         "connect-home-app-na"),
    ("connect-cloud-gw",         "connect-home-app-apac"),
    ("connect-cloud-gw",         "connect-home-app-emea"),
    ("connect-cloud-gw",         "connect-team-mgr"),
    ("connect-cloud-gw",         "connect-search-svc"),
    ("connect-cloud-gw",         "connect-doc-svc"),
    ("connect-cloud-gw",         "connect-session-svc"),
    ("connect-cloud-gw",         "connect-config-svc"),
    ("connect-cloud-gw",         "connect-metrics-svc"),
    ("connect-home-app-na",      "connect-profile-svc"),
    ("connect-home-app-na",      "connect-auth-svc"),
    ("connect-home-app-apac",    "connect-profile-svc"),
    ("connect-home-app-apac",    "connect-auth-svc"),
    ("connect-home-app-emea",    "connect-profile-svc"),
    ("connect-home-app-emea",    "connect-auth-svc"),
    ("connect-team-mgr",         "db-primary"),
    ("connect-team-mgr",         "connect-auth-svc"),
    ("connect-search-svc",       "cache-layer"),
    ("connect-search-svc",       "db-replica"),
    ("connect-auth-svc",         "cache-layer"),
    ("connect-session-svc",      "cache-layer"),
    ("connect-config-svc",       "db-replica"),
    ("connect-metrics-svc",      "message-queue"),

    # Additional edges for Blast Radius Layers internal connectivity
    ("active-advisory",          "connect-profile-svc"),
    ("connect-coverage-app",     "ipbol-account"),
    ("ipbol-account",            "ipbol-doc-domain"),

    # Cross-app downstream from Advisor Connect (90176)
    ("connect-coverage-app",     "spieq-portfolio-svc"),
    ("connect-data-sync",        "quantum-data-lake"),
    ("ipbol-account",            "ccpe-ledger-svc"),
    ("spieq-settlement-svc",     "spieq-notif-svc"),
    ("spieq-api-gateway",        "payment-gateway"),
    ("payment-gateway",          "spieq-notif-svc"),

    # MORGAN MONEY cluster (16649) - Ultra Simple
    ("mm-ui",              "mm-api"),
    ("mm-api",             "mm-data-svc"),

    # PANDA cluster (35115) - Simple
    ("panda-gateway",      "panda-data-svc"),
    ("panda-gateway",      "panda-cache-svc"),
    ("panda-data-svc",     "panda-cache-svc"),
    ("panda-data-svc",     "panda-export-svc"),

    # QUANTUM cluster (91001) - Medium
    ("quantum-portal",          "quantum-api-gw"),
    ("quantum-api-gw",          "quantum-portfolio-svc"),
    ("quantum-api-gw",          "quantum-analytics-svc"),
    ("quantum-api-gw",          "quantum-auth-svc"),
    ("quantum-portfolio-svc",   "quantum-data-lake"),
    ("quantum-analytics-svc",   "quantum-data-lake"),
    ("quantum-analytics-svc",   "quantum-report-svc"),
    ("quantum-report-svc",      "quantum-data-lake"),

    # ORDER DECISION ENGINE cluster (81884) - Medium
    ("ode-router",          "ode-rule-engine"),
    ("ode-router",          "ode-risk-check"),
    ("ode-router",          "ode-market-feed"),
    ("ode-rule-engine",     "ode-exec-svc"),
    ("ode-risk-check",      "ode-market-feed"),
    ("ode-risk-check",      "ode-exec-svc"),
    ("ode-exec-svc",        "ode-audit-log"),
    ("ode-exec-svc",        "ode-notif-svc"),
    ("ode-exec-svc",        "ode-reconcile-svc"),
    ("ode-reconcile-svc",   "ode-audit-log"),

    # CREDIT CARD PROCESSING ENGINE cluster (45440) - Complex
    ("ccpe-ingress",         "ccpe-auth-svc"),
    ("ccpe-auth-svc",        "ccpe-fraud-engine"),
    ("ccpe-auth-svc",        "ccpe-limit-svc"),
    ("ccpe-fraud-engine",    "ccpe-ledger-svc"),
    ("ccpe-limit-svc",       "ccpe-ledger-svc"),
    ("ccpe-ledger-svc",      "ccpe-settlement-svc"),
    ("ccpe-ledger-svc",      "ccpe-rewards-svc"),
    ("ccpe-ledger-svc",      "ccpe-notif-svc"),
    ("ccpe-settlement-svc",  "ccpe-report-svc"),
    ("ccpe-settlement-svc",  "ccpe-archive-svc"),
    ("ccpe-dispute-svc",     "ccpe-ledger-svc"),
    ("ccpe-dispute-svc",     "ccpe-notif-svc"),
    ("ccpe-report-svc",      "ccpe-archive-svc"),

    # WEAVE / AWM ENTITLEMENTS cluster (102987) - Complex
    ("weave-admin-portal",   "weave-gateway"),
    ("weave-gateway",        "weave-policy-engine"),
    ("weave-gateway",        "weave-token-svc"),
    ("weave-gateway",        "weave-audit-svc"),
    ("weave-policy-engine",  "weave-role-svc"),
    ("weave-policy-engine",  "weave-user-store"),
    ("weave-policy-engine",  "weave-cache-layer"),
    ("weave-role-svc",       "weave-user-store"),
    ("weave-role-svc",       "weave-cache-layer"),
    ("weave-user-store",     "weave-sync-svc"),
    ("weave-sync-svc",       "weave-event-bus"),
    ("weave-token-svc",      "weave-cache-layer"),
    ("weave-token-svc",      "weave-user-store"),
    ("weave-consent-svc",    "weave-user-store"),
    ("weave-consent-svc",    "weave-audit-svc"),
    ("weave-report-svc",     "weave-audit-svc"),
    ("weave-report-svc",     "weave-role-svc"),
    ("weave-event-bus",      "weave-audit-svc"),

    # REAL-TIME PAYMENTS GATEWAY cluster (62100) - Very Complex
    ("rtpg-ingress-lb",      "rtpg-api-gw"),
    ("rtpg-api-gw",          "rtpg-validation-svc"),
    ("rtpg-api-gw",          "rtpg-audit-svc"),
    ("rtpg-api-gw",          "rtpg-monitor-svc"),
    ("rtpg-validation-svc",  "rtpg-routing-engine"),
    ("rtpg-routing-engine",  "rtpg-sanctions-svc"),
    ("rtpg-routing-engine",  "rtpg-aml-svc"),
    ("rtpg-routing-engine",  "rtpg-fx-converter"),
    ("rtpg-routing-engine",  "rtpg-clearing-svc"),
    ("rtpg-sanctions-svc",   "rtpg-clearing-svc"),
    ("rtpg-aml-svc",         "rtpg-clearing-svc"),
    ("rtpg-clearing-svc",    "rtpg-settlement-svc"),
    ("rtpg-settlement-svc",  "rtpg-ledger-svc"),
    ("rtpg-settlement-svc",  "rtpg-notif-svc"),
    ("rtpg-settlement-svc",  "rtpg-recon-svc"),
    ("rtpg-recon-svc",       "rtpg-ledger-svc"),
    ("rtpg-recon-svc",       "rtpg-archive-svc"),
    ("rtpg-ledger-svc",      "rtpg-audit-svc"),
    ("rtpg-monitor-svc",     "rtpg-audit-svc"),

    # Digital Channels Platform (77777) — sparse: only 2 edges, 11 orphan nodes
    ("dcp-web-portal",       "dcp-api-gateway"),
    ("dcp-api-gateway",      "dcp-auth-svc"),
]

# ── Blast Radius Layers - mock data ──────────────────────────────────────────

SEAL_COMPONENTS = {
    # Simple graph (6 components)
    "88180": [
        "connect-portal", "connect-cloud-gw", "connect-auth-svc",
        "connect-home-app-na", "connect-home-app-apac", "connect-home-app-emea",
    ],
    # Medium graph (10 components)
    "90176": [
        "connect-profile-svc", "connect-coverage-app", "connect-notification",
        "connect-data-sync", "connect-doc-svc", "connect-pref-svc",
        "connect-audit-svc", "active-advisory", "ipbol-account", "ipbol-doc-domain",
    ],
    # Complex graph (14 components)
    "90215": [
        "spieq-ui-service", "spieq-api-gateway", "spieq-trade-service",
        "spieq-portfolio-svc", "spieq-pricing-engine", "spieq-risk-service",
        "spieq-order-router", "spieq-market-data", "spieq-compliance-svc",
        "spieq-settlement-svc", "spieq-audit-trail", "spieq-notif-svc",
        "payment-gateway", "email-notification",
    ],
    # Ultra Simple (3 components)
    "16649": ["mm-ui", "mm-api", "mm-data-svc"],
    # Simple (4 components)
    "35115": ["panda-gateway", "panda-data-svc", "panda-cache-svc", "panda-export-svc"],
    # Medium (7 components)
    "91001": [
        "quantum-portal", "quantum-api-gw", "quantum-portfolio-svc",
        "quantum-analytics-svc", "quantum-report-svc", "quantum-data-lake",
        "quantum-auth-svc",
    ],
    # Medium (8 components)
    "81884": [
        "ode-router", "ode-rule-engine", "ode-market-feed", "ode-risk-check",
        "ode-exec-svc", "ode-audit-log", "ode-notif-svc", "ode-reconcile-svc",
    ],
    # Complex (11 components)
    "45440": [
        "ccpe-ingress", "ccpe-auth-svc", "ccpe-fraud-engine", "ccpe-ledger-svc",
        "ccpe-limit-svc", "ccpe-notif-svc", "ccpe-dispute-svc", "ccpe-rewards-svc",
        "ccpe-settlement-svc", "ccpe-report-svc", "ccpe-archive-svc",
    ],
    # Complex (12 components)
    "102987": [
        "weave-gateway", "weave-policy-engine", "weave-role-svc", "weave-user-store",
        "weave-audit-svc", "weave-sync-svc", "weave-token-svc", "weave-consent-svc",
        "weave-admin-portal", "weave-report-svc", "weave-cache-layer", "weave-event-bus",
    ],
    # Very Complex (15 components)
    "62100": [
        "rtpg-ingress-lb", "rtpg-api-gw", "rtpg-validation-svc", "rtpg-routing-engine",
        "rtpg-sanctions-svc", "rtpg-aml-svc", "rtpg-fx-converter", "rtpg-clearing-svc",
        "rtpg-settlement-svc", "rtpg-ledger-svc", "rtpg-notif-svc", "rtpg-audit-svc",
        "rtpg-recon-svc", "rtpg-archive-svc", "rtpg-monitor-svc",
    ],
    # Sparse graph — 14 components, only 3 connected (simulates partial live data)
    "77777": [
        "dcp-web-portal", "dcp-api-gateway", "dcp-auth-svc", "dcp-content-svc",
        "dcp-search-svc", "dcp-notification-svc", "dcp-analytics-svc", "dcp-media-svc",
        "dcp-config-svc", "dcp-cache-svc", "dcp-session-svc", "dcp-preference-svc",
        "dcp-audit-svc", "dcp-mobile-bff",
    ],
}

INDICATOR_NODES = [
    # ── Connect OS (88180) - 8 indicators across 6 components ──
    {"id": "dt-pg-cloud-gw",       "label": "connect-cloud-gateway",  "indicator_type": "Process Group", "health": "amber", "component": "connect-cloud-gw"},
    {"id": "dt-pg-portal",         "label": "connect-portal",         "indicator_type": "Process Group", "health": "green", "component": "connect-portal"},
    {"id": "dt-svc-auth",          "label": "AuthenticationSvc",      "indicator_type": "Service",       "health": "green", "component": "connect-auth-svc"},
    {"id": "dt-syn-login",         "label": "Login Flow",             "indicator_type": "Synthetic",     "health": "green", "component": "connect-auth-svc"},
    {"id": "dt-syn-home-na",       "label": "Home Page NA",           "indicator_type": "Synthetic",     "health": "green", "component": "connect-home-app-na"},
    {"id": "dt-svc-home-apac",     "label": "HomeApp-APAC",           "indicator_type": "Service",       "health": "amber", "component": "connect-home-app-apac"},
    {"id": "dt-syn-home-apac",     "label": "Home Page APAC",         "indicator_type": "Synthetic",     "health": "amber", "component": "connect-home-app-apac"},
    {"id": "dt-svc-home-emea",     "label": "HomeApp-EMEA",           "indicator_type": "Service",       "health": "green", "component": "connect-home-app-emea"},

    # ── Advisor Connect (90176) - 14 indicators across 10 components ──
    {"id": "dt-pg-profile-svc",    "label": "connect-profile-svc",    "indicator_type": "Process Group", "health": "amber", "component": "connect-profile-svc"},
    {"id": "dt-svc-profile",       "label": "ProfileService",         "indicator_type": "Service",       "health": "amber", "component": "connect-profile-svc"},
    {"id": "dt-pg-coverage-app",   "label": "connect-coverage-app",   "indicator_type": "Process Group", "health": "red",   "component": "connect-coverage-app"},
    {"id": "dt-syn-coverage",      "label": "Coverage Lookup",        "indicator_type": "Synthetic",     "health": "amber", "component": "connect-coverage-app"},
    {"id": "dt-svc-notification",  "label": "NotificationSvc",        "indicator_type": "Service",       "health": "amber", "component": "connect-notification"},
    {"id": "dt-pg-data-sync",      "label": "connect-data-sync",      "indicator_type": "Process Group", "health": "green", "component": "connect-data-sync"},
    {"id": "dt-svc-doc-svc",       "label": "DocumentService",        "indicator_type": "Service",       "health": "amber", "component": "connect-doc-svc"},
    {"id": "dt-pg-pref-svc",       "label": "connect-pref-svc",       "indicator_type": "Process Group", "health": "green", "component": "connect-pref-svc"},
    {"id": "dt-syn-audit-trail",   "label": "Audit Trail",            "indicator_type": "Synthetic",     "health": "green", "component": "connect-audit-svc"},
    {"id": "dt-svc-advisory",      "label": "ActiveAdvisorySvc",      "indicator_type": "Service",       "health": "green", "component": "active-advisory"},
    {"id": "dt-pg-ipbol-acct",     "label": "ipbol-account",          "indicator_type": "Process Group", "health": "red",   "component": "ipbol-account"},
    {"id": "dt-syn-ipbol-acct",    "label": "Account Lookup",         "indicator_type": "Synthetic",     "health": "red",   "component": "ipbol-account"},
    {"id": "dt-svc-doc-domain",    "label": "DocDomainSvc",           "indicator_type": "Service",       "health": "red",   "component": "ipbol-doc-domain"},
    {"id": "dt-pg-doc-domain",     "label": "ipbol-doc-domain",       "indicator_type": "Process Group", "health": "red",   "component": "ipbol-doc-domain"},

    # ── Spectrum Portfolio Mgmt (90215) - 22 indicators across 14 components ──
    {"id": "dt-syn-ui-health",     "label": "UI Health Check",        "indicator_type": "Synthetic",     "health": "green", "component": "spieq-ui-service"},
    {"id": "dt-svc-api-gw",        "label": "APIGatewaySvc",          "indicator_type": "Service",       "health": "amber", "component": "spieq-api-gateway"},
    {"id": "dt-pg-api-gw",         "label": "spieq-api-gateway",      "indicator_type": "Process Group", "health": "amber", "component": "spieq-api-gateway"},
    {"id": "dt-pg-trade-svc",      "label": "spieq-trade-service",    "indicator_type": "Process Group", "health": "red",   "component": "spieq-trade-service"},
    {"id": "dt-svc-trade",         "label": "TradeExecutionSvc",      "indicator_type": "Service",       "health": "red",   "component": "spieq-trade-service"},
    {"id": "dt-syn-trade-submit",  "label": "Trade Submission",       "indicator_type": "Synthetic",     "health": "red",   "component": "spieq-trade-service"},
    {"id": "dt-syn-portfolio",     "label": "Portfolio View",         "indicator_type": "Synthetic",     "health": "green", "component": "spieq-portfolio-svc"},
    {"id": "dt-pg-pricing",        "label": "spieq-pricing-engine",   "indicator_type": "Process Group", "health": "amber", "component": "spieq-pricing-engine"},
    {"id": "dt-svc-pricing",       "label": "PricingEngineSvc",       "indicator_type": "Service",       "health": "amber", "component": "spieq-pricing-engine"},
    {"id": "dt-pg-risk-svc",       "label": "spieq-risk-service",     "indicator_type": "Process Group", "health": "red",   "component": "spieq-risk-service"},
    {"id": "dt-svc-risk",          "label": "RiskAssessmentSvc",      "indicator_type": "Service",       "health": "red",   "component": "spieq-risk-service"},
    {"id": "dt-svc-order-router",  "label": "OrderRouterSvc",         "indicator_type": "Service",       "health": "green", "component": "spieq-order-router"},
    {"id": "dt-pg-market-data",    "label": "MarketDataFeed",         "indicator_type": "Process Group", "health": "amber", "component": "spieq-market-data"},
    {"id": "dt-syn-compliance",    "label": "Compliance Check",       "indicator_type": "Synthetic",     "health": "green", "component": "spieq-compliance-svc"},
    {"id": "dt-svc-settlement",    "label": "SettlementSvc",          "indicator_type": "Service",       "health": "amber", "component": "spieq-settlement-svc"},
    {"id": "dt-pg-audit-trail",    "label": "spieq-audit-trail",      "indicator_type": "Process Group", "health": "green", "component": "spieq-audit-trail"},
    {"id": "dt-svc-notif",         "label": "NotificationSvc",        "indicator_type": "Service",       "health": "green", "component": "spieq-notif-svc"},
    {"id": "dt-svc-payment",       "label": "PaymentGatewaySvc",      "indicator_type": "Service",       "health": "red",   "component": "payment-gateway"},
    {"id": "dt-syn-payment",       "label": "Payment Processing",     "indicator_type": "Synthetic",     "health": "red",   "component": "payment-gateway"},
    {"id": "dt-pg-email",          "label": "email-notification",     "indicator_type": "Process Group", "health": "red",   "component": "email-notification"},

    # ── Morgan Money (16649) - 4 indicators across 3 components ──
    {"id": "dt-pg-mm-ui",          "label": "morgan-money-ui",        "indicator_type": "Process Group", "health": "green", "component": "mm-ui"},
    {"id": "dt-svc-mm-api",        "label": "MorganMoneyAPI",         "indicator_type": "Service",       "health": "amber", "component": "mm-api"},
    {"id": "dt-pg-mm-data",        "label": "morgan-money-data",      "indicator_type": "Process Group", "health": "red",   "component": "mm-data-svc"},
    {"id": "dt-syn-mm-data",       "label": "Data Lookup",            "indicator_type": "Synthetic",     "health": "red",   "component": "mm-data-svc"},

    # ── PANDA (35115) - 5 indicators across 4 components ──
    {"id": "dt-pg-panda-gw",       "label": "panda-gateway",          "indicator_type": "Process Group", "health": "green", "component": "panda-gateway"},
    {"id": "dt-svc-panda-data",    "label": "PandaDataSvc",           "indicator_type": "Service",       "health": "green", "component": "panda-data-svc"},
    {"id": "dt-pg-panda-cache",    "label": "panda-cache",            "indicator_type": "Process Group", "health": "amber", "component": "panda-cache-svc"},
    {"id": "dt-syn-panda-cache",   "label": "Cache Hit Rate",         "indicator_type": "Synthetic",     "health": "amber", "component": "panda-cache-svc"},
    {"id": "dt-svc-panda-export",  "label": "PandaExportSvc",         "indicator_type": "Service",       "health": "green", "component": "panda-export-svc"},

    # ── Quantum (91001) - 10 indicators across 7 components ──
    {"id": "dt-syn-quantum-portal",   "label": "Portal Health",          "indicator_type": "Synthetic",     "health": "green", "component": "quantum-portal"},
    {"id": "dt-svc-quantum-api",      "label": "QuantumAPISvc",          "indicator_type": "Service",       "health": "amber", "component": "quantum-api-gw"},
    {"id": "dt-pg-quantum-api",       "label": "quantum-api-gateway",    "indicator_type": "Process Group", "health": "amber", "component": "quantum-api-gw"},
    {"id": "dt-pg-quantum-portfolio", "label": "quantum-portfolio",      "indicator_type": "Process Group", "health": "red",   "component": "quantum-portfolio-svc"},
    {"id": "dt-svc-quantum-portfolio","label": "PortfolioSvc",           "indicator_type": "Service",       "health": "red",   "component": "quantum-portfolio-svc"},
    {"id": "dt-pg-quantum-analytics", "label": "quantum-analytics",      "indicator_type": "Process Group", "health": "amber", "component": "quantum-analytics-svc"},
    {"id": "dt-svc-quantum-report",   "label": "QuantumReportSvc",       "indicator_type": "Service",       "health": "green", "component": "quantum-report-svc"},
    {"id": "dt-pg-quantum-lake",      "label": "quantum-data-lake",      "indicator_type": "Process Group", "health": "red",   "component": "quantum-data-lake"},
    {"id": "dt-syn-quantum-lake",     "label": "Data Lake Query",        "indicator_type": "Synthetic",     "health": "red",   "component": "quantum-data-lake"},
    {"id": "dt-svc-quantum-auth",     "label": "QuantumAuthSvc",         "indicator_type": "Service",       "health": "green", "component": "quantum-auth-svc"},

    # ── Order Decision Engine (81884) - 12 indicators across 8 components ──
    {"id": "dt-pg-ode-router",        "label": "ode-order-router",       "indicator_type": "Process Group", "health": "amber", "component": "ode-router"},
    {"id": "dt-svc-ode-router",       "label": "OrderRouterSvc",         "indicator_type": "Service",       "health": "amber", "component": "ode-router"},
    {"id": "dt-pg-ode-rules",         "label": "ode-rule-engine",        "indicator_type": "Process Group", "health": "green", "component": "ode-rule-engine"},
    {"id": "dt-pg-ode-market",        "label": "ode-market-data",        "indicator_type": "Process Group", "health": "amber", "component": "ode-market-feed"},
    {"id": "dt-syn-ode-market",       "label": "Market Feed Latency",    "indicator_type": "Synthetic",     "health": "amber", "component": "ode-market-feed"},
    {"id": "dt-pg-ode-risk",          "label": "ode-risk-validation",    "indicator_type": "Process Group", "health": "red",   "component": "ode-risk-check"},
    {"id": "dt-svc-ode-risk",         "label": "RiskValidationSvc",      "indicator_type": "Service",       "health": "red",   "component": "ode-risk-check"},
    {"id": "dt-pg-ode-exec",          "label": "ode-execution-svc",      "indicator_type": "Process Group", "health": "red",   "component": "ode-exec-svc"},
    {"id": "dt-syn-ode-exec",         "label": "Order Execution",        "indicator_type": "Synthetic",     "health": "red",   "component": "ode-exec-svc"},
    {"id": "dt-pg-ode-audit",         "label": "ode-audit-log",          "indicator_type": "Process Group", "health": "green", "component": "ode-audit-log"},
    {"id": "dt-svc-ode-notif",        "label": "OdeNotifSvc",            "indicator_type": "Service",       "health": "green", "component": "ode-notif-svc"},
    {"id": "dt-svc-ode-recon",        "label": "ReconciliationSvc",      "indicator_type": "Service",       "health": "amber", "component": "ode-reconcile-svc"},

    # ── Credit Card Processing Engine (45440) - 15 indicators across 11 components ──
    {"id": "dt-pg-ccpe-ingress",      "label": "ccpe-ingress",           "indicator_type": "Process Group", "health": "green", "component": "ccpe-ingress"},
    {"id": "dt-svc-ccpe-auth",        "label": "CCAuthorizationSvc",     "indicator_type": "Service",       "health": "amber", "component": "ccpe-auth-svc"},
    {"id": "dt-syn-ccpe-auth",        "label": "Auth Response Time",     "indicator_type": "Synthetic",     "health": "amber", "component": "ccpe-auth-svc"},
    {"id": "dt-pg-ccpe-fraud",        "label": "ccpe-fraud-engine",      "indicator_type": "Process Group", "health": "red",   "component": "ccpe-fraud-engine"},
    {"id": "dt-svc-ccpe-fraud",       "label": "FraudDetectionSvc",      "indicator_type": "Service",       "health": "red",   "component": "ccpe-fraud-engine"},
    {"id": "dt-pg-ccpe-ledger",       "label": "ccpe-ledger",            "indicator_type": "Process Group", "health": "red",   "component": "ccpe-ledger-svc"},
    {"id": "dt-syn-ccpe-ledger",      "label": "Ledger Posting",         "indicator_type": "Synthetic",     "health": "red",   "component": "ccpe-ledger-svc"},
    {"id": "dt-svc-ccpe-limit",       "label": "CreditLimitSvc",         "indicator_type": "Service",       "health": "amber", "component": "ccpe-limit-svc"},
    {"id": "dt-svc-ccpe-notif",       "label": "CustomerNotifSvc",       "indicator_type": "Service",       "health": "green", "component": "ccpe-notif-svc"},
    {"id": "dt-pg-ccpe-dispute",      "label": "ccpe-dispute",           "indicator_type": "Process Group", "health": "green", "component": "ccpe-dispute-svc"},
    {"id": "dt-svc-ccpe-rewards",     "label": "RewardsSvc",             "indicator_type": "Service",       "health": "green", "component": "ccpe-rewards-svc"},
    {"id": "dt-svc-ccpe-settlement",  "label": "SettlementSvc",          "indicator_type": "Service",       "health": "amber", "component": "ccpe-settlement-svc"},
    {"id": "dt-pg-ccpe-report",       "label": "ccpe-reporting",         "indicator_type": "Process Group", "health": "green", "component": "ccpe-report-svc"},
    {"id": "dt-pg-ccpe-archive",      "label": "ccpe-archive",           "indicator_type": "Process Group", "health": "green", "component": "ccpe-archive-svc"},
    {"id": "dt-syn-ccpe-settlement",  "label": "Settlement Cycle",       "indicator_type": "Synthetic",     "health": "amber", "component": "ccpe-settlement-svc"},

    # ── WEAVE / AWM Entitlements (102987) - 16 indicators across 12 components ──
    {"id": "dt-pg-weave-gw",          "label": "weave-gateway",          "indicator_type": "Process Group", "health": "green", "component": "weave-gateway"},
    {"id": "dt-pg-weave-policy",      "label": "weave-policy-engine",    "indicator_type": "Process Group", "health": "red",   "component": "weave-policy-engine"},
    {"id": "dt-svc-weave-policy",     "label": "PolicyEngineSvc",        "indicator_type": "Service",       "health": "red",   "component": "weave-policy-engine"},
    {"id": "dt-svc-weave-role",       "label": "RoleServiceSvc",         "indicator_type": "Service",       "health": "amber", "component": "weave-role-svc"},
    {"id": "dt-pg-weave-user",        "label": "weave-user-store",       "indicator_type": "Process Group", "health": "red",   "component": "weave-user-store"},
    {"id": "dt-syn-weave-user",       "label": "User Lookup",            "indicator_type": "Synthetic",     "health": "red",   "component": "weave-user-store"},
    {"id": "dt-pg-weave-audit",       "label": "weave-audit",            "indicator_type": "Process Group", "health": "green", "component": "weave-audit-svc"},
    {"id": "dt-svc-weave-sync",       "label": "IdentitySyncSvc",        "indicator_type": "Service",       "health": "amber", "component": "weave-sync-svc"},
    {"id": "dt-svc-weave-token",      "label": "TokenServiceSvc",        "indicator_type": "Service",       "health": "green", "component": "weave-token-svc"},
    {"id": "dt-pg-weave-consent",     "label": "weave-consent",          "indicator_type": "Process Group", "health": "green", "component": "weave-consent-svc"},
    {"id": "dt-syn-weave-admin",      "label": "Admin Portal Health",    "indicator_type": "Synthetic",     "health": "green", "component": "weave-admin-portal"},
    {"id": "dt-svc-weave-report",     "label": "ComplianceReportSvc",    "indicator_type": "Service",       "health": "amber", "component": "weave-report-svc"},
    {"id": "dt-pg-weave-cache",       "label": "weave-cache",            "indicator_type": "Process Group", "health": "green", "component": "weave-cache-layer"},
    {"id": "dt-pg-weave-eventbus",    "label": "weave-event-bus",        "indicator_type": "Process Group", "health": "red",   "component": "weave-event-bus"},
    {"id": "dt-svc-weave-eventbus",   "label": "EventBusSvc",            "indicator_type": "Service",       "health": "red",   "component": "weave-event-bus"},
    {"id": "dt-syn-weave-entitle",    "label": "Entitlement Check",      "indicator_type": "Synthetic",     "health": "red",   "component": "weave-policy-engine"},

    # ── Real-Time Payments Gateway (62100) - 20 indicators across 15 components ──
    {"id": "dt-pg-rtpg-lb",           "label": "rtpg-ingress-lb",        "indicator_type": "Process Group", "health": "green", "component": "rtpg-ingress-lb"},
    {"id": "dt-svc-rtpg-api",         "label": "RTPGApiGwSvc",           "indicator_type": "Service",       "health": "amber", "component": "rtpg-api-gw"},
    {"id": "dt-pg-rtpg-api",          "label": "rtpg-api-gateway",       "indicator_type": "Process Group", "health": "amber", "component": "rtpg-api-gw"},
    {"id": "dt-svc-rtpg-validation",  "label": "ValidationSvc",          "indicator_type": "Service",       "health": "green", "component": "rtpg-validation-svc"},
    {"id": "dt-pg-rtpg-routing",      "label": "rtpg-routing-engine",    "indicator_type": "Process Group", "health": "red",   "component": "rtpg-routing-engine"},
    {"id": "dt-svc-rtpg-routing",     "label": "RoutingEngineSvc",       "indicator_type": "Service",       "health": "red",   "component": "rtpg-routing-engine"},
    {"id": "dt-syn-rtpg-routing",     "label": "Payment Routing",        "indicator_type": "Synthetic",     "health": "red",   "component": "rtpg-routing-engine"},
    {"id": "dt-svc-rtpg-sanctions",   "label": "SanctionsSvc",           "indicator_type": "Service",       "health": "amber", "component": "rtpg-sanctions-svc"},
    {"id": "dt-svc-rtpg-aml",         "label": "AMLCheckSvc",            "indicator_type": "Service",       "health": "green", "component": "rtpg-aml-svc"},
    {"id": "dt-svc-rtpg-fx",          "label": "FXConverterSvc",         "indicator_type": "Service",       "health": "amber", "component": "rtpg-fx-converter"},
    {"id": "dt-pg-rtpg-clearing",     "label": "rtpg-clearing",          "indicator_type": "Process Group", "health": "red",   "component": "rtpg-clearing-svc"},
    {"id": "dt-syn-rtpg-clearing",    "label": "Clearing Cycle",         "indicator_type": "Synthetic",     "health": "red",   "component": "rtpg-clearing-svc"},
    {"id": "dt-pg-rtpg-settlement",   "label": "rtpg-settlement",        "indicator_type": "Process Group", "health": "red",   "component": "rtpg-settlement-svc"},
    {"id": "dt-svc-rtpg-settlement",  "label": "SettlementEngineSvc",    "indicator_type": "Service",       "health": "red",   "component": "rtpg-settlement-svc"},
    {"id": "dt-svc-rtpg-ledger",      "label": "CoreLedgerSvc",          "indicator_type": "Service",       "health": "amber", "component": "rtpg-ledger-svc"},
    {"id": "dt-svc-rtpg-notif",       "label": "NotifDispatchSvc",       "indicator_type": "Service",       "health": "green", "component": "rtpg-notif-svc"},
    {"id": "dt-pg-rtpg-audit",        "label": "rtpg-audit-trail",       "indicator_type": "Process Group", "health": "green", "component": "rtpg-audit-svc"},
    {"id": "dt-svc-rtpg-recon",       "label": "ReconciliationSvc",      "indicator_type": "Service",       "health": "green", "component": "rtpg-recon-svc"},
    {"id": "dt-pg-rtpg-archive",      "label": "rtpg-archive",           "indicator_type": "Process Group", "health": "green", "component": "rtpg-archive-svc"},
    {"id": "dt-svc-rtpg-monitor",     "label": "HealthMonitorSvc",       "indicator_type": "Service",       "health": "amber", "component": "rtpg-monitor-svc"},

    # ── Digital Channels Platform (77777) — includes high-indicator-count component ──
    {"id": "dt-syn-dcp-portal",       "label": "Portal Health",          "indicator_type": "Synthetic",     "health": "green", "component": "dcp-web-portal"},
    {"id": "dt-pg-dcp-portal",        "label": "dcp-web-portal",         "indicator_type": "Process Group", "health": "green", "component": "dcp-web-portal"},
    # dcp-api-gateway: 12 indicators — simulates a heavily-monitored component
    {"id": "dt-pg-dcp-gw",            "label": "dcp-api-gateway",        "indicator_type": "Process Group", "health": "amber", "component": "dcp-api-gateway"},
    {"id": "dt-svc-dcp-gw",           "label": "APIGatewaySvc",          "indicator_type": "Service",       "health": "amber", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-login",     "label": "Login Flow",             "indicator_type": "Synthetic",     "health": "green", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-checkout",  "label": "Checkout Flow",          "indicator_type": "Synthetic",     "health": "red",   "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-search",    "label": "Search Flow",            "indicator_type": "Synthetic",     "health": "green", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-transfer",  "label": "Transfer Flow",          "indicator_type": "Synthetic",     "health": "amber", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-dashboard", "label": "Dashboard Load",         "indicator_type": "Synthetic",     "health": "green", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-profile",   "label": "Profile Update",         "indicator_type": "Synthetic",     "health": "green", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-alerts",    "label": "Alert Delivery",         "indicator_type": "Synthetic",     "health": "amber", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-export",    "label": "Data Export",            "indicator_type": "Synthetic",     "health": "green", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-onboard",   "label": "Onboarding Flow",        "indicator_type": "Synthetic",     "health": "green", "component": "dcp-api-gateway"},
    {"id": "dt-syn-dcp-gw-mfa",       "label": "MFA Verification",       "indicator_type": "Synthetic",     "health": "red",   "component": "dcp-api-gateway"},
    {"id": "dt-svc-dcp-auth",         "label": "AuthService",            "indicator_type": "Service",       "health": "green", "component": "dcp-auth-svc"},
    {"id": "dt-svc-dcp-mobile",       "label": "MobileBFFSvc",           "indicator_type": "Service",       "health": "red",   "component": "dcp-mobile-bff"},
    {"id": "dt-pg-dcp-mobile",        "label": "dcp-mobile-bff",         "indicator_type": "Process Group", "health": "red",   "component": "dcp-mobile-bff"},
    {"id": "dt-syn-dcp-mobile",       "label": "Mobile App Flow",        "indicator_type": "Synthetic",     "health": "red",   "component": "dcp-mobile-bff"},
]

PLATFORM_NODES = [
    # GAP (Global Application Platform) pools
    {"id": "gap-pool-na-01",      "label": "NA-5S",    "type": "gap", "subtype": "pool",    "datacenter": "NA-NW-C02",      "status": "healthy"},
    {"id": "gap-pool-apac-01",    "label": "AP-6T",    "type": "gap", "subtype": "pool",    "datacenter": "AP-HK-C02",      "status": "warning"},
    {"id": "gap-pool-emea-01",    "label": "EM-5U",    "type": "gap", "subtype": "pool",    "datacenter": "EM-CH-Lausanne",  "status": "healthy"},
    # GKP (Global Kubernetes Platform) clusters
    {"id": "gkp-cluster-na-01",   "label": "NA-K8S-01",   "type": "gkp", "subtype": "cluster", "datacenter": "NA-NW-C02",      "status": "critical"},
    {"id": "gkp-cluster-apac-01", "label": "AP-K8S-02",   "type": "gkp", "subtype": "cluster", "datacenter": "AP-HK-C02",      "status": "healthy"},
    {"id": "gkp-cluster-emea-01", "label": "EM-K8S-01",   "type": "gkp", "subtype": "cluster", "datacenter": "EM-CH-Lausanne",  "status": "warning"},
    # ECS (Elastic Container Service)
    {"id": "ecs-na-01",           "label": "NA-ECS-01",   "type": "ecs", "subtype": "service", "datacenter": "NA-NW-C02",      "status": "healthy"},
    {"id": "ecs-apac-01",         "label": "AP-ECS-02",   "type": "ecs", "subtype": "service", "datacenter": "AP-HK-C02",      "status": "healthy"},
    # EKS (Elastic Kubernetes Service)
    {"id": "eks-na-01",           "label": "NA-EKS-01",   "type": "eks", "subtype": "service", "datacenter": "NA-NW-C02",      "status": "warning"},
    {"id": "eks-emea-01",         "label": "EM-EKS-01",   "type": "eks", "subtype": "service", "datacenter": "EM-CH-Lausanne",  "status": "healthy"},
]

PLATFORM_NODE_MAP = {n["id"]: n for n in PLATFORM_NODES}

# Every component in every SEAL has exactly one platform edge
COMPONENT_PLATFORM_EDGES = [
    # ── Connect OS (88180) - Simple ──
    ("connect-portal",        "gap-pool-na-01"),
    ("connect-cloud-gw",      "gkp-cluster-na-01"),
    ("connect-auth-svc",      "gkp-cluster-na-01"),
    ("connect-home-app-na",   "gap-pool-na-01"),
    ("connect-home-app-apac", "gap-pool-apac-01"),
    ("connect-home-app-emea", "gap-pool-emea-01"),
    # ── Advisor Connect (90176) - Medium ──
    ("connect-profile-svc",   "gap-pool-na-01"),
    ("connect-coverage-app",  "gap-pool-na-01"),
    ("connect-notification",  "gkp-cluster-na-01"),
    ("connect-data-sync",     "gkp-cluster-apac-01"),
    ("connect-doc-svc",       "ecs-na-01"),
    ("connect-pref-svc",      "gap-pool-na-01"),
    ("connect-audit-svc",     "gkp-cluster-na-01"),
    ("active-advisory",       "ecs-na-01"),
    ("ipbol-account",         "gap-pool-apac-01"),
    ("ipbol-doc-domain",      "gap-pool-emea-01"),
    # ── Spectrum Portfolio Mgmt (90215) - Complex ──
    ("spieq-ui-service",      "gap-pool-na-01"),
    ("spieq-api-gateway",     "gkp-cluster-na-01"),
    ("spieq-trade-service",   "gkp-cluster-na-01"),
    ("spieq-portfolio-svc",   "gkp-cluster-na-01"),
    ("spieq-pricing-engine",  "eks-na-01"),
    ("spieq-risk-service",    "gkp-cluster-na-01"),
    ("spieq-order-router",    "eks-na-01"),
    ("spieq-market-data",     "ecs-apac-01"),
    ("spieq-compliance-svc",  "gkp-cluster-emea-01"),
    ("spieq-settlement-svc",  "gkp-cluster-emea-01"),
    ("spieq-audit-trail",     "ecs-apac-01"),
    ("spieq-notif-svc",       "eks-emea-01"),
    ("payment-gateway",       "gap-pool-na-01"),
    ("email-notification",    "ecs-na-01"),
    # ── Morgan Money (16649) - Ultra Simple ──
    ("mm-ui",                 "gap-pool-na-01"),
    ("mm-api",                "gkp-cluster-na-01"),
    ("mm-data-svc",           "gkp-cluster-na-01"),
    # ── PANDA (35115) - Simple ──
    ("panda-gateway",         "gap-pool-na-01"),
    ("panda-data-svc",        "gkp-cluster-na-01"),
    ("panda-cache-svc",       "gkp-cluster-na-01"),
    ("panda-export-svc",      "ecs-na-01"),
    # ── Quantum (91001) - Medium ──
    ("quantum-portal",        "gap-pool-na-01"),
    ("quantum-api-gw",        "gkp-cluster-na-01"),
    ("quantum-portfolio-svc", "gkp-cluster-na-01"),
    ("quantum-analytics-svc", "eks-na-01"),
    ("quantum-report-svc",    "ecs-na-01"),
    ("quantum-data-lake",     "gkp-cluster-apac-01"),
    ("quantum-auth-svc",      "gkp-cluster-na-01"),
    # ── Order Decision Engine (81884) - Medium ──
    ("ode-router",            "gap-pool-na-01"),
    ("ode-rule-engine",       "gkp-cluster-na-01"),
    ("ode-market-feed",       "eks-na-01"),
    ("ode-risk-check",        "gkp-cluster-na-01"),
    ("ode-exec-svc",          "gkp-cluster-na-01"),
    ("ode-audit-log",         "ecs-na-01"),
    ("ode-notif-svc",         "ecs-na-01"),
    ("ode-reconcile-svc",     "gkp-cluster-emea-01"),
    # ── Credit Card Processing Engine (45440) - Complex ──
    ("ccpe-ingress",          "gap-pool-na-01"),
    ("ccpe-auth-svc",         "gkp-cluster-na-01"),
    ("ccpe-fraud-engine",     "gkp-cluster-na-01"),
    ("ccpe-ledger-svc",       "gkp-cluster-na-01"),
    ("ccpe-limit-svc",        "eks-na-01"),
    ("ccpe-notif-svc",        "ecs-na-01"),
    ("ccpe-dispute-svc",      "gkp-cluster-emea-01"),
    ("ccpe-rewards-svc",      "ecs-apac-01"),
    ("ccpe-settlement-svc",   "gkp-cluster-emea-01"),
    ("ccpe-report-svc",       "ecs-apac-01"),
    ("ccpe-archive-svc",      "eks-emea-01"),
    # ── WEAVE / AWM Entitlements (102987) - Complex ──
    ("weave-gateway",         "gap-pool-na-01"),
    ("weave-policy-engine",   "gkp-cluster-na-01"),
    ("weave-role-svc",        "gkp-cluster-na-01"),
    ("weave-user-store",      "gkp-cluster-na-01"),
    ("weave-audit-svc",       "ecs-na-01"),
    ("weave-sync-svc",        "gkp-cluster-apac-01"),
    ("weave-token-svc",       "gkp-cluster-na-01"),
    ("weave-consent-svc",     "gap-pool-emea-01"),
    ("weave-admin-portal",    "gap-pool-na-01"),
    ("weave-report-svc",      "ecs-apac-01"),
    ("weave-cache-layer",     "eks-na-01"),
    ("weave-event-bus",       "gkp-cluster-emea-01"),
    # ── Real-Time Payments Gateway (62100) - Very Complex ──
    ("rtpg-ingress-lb",       "gap-pool-na-01"),
    ("rtpg-api-gw",           "gkp-cluster-na-01"),
    ("rtpg-validation-svc",   "gkp-cluster-na-01"),
    ("rtpg-routing-engine",   "gkp-cluster-na-01"),
    ("rtpg-sanctions-svc",    "eks-na-01"),
    ("rtpg-aml-svc",          "eks-na-01"),
    ("rtpg-fx-converter",     "gkp-cluster-emea-01"),
    ("rtpg-clearing-svc",     "gkp-cluster-na-01"),
    ("rtpg-settlement-svc",   "gkp-cluster-apac-01"),
    ("rtpg-ledger-svc",       "gkp-cluster-na-01"),
    ("rtpg-notif-svc",        "ecs-na-01"),
    ("rtpg-audit-svc",        "ecs-apac-01"),
    ("rtpg-recon-svc",        "gkp-cluster-emea-01"),
    ("rtpg-archive-svc",      "eks-emea-01"),
    ("rtpg-monitor-svc",      "ecs-na-01"),
]

DATA_CENTER_NODES = [
    {"id": "dc-na-nw-c02",      "label": "NA-NW-C02",      "region": "NA",   "status": "healthy"},
    {"id": "dc-na-ne-c01",      "label": "NA-NE-C01",      "region": "NA",   "status": "warning"},
    {"id": "dc-ap-hk-c02",      "label": "AP-HK-C02",      "region": "APAC", "status": "healthy"},
    {"id": "dc-ap-sg-c01",      "label": "AP-SG-C01",      "region": "APAC", "status": "critical"},
    {"id": "dc-em-ch-lausanne", "label": "EM-CH-Lausanne",  "region": "EMEA", "status": "healthy"},
    {"id": "dc-em-uk-c01",      "label": "EM-UK-C01",      "region": "EMEA", "status": "healthy"},
]

# Computed: datacenter label -> datacenter node id
DC_LOOKUP = {
    "NA-NW-C02":      "dc-na-nw-c02",
    "NA-NE-C01":      "dc-na-ne-c01",
    "AP-HK-C02":      "dc-ap-hk-c02",
    "AP-SG-C01":      "dc-ap-sg-c01",
    "EM-CH-Lausanne": "dc-em-ch-lausanne",
    "EM-UK-C01":      "dc-em-uk-c01",
}

# Reverse lookup: component_id -> seal_id (for cross-app edge detection)
COMP_TO_SEAL = {}
for _sid, _comps in SEAL_COMPONENTS.items():
    for _cid in _comps:
        COMP_TO_SEAL[_cid] = _sid

# SEAL labels for external node display
SEAL_LABELS = {
    "16649": "Morgan Money", "35115": "PANDA", "88180": "Connect OS",
    "90176": "Advisor Connect", "81884": "Order Decision Engine",
    "91001": "Quantum", "45440": "Credit Card Processing Engine",
    "102987": "AWM Entitlements (WEAVE)", "90215": "Spectrum Portfolio Mgmt",
    "62100": "Real-Time Payments Gateway", "77777": "Digital Channels Platform",
}

# Component-to-component edges that communicate in both directions
BIDIRECTIONAL_PAIRS = {
    # Connect OS - portal and cloud gateway exchange requests/responses
    ("connect-portal", "connect-cloud-gw"),
    # Advisor Connect - profile service and data sync synchronize bidirectionally
    ("connect-profile-svc", "connect-data-sync"),
    # Spectrum - API gateway and trade service exchange order flow
    ("spieq-api-gateway", "spieq-trade-service"),
    # Spectrum - trade service and risk service validate in both directions
    ("spieq-trade-service", "spieq-risk-service"),
    # Quantum - portfolio service and data lake exchange data bidirectionally
    ("quantum-portfolio-svc", "quantum-data-lake"),
    # ODE - risk check and execution service validate in both directions
    ("ode-risk-check", "ode-exec-svc"),
    # CCPE - fraud engine and ledger exchange transaction data
    ("ccpe-fraud-engine", "ccpe-ledger-svc"),
    # WEAVE - role service and user store synchronize bidirectionally
    ("weave-role-svc", "weave-user-store"),
    # WEAVE - user store and identity sync exchange data
    ("weave-user-store", "weave-sync-svc"),
    # RTPG - routing engine and clearing engine exchange flow
    ("rtpg-routing-engine", "rtpg-clearing-svc"),
    # RTPG - clearing and settlement exchange transaction data
    ("rtpg-clearing-svc", "rtpg-settlement-svc"),
}
