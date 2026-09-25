# --------------------------------------------------------------------------
# ACTIVATION TEST FILE — AIOO-4 pilot, security_pilot_test_vulnerable.py
#
# This file exists only to trigger the claude-code-security-review pilot
# on activation day. It contains deliberately planted, fake security issues.
# No secret in this file is real. Close this test PR without merging once
# the pilot bot has commented on it.
# --------------------------------------------------------------------------

import sqlite3
import pickle

# --- Planted issue 1: hardcoded secret -------------------------------------
# A real API key or password should never be written directly into source
# code. This value is fake and only exists to confirm the bot flags it.
STRIPE_API_KEY = "sk_test_FAKE_51NotARealKeyDoNotUse000000"


def get_user_by_email(email):
    """Planted issue 2: SQL injection via string formatting.

    User input is inserted directly into the query string instead of
    being passed as a parameter, which lets an attacker break out of the
    intended query using a crafted email value.
    """
    connection = sqlite3.connect("test_pilot.db")
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE email = '%s'" % email  # unsafe
    cursor.execute(query)
    return cursor.fetchone()


def load_user_preferences(raw_bytes):
    """Planted issue 3: unsafe deserialization.

    pickle.loads() executes arbitrary code embedded in its input, so
    calling it on data from an untrusted source (like a network request
    or uploaded file) lets an attacker run code on this server.
    """
    return pickle.loads(raw_bytes)  # unsafe
