from fastapi import (
    Depends,
    APIRouter,
)
from authenticator import authenticator

from queries.member_queries import (
    Member,
    MembersList,
    MembersRepo
    )

router = APIRouter(tags=["members"])


@router.post("/api/group/{group_id}/member", response_model=Member)
def create_member(
    group_id: int,
    repo: MembersRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    user_id = account_data["id"]
    return repo.create(group_id, user_id)
