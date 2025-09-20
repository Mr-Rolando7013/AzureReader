class Lnk_au_member_user:
    def __init__(self, administrativeUnit, user):
        self.administrativeUnit = administrativeUnit
        self.user = user

    def __repr__(self):
        return f"Lnk_au_member_user(administrativeUnit={self.administrativeUnit}, user={self.user})"