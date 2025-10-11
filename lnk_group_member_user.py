class Lnk_group_member_user:
    def __init__(self, group, user):
        self.group = group
        self.user = user

    def __repr__(self):
        return f"Lnk_group_member_user(group={self.group}, user={self.user})"