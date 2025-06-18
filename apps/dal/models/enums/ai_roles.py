class AIRole:
    USER = "user"
    SYSTEM = "system"

    @staticmethod
    def get_all_roles():
        return [AIRole.USER, AIRole.SYSTEM]
