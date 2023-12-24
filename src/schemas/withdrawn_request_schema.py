withdrawn_request_schema = {
    "type": "object",
    "properties": {
        "request_type": {"type": "string"},
        "request_id": {"type": "integer", "minimum": 0},
        "status": {"type": "string"},
        "comment": {"type": "string", "pattern": "[A-Za-z0-9_ ]+"},
    },
    "required": ["request_type", "request_id", "status", "comment"],
    "additionalProperties": False,
}
