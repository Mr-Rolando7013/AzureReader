class Lnk_serviceprincipal_owner_user:
    def __init__(self, servicePrincipal, user):
        self.servicePrincipal = servicePrincipal
        self.user = user

    def __repr__(self):
        return f"Lnk_serviceprincipal_owner_user(servicePrincipal={self.servicePrincipal}, user={self.user})"