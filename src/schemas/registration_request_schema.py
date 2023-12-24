registration_request_schema = {
    "type": "object",
    "properties": {
        "request_type": {"type": "string"},
        "user_id": {"type": "integer", "minimum": 0},
        "status": {"type": "string"},
    },
    "required": ["request_type", "user_id", "status"],
    "additionalProperties": False,
}
