transfer_funds_schema = {
    "type": "object",
    "properties": {
        "amount_to_transfer": {"type": "integer"},
        "account_to_transfer": {"type": "integer"},
    },
    "required": ["account_to_transfer", "amount_to_transfer"],
    "additionalProperties": False,
}
