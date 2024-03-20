from pydantic import BaseModel
from typing import Optional, List
from queries.pool import pool
from .user_queries import BasicUserOut
from fastapi import HTTPException
# from datetime import datetime


class Member(BaseModel):
    group_id: int
    member_id: int


class MembersList(BaseModel):
    attendees: Optional[List[BasicUserOut]]
    event_id: int


class MembersRepo:

    def create(self, group_id: int, user_id: int) -> Member:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        INSERT INTO group_members (
                            group_id,
                            user_id,
                            approved
                        )
                        VALUES
                        (%s, %s, %s);
                        """,
                        [group_id, user_id, False],
                    )

                    return Member(
                        event_id=group_id,
                        user_id=user_id,
                    )
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
