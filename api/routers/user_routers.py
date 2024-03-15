from fastapi import (
    Depends,
    HTTPException,
    status,
    Response,
    APIRouter,
    Request,
)
from jwtdown_fastapi.authentication import Token
from authenticator import authenticator
from typing import Optional, Union

from pydantic import BaseModel

from queries.user_queries import (
    Error,
    UserIn,
    UserOut,
    UserUpdateIn,
    UsersOut,
    UserRepository,
    DuplicateUserError,
)


class AccountForm(BaseModel):
    username: str
    password: str


class AccountToken(Token):
    account: UserOut


class HttpError(BaseModel):
    detail: str


router = APIRouter(tags=["Users"])


@router.get("/token", response_model=AccountToken | None)
async def get_token(
    request: Request,
    account: UserOut = Depends(authenticator.try_get_current_account_data),
) -> AccountToken | None:
    if account and authenticator.cookie_name in request.cookies:
        return {
            "access_token": request.cookies[authenticator.cookie_name],
            "type": "Bearer",
            "account": account,
        }


@router.post("/api/users", response_model=AccountToken | HttpError)
async def create_account(
    info: UserIn,
    request: Request,
    response: Response,
    repo: UserRepository = Depends(),
):
    hashed_password = authenticator.hash_password(info.password)
    try:
        account = repo.create(info, hashed_password)
    except DuplicateUserError:
        # print(account, "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an user with those credentials",
        )
    form = AccountForm(username=info.email, password=info.password)
    token = await authenticator.login(response, request, form, repo)
    return AccountToken(account=account, **token.dict())


@router.get("/api/users/{user_id}", response_model=Optional[UserOut])
def get_one_user(
    user_id: int,
    response: Response,
    repo: UserRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> UserOut:
    user = repo.get_one(user_id)
    if user is None:
        response.status_code = 404
    return user


@router.get("/api/users", response_model=UsersOut | Error)
def get_all_users(
    repo: UserRepository = Depends(),
):
    return {"users": repo.get_all()}


@router.delete("/api/users/{user_id}", response_model=bool)
def delete_user(
    user_id: int,
    repo: UserRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> bool:
    if user_id == account_data["id"]:
        return repo.delete(user_id)
    else:
        return False


@router.put("/api/users", response_model=Union[UserOut, Error])
def edit_user(
    user: UserUpdateIn,
    response: Response,
    repo: UserRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
) -> Union[Error, UserOut]:
    try:
        return repo.update(account_data["id"], user)
    except Exception as e:
        response.status_code = 400
        return Error(message=str(e))
