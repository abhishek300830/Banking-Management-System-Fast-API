new_registration_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "pattern": r"[A-Za-z0-9_]+"},
        "password": {
            "type": "string",
            "pattern": r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
            "message": {
                "pattern": "Make sure password is minimum 8 character including (sepecial Char,Number,Caplital and small letter)"
            },
        },
        "name": {"type": "string", "pattern": r"[A-Za-z ]+", "maxlength": 30},
        "email": {
            "type": "string",
            "pattern": r"^[a-zA-Z][a-zA-Z0-9]+\@[a-zA-Z]+\.(in|net|com)",
            "message": {"pattern": "Your email in not valid. Check and try again"},
        },
        "phone": {
            "type": "string",
            "pattern": r"[0-9]{10}",
            "message": {"pattern": "Please Enter Valid Phone Number"},
        },
        "id_proof_type": {"type": "string", "enum": ["Aadhar Card", "Pan Card"]},
        "id_proof": {"type": "string", "minlength": 5},
        "gender": {"type": "string", "enum": ["Male", "Female", "Other"]},
    },
    "required": [
        "username",
        "password",
        "name",
        "email",
        "phone",
        "id_proof_type",
        "id_proof",
        "gender",
    ],
    "additionalProperties": False,
}
