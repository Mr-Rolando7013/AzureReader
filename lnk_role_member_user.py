class Lnk_role_member_user:
    def __init__(self, directoryRole, user):
        self.directoryRole = directoryRole
        self.user = user

    def __repr__(self):
        return f"Lnk_role_member_user(directoryRole={self.directoryRole}, user={self.user})"