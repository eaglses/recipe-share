import os
from fastapi import Depends
from jwtdown_fastapi.authentication import Authenticator
from queries.user_queries import UserRepository, UserOut, UserOutWithPassword


class UserAuthenticator(Authenticator):
    async def get_account_data(
        self,
        username: str,
        users: UserRepository,
    ):
        # Use your repo to get the user based on the
        # username (which could be an username)
        return users.get(username)

    def get_account_getter(
        self,
        user: UserRepository = Depends(),
    ):
        # Return the user. That's it.
        return user

    def get_hashed_password(self, user: UserOutWithPassword):
        # Return the encrypted password value from your
        # user object
        return user.hashed_password

    def get_account_data_for_cookie(self, user: UserOut):
        # Return the email and the data for the cookie.
        # You must return TWO values from this method.
        return user.email, user


authenticator = UserAuthenticator(os.environ["SIGNING_KEY"])
