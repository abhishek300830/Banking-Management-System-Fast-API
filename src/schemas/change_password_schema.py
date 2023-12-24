change_password_schema = {
    "type": "object",
    "properties": {
        "old_password": {
            "type": "string",
            "pattern": r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
            "message": {
                "pattern": "Make sure password is minimum 8 character including\
                    (sepecial Char,Number,Caplital and small letter)"
            },
        },
        "new_password": {
            "type": "string",
            "pattern": r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
            "message": {
                "pattern": "Make sure password is minimum 8 character including \
                    (sepecial Char,Number,Caplital and small letter)"
            },
        },
    },
    "required": ["old_password", "new_password"],
    "additionalProperties": False,
}
