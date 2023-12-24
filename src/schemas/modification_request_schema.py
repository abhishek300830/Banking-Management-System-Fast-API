modification_request_schema = {
    "type": "object",
    "properties": {
        "request_type": {"type": "string"},
        "request_id": {"type": "integer", "minimum": 0},
        "status": {"type": "string"},
    },
    "required": ["request_type", "request_id", "status"],
    "additionalProperties": False,
}
