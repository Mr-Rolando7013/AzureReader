class Lnk_application_owner_user:
    def __init__(self, application, user):
        self.application = application
        self.user = user

    def __repr__(self):
        return f"Lnk_application_owner_user(application={self.application}, user={self.user})"