from pydantic import BaseModel
from typing import Optional, List, Union
from queries.pool import pool
from fastapi import HTTPException
from datetime import datetime

class DuplicateGroupError(ValueError):
    pass

class Member(BaseModel):
    user_id: int

class NewGroup(BaseModel):
    group_name: str


class GroupOwnerID(BaseModel):
    id: int
    owner_id: int
    group_name: str

# class GroupeList(BaseModel):
#     ownerId: int
#     members: Optional[List[Member]]


class groupRepo:

    def record_to_GroupOwnerID(self, record):
        return GroupOwnerID(
            id=record[0],
            owner_id=record[1],
            group_name=record[2],
        )

    def get_group(self, group_id: int) -> Optional[GroupOwnerID]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        SELECT
                        id,
                        owner_id,
                        group_name
                        FROM user_group
                        WHERE id = %s;
                        """,
                        [group_id],
                    )
                    record = result.fetchone()
                    if record is None:
                        return None

                    return self.record_to_GroupOwnerID(record)
        except Exception:
            return {"message": "Could not get that group"}

    def create(
        self, new_group: NewGroup, owner_id: int
    ) -> Union[GroupOwnerID, DuplicateGroupError]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        INSERT INTO user_group (                           
                            group_name,
                            owner_id                                                
                        )
                        VALUES
                            (%s, %s)
                        RETURNING id;
                        """,
                        [
                            new_group.group_name,
                            owner_id,
                        ],
                    )
                    group_id = result.fetchone()[0]

                    conn.commit()
                    result_object = GroupOwnerID(
                        id=group_id,
                        owner_id=owner_id,
                        group_name=new_group.group_name,
                    )
                    return result_object
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=403, detail="User cannot create group"
            )
