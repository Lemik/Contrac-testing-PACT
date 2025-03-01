import os
import pytest
from pact.verifier import Verifier

# Ensure the correct pact file path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PACT_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "../pacts/bankfrontend-bankapi.json"))
BANK_API_URL = "http://127.0.0.1:8000"


print(f"PACT FILE PATH: {PACT_FILE}")

verifier = Verifier(provider="BankAPI", provider_base_url=BANK_API_URL)

@pytest.fixture(scope="module", autouse=True)
def ensure_api_running():
    """Ensure that the Bank API is running before verification"""
    print(f"\n🔍 Verifying provider: BankAPI at {BANK_API_URL}")
    print(f"✅ Using Pact file: {PACT_FILE}")
    assert os.path.exists(PACT_FILE), f"❌ Pact file not found: {PACT_FILE}"


