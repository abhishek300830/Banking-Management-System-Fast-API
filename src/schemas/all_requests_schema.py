all_requests_schema = {
    "type": "object",
    "properties": {
        "request_type": {
            "type": "string",
            "enum": [
                "withdrawn_request",
                "registration_request",
                "modification_request",
            ],
        },
        "status": {
            "type": "string",
            "enum": [
                "approved",
                "rejected",
            ],
        },
    },
    "required": ["request_type", "status"],
}
