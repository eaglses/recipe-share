from fastapi import (
    Depends,
    APIRouter,
    Response,
)
from authenticator import authenticator
from typing import Union, Optional, List
from queries.group_queries import (
    groupRepo,
    DuplicateGroupError,
    GroupOwnerID,
    Member,
    NewGroup,
)

router = APIRouter(tags=["group"])


@router.get("/api/group/{group_id}", response_model=Optional[GroupOwnerID])
def get_event(
    group_id: int,
    response: Response,
    repo: groupRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> GroupOwnerID:
    group = repo.get_group(group_id)
    if group is None:
        response.status_code = 404
    return group


@router.post("/group/create", response_model=GroupOwnerID)
def create_group(
    group: NewGroup,
    repo: groupRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    owner_id = account_data["id"]
    try:
        new_group = repo.create(group, owner_id)
        return new_group
    except DuplicateGroupError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
