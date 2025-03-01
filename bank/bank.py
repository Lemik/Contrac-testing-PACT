from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Mock database: Client balances
clients = {
    "123456": {"name": "Alice", "balance": 1000},
    "654321": {"name": "Bob", "balance": 500},
}

class Transaction(BaseModel):
    account_id: str
    amount: float

@app.get("/balance/{account_id}")
def get_balance(account_id: str):
    """Check account balance"""
    if account_id not in clients:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": clients[account_id]["balance"]}

@app.post("/deposit")
def deposit_money(transaction: Transaction):
    """Deposit money into an account"""
    if transaction.account_id not in clients:
        raise HTTPException(status_code=404, detail="Account not found")
    
    clients[transaction.account_id]["balance"] += transaction.amount
    return {"message": "Deposit successful", "new_balance": clients[transaction.account_id]["balance"]}

@app.post("/withdraw")
def withdraw_money(transaction: Transaction):
    """Withdraw money from an account"""
    if transaction.account_id not in clients:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if clients[transaction.account_id]["balance"] < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    clients[transaction.account_id]["balance"] -= transaction.amount
    return {"message": "Withdrawal successful", "new_balance": clients[transaction.account_id]["balance"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
