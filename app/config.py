import os

# ── Feature flags ─────────────────────────────────────────────────────────────
USE_MOCK_DATA = os.environ.get("USE_MOCK_DATA", "true").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# ── Database (for real API integration) ───────────────────────────────────────
# REAL: Set DATABASE_URL to your MySQL connection string
# Example: mysql+pymysql://user:pass@host:3306/uop
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# ── SMTP ──────────────────────────────────────────────────────────────────────
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "uop-api@example.com")
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"

# ── CORS ──────────────────────────────────────────────────────────────────────
# REAL: Restrict to your UI domain(s) in production
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
