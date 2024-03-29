from pydantic import BaseModel
from typing import Optional, Union, List
from queries.pool import pool
from fastapi import HTTPException


class DuplicateUserError(ValueError):
    pass


class Error(BaseModel):
    message: str


class UserIn(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    profile_image: Optional[str]


class UserUpdateIn(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_image: Optional[str]


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    profile_image: Optional[str]


class UsersOut(BaseModel):
    users: List[UserOut]


class BasicUserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    profile_image: Optional[str]


class UserOutWithPassword(UserOut):
    hashed_password: str


class UserRepository:
    def get(self, username: str) -> UserOutWithPassword:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT
                        id,
                        email,
                        password,
                        first_name,
                        last_name,
                        profile_image
                        FROM users
                        WHERE email = %s;
                        """,
                        [username],
                    )
                    record = result.fetchone()
                    if record is None:
                        return None
                    return self.record_to_user_out_with_pw(record)
        except Exception:
            raise HTTPException(status_code=400, detail="Could not get user")

    def create(
        self, user: UserIn, hashed_password: str
    ) -> Union[UserOut, DuplicateUserError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO users
                        (
                        email,
                        password,
                        first_name,
                        last_name,
                        profile_image
                        )
                        VALUES
                        (%s, %s, %s, %s, %s)
                        RETURNING id;
                        """,
                        [
                            user.email,
                            hashed_password,
                            user.first_name,
                            user.last_name,
                            user.profile_image,
                        ],
                    )
                    conn.commit()
                    id = result.fetchone()[0]
                    result_object = UserOut(
                        id=id,
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        profile_image=user.profile_image,
                    )
                    return result_object
        except Exception:
            raise HTTPException(
                status_code=403, detail="Account could not be created"
            )
