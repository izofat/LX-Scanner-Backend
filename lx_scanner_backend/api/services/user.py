from lx_scanner_backend.db.query import Query


class UserService:
    query = Query()

    @classmethod
    def create_user(cls, username: str, password: str):
        create_user_query = cls.query.register_account

        return cls.query.execute_query(create_user_query, True, username, password)
