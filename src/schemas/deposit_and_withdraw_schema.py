deposit_and_withdraw_schema = {
    "type": "object",
    "properties": {
        "account_number": {"type": "integer"},
        "amount": {"type": "integer", "minimum": 1},
    },
    "required": ["account_number", "amount"],
    "additionalProperties": False,
}
