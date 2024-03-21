from fastapi import (
    Depends,
    APIRouter,
)
from authenticator import authenticator

from queries.member_queries import (
    Member,
    MembersList,
    MembersRepo,
    MemberApproval,
)

router = APIRouter(tags=["members"])


@router.post("/api/group/{group_id}/member", response_model=MemberApproval)
def create_member(
    group_id: int,
    approved: bool,
    repo: MembersRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    user_id = account_data["id"]
    return repo.create(group_id, user_id, approved)
