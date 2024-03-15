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


@router.post("/api/events/{event_id}/attendees", response_model=Attendee)
def create_attendee(
    event_id: int,
    repo: AttendeesRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    user_id = account_data["id"]
    return repo.create(event_id, user_id)
