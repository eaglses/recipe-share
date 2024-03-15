from fastapi import (
    Depends,
    APIRouter,
)
from authenticator import authenticator

from queries.member_queries import (
    AttendeesOut,
    AttendeesRepo,
    Attendee,
    EventsOut,
)

router = APIRouter(tags=["members"])


@router.post("/api/group/{group_id}/member", response_model=Attendee)
def create_attendee(
    group_id: int,
    repo: AttendeesRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    user_id = account_data["id"]
    return repo.create(group_id, user_id)
