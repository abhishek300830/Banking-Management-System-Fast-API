update_customer_schema = {
    "type": "object",
    "properties": {
        "account_no": {"type": "string"},
        "attribute_to_update": {
            "type": "string",
            "enum": ["name", "email", "phone_no", "gender"],
        },
        "attribute_value": {"type": "string"},
    },
    "required": ["account_no", "attribute_to_update", "attribute_value"],
    "additionalProperties": False,
}
