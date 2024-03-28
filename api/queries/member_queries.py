from pydantic import BaseModel
from typing import Union, Optional, List
from queries.pool import pool
from .user_queries import BasicUserOut
from queries.user_queries import Error
from fastapi import HTTPException

# from datetime import datetime


class Member(BaseModel):
    group_id: int
    member_id: int


class MemberApproval(BaseModel):
    group_id: int
    user_id: int
    approved: bool


class BasicUserOutApproval(BaseModel):
    id: int
    first_name: str
    last_name: str
    profile_image: Optional[str]
    approved: bool


class UnapprovedMembersList(BaseModel):
    members: Optional[List[BasicUserOutApproval]]
    group_id: int


class MembersList(BaseModel):
    members: Optional[List[BasicUserOut]]
    group_id: int


class MembersRepo:

    def update(
        self, group_id: int, member: MemberApproval, owner_id: int
    ) -> Union[MemberApproval, Error]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        UPDATE events
                        SET
                        approved = %s,
                        WHERE group_id = %s AND owner_id = %s;
                        """,
                        [
                            True,
                            group_id,
                            owner_id,
                        ],
                    )
                    conn.commit()
                    #  errer is below here ---------------
                updated_event = self.get_event(group_id)
                return updated_event
        except Exception:
            raise HTTPException(
                status_code=403, detail="User cannot update event"
            )

    def delete(self, group_id: int, user_id: int) -> bool:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    db.execute(
                        """
                        DELETE from group_members
                        WHERE group_id = %s AND user_id = %s
                        """,
                        [group_id, user_id],
                    )
                    return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_not_approved(self, group_id: int) -> UnapprovedMembersList:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT
                        users.id,
                        users.first_name,
                        users.last_name,
                        users.profile_image,
                        group_members.approved
                        FROM
                        user_group
                        JOIN group_members ON
                        user_group.id = group_members.group_id
                        JOIN users ON users.id = user_id
                        WHERE user_group.id = %s AND
                        group_members.approved=false;
                        """,
                        [group_id],
                    )
                    records = result.fetchall()
                    members_list = []
                    for record in records:
                        print(members_list)
                        one_member = BasicUserOutApproval(
                            id=record[0],
                            first_name=record[1],
                            last_name=record[2],
                            profile_image=record[3],
                            approved=record[4],
                        )
                        members_list.append(one_member)
                    return UnapprovedMembersList(
                        members=members_list, group_id=group_id
                    )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_all(self, group_id: int) -> MembersList:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT
                        users.id,
                        users.first_name,
                        users.last_name,
                        users.profile_image
                        FROM
                        user_group
                        JOIN group_members ON 
                        user_group.id = group_members.group_id
                        JOIN users ON users.id = user_id
                        WHERE user_group.id = %s;
                        """,
                        [group_id],
                    )
                    records = result.fetchall()
                    members_list = []
                    for record in records:
                        one_member = BasicUserOut(
                            id=record[0],
                            first_name=record[1],
                            last_name=record[2],
                            profile_image=record[3],
                        )
                        members_list.append(one_member)
                    return MembersList(
                        members=members_list, group_id=group_id
                    )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def create(
        self, group_id: int, user_id: int, approved: bool
    ) -> MemberApproval:
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
                        [
                            group_id,
                            user_id,
                            approved,
                        ],
                    )
                    print(
                        group_id,
                        user_id,
                        approved,
                    )
                    return MemberApproval(
                        group_id=group_id,
                        user_id=user_id,
                        approved=approved,
                    )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
