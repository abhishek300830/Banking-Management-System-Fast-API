class User:
    """The class provides properties for users"""

    def __init__(
        self,
        role=None,
        name=None,
        email=None,
        phone=None,
        id_proof_type=None,
        id_proof=None,
        gender=None,
    ):
        self.name = name
        self.email = email
        self.phone_no = phone
        self.role = role
        self.id_proof_type = id_proof_type
        self.id_proof = id_proof
        self.gender = gender
