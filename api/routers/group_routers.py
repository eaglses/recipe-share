from fastapi import (
    Depends,
    APIRouter,
    Response,
    status,
    HTTPException,
)
from authenticator import authenticator
from typing import (
    Union,
    Optional,
    # List,
    )
from queries.user_queries import Error
from queries.group_queries import (
    groupRepo,
    DuplicateGroupError,
    GroupOwnerID,
    # Member,
    NewGroup,
)

router = APIRouter(tags=["group"])


@router.delete("/api/group/{group_id}", response_model=bool)
def delete_event(
    group_id: int,
    repo: groupRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> bool:
    event = repo.get_group(group_id)

    if event and account_data and event.owner_id == account_data["id"]:
        return repo.delete(group_id)
    else:
        return False


@router.put(
    "/api/group/{group_id}",
    response_model=Union[GroupOwnerID, Error],
)
def update_group(
    group_id: int,
    group: NewGroup,
    repo: groupRepo = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> Union[Error, GroupOwnerID]:
    owner_id = account_data["id"]
    old = repo.get_group(group_id)
    if old.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="User cannot update group")
    return repo.update(group_id, group, owner_id)


@router.get("/api/group/{group_id}", response_model=Optional[GroupOwnerID])
def get_group(
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
