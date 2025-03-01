import os
import pytest
import requests
from pact import Consumer, Provider

PACT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../pacts/"

# Define the consumer and provider
pact = Consumer("BankFrontend").has_pact_with(Provider("BankAPI"), pact_dir=PACT_DIR)

@pytest.fixture(scope="module", autouse=True)
def pact_mock_server():
    """Starts the mock Pact server before tests"""
    pact.start_service()
    yield
    pact.stop_service()

def test_get_balance():
    """Consumer test for checking balance API"""

    # Define expected interaction
    expected_response = {"account_id": "123456", "balance": 1000}

    (pact
     .given("Account 123456 exists")
     .upon_receiving("a request for account balance")
     .with_request(method="GET", path="/balance/123456")
     .will_respond_with(200, body=expected_response))

    with pact:
        # Simulate API request
        url = f"http://localhost:{pact.port}/balance/123456"
        response = requests.get(url)

        # Validate response
        assert response.status_code == 200
        assert response.json() == expected_response

def test_deposit_money():
    """Consumer test for depositing money"""

    deposit_request = {"account_id": "123456", "amount": 500}
    expected_response = {"message": "Deposit successful", "new_balance": 1500}

    (pact
     .given("Account 123456 exists")
     .upon_receiving("a request to deposit money")
     .with_request(method="POST", path="/deposit", body=deposit_request)
     .will_respond_with(200, body=expected_response))

    with pact:
        url = f"http://localhost:{pact.port}/deposit"
        response = requests.post(url, json=deposit_request)

        assert response.status_code == 200
        assert response.json() == expected_response

def test_withdraw_money():
    """Consumer test for withdrawing money"""

    withdraw_request = {"account_id": "123456", "amount": 200}
    expected_response = {"message": "Withdrawal successful", "new_balance": 1300}

    (pact
     .given("Account 123456 exists with sufficient balance")
     .upon_receiving("a request to withdraw money")
     .with_request(method="POST", path="/withdraw", body=withdraw_request)
     .will_respond_with(200, body=expected_response))

    with pact:
        url = f"http://localhost:{pact.port}/withdraw"
        response = requests.post(url, json=withdraw_request)

        assert response.status_code == 200
        assert response.json() == expected_response
