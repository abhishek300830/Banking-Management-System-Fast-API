login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {
            "type": "string",
            "pattern": r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
            "message": {
                "pattern": "Make sure password is minimum 8 character including (sepecial Char,Number,Caplital and small letter)"
            },
        },
    },
    "required": ["username", "password"],
    "additionalProperties": False,
}
