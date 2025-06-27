# backend/fraud_model.py
def calculate_fraud_score(data: dict) -> int:
    score = 0

    if not data.get("device_id_known", False):
        score += 20

    if data.get("location_change", False):
        score += 25

    if data.get("amount_usd", 0) > 500:
        score += 20
    elif data.get("amount_usd", 0) > 200:
        score += 10

    if data.get("purchase_hour", 12) in range(0, 6):  # Midnight to 6am
        score += 10

    if data.get("is_new_account", False):
        score += 15

    if data.get("is_sale_event", False):
        score -= 15  # Allow more flexibility during sales

    return min(max(score, 0), 100)
