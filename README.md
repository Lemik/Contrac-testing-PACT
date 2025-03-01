# Pact Contract Testing for Bank API

## Overview
This project implements **Consumer-Driven Contract Testing** using **Pact** for a simple **Bank API**. The system consists of:
- **Consumer:** `BankFrontend`
- **Provider:** `BankAPI`
- **Pact Broker:** To store and verify contracts

This ensures that the API meets expected contracts before deployment.

---

## 📌 Features
- ✅ Consumer-driven contract generation
- ✅ Provider verification against the contract
- ✅ Pact Broker integration for contract sharing
- ✅ Local testing and verification

---

## 🚀 Installation

### **1️⃣ Install Dependencies**
Ensure you have Python installed, then install required dependencies:
```bash
pip install fastapi uvicorn pact-python pytest requests
```

If using **Pact Broker**, install Ruby and `pact-broker`:
```bash
gem install pact-broker
```

---

## 🏦 Bank API (Provider)
### **Start the Bank API**
```bash
uvicorn bank_api:app --reload
```
**Test if it's running:**
```bash
curl http://127.0.0.1:8000/docs
```

---

## 🛠️ Consumer Testing (BankFrontend)
### **Run Consumer Tests (Generate Pact Files)**
```bash
pytest tests/test_consumer.py
```
This creates a **Pact contract** in the `pacts/` directory.

---

## 📡 Pact Broker (Optional, for Visualization)
### **Run a Local Pact Broker**
```bash
pact-broker --port 9292 --database-url sqlite:pact_broker.db
```

### **Publish Consumer Pact to the Broker**
```bash
pact-broker publish pacts/ --broker-base-url=http://localhost:9292 --consumer-app-version=1.0.0
```
Check **http://localhost:9292** to visualize contracts.

---

## ✅ Provider Verification (BankAPI)
### **Verify API Against Pact Contract**
Ensure **Bank API is running**, then run:
```bash
pytest tests/test_provider.py
```
If using **Pact Broker**:
```bash
pytest tests/test_provider.py --broker-url=http://localhost:9292
```


