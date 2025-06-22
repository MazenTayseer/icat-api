class AIRole:
    USER = "user"
    # System is set to role, it will be inserted at the beginning of the contents sent to AI
    SYSTEM = "user"

    @staticmethod
    def get_all_roles():
        return [AIRole.USER, AIRole.SYSTEM]
