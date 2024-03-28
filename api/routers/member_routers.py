from fastapi import Depends, APIRouter, HTTPException
from authenticator import authenticator
from typing import Union
from queries.group_queries import groupRepo
from queries.user_queries import Error
from queries.member_queries import (
    MembersList,
    UnapprovedMembersList,
    MembersRepo,
    MemberApproval,
)

router = APIRouter(tags=["members"])


@router.put(
    "/api/group/{group_id}/approve",
    response_model=Union[MemberApproval, Error],
)
def approve_member(
    group_id: int,
    member: MemberApproval,
    members_repo: MembersRepo = Depends(),
    membersrepo: groupRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> Union[Error, MemberApproval]:
    user = account_data["id"]
    owner_id = membersrepo.get_group(group_id).owner_id
    print(user, "user", owner_id, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    if user != owner_id:
        raise HTTPException(
            status_code=403,
            detail="only the owner may approve members"
            )
    else:
        return members_repo.update(
            group_id,
            member,
            )


@router.delete("/api/group/{group_id}/member", response_model=bool)
def delete_member(
    group_id: int,
    repo: MembersRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    user_id = account_data["id"]
    print(group_id, user_id)
    return repo.delete(group_id, user_id)


@router.get(
    "/api/group/{group_id}/approval", response_model=UnapprovedMembersList
)
def get_not_approved_members(
    group_id: int,
    repo: MembersRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    return repo.get_all_not_approved(group_id)


@router.get("/api/group/{group_id}/members", response_model=MembersList)
def get_group_members(
    group_id: int,
    repo: MembersRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    return repo.get_all(group_id)


@router.post("/api/group/{group_id}/member", response_model=MemberApproval)
def create_member(
    group_id: int,
    approved: bool,
    repo: MembersRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    user_id = account_data["id"]
    return repo.create(group_id, user_id, approved)
