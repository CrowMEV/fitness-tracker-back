import fastapi as fa
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from core import cookie, dependency, security
from schemas import SchemaStatusCode, SchemaUser
from services import UserService

router = fa.APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/login/",
    response_class=JSONResponse,
    responses={401: {"model": SchemaStatusCode.StatusCode}},
)
async def login(
    session: dependency.AsyncSessionDepency,
    data: SchemaUser.UserLogin,
):
    user_service = UserService(session)
    user = await user_service.authenticate_user(**data.model_dump())
    if user is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = security.create_access_token({"user_email": user.email})
    response = JSONResponse(content="OK", status_code=fa.status.HTTP_200_OK)
    cookie.set_cookie(response, access_token)
    return response


@router.post(
    "/logout/",
    response_class=JSONResponse,
)
async def logout():
    response = JSONResponse(content="OK", status_code=fa.status.HTTP_200_OK)
    cookie.drop_cookie(response)
    return response


@router.get(
    "/me/",
    response_model=SchemaUser.UserResponse,
    responses={
        400: {"model": SchemaStatusCode.StatusCode},
        401: {"model": SchemaStatusCode.StatusCode},
    },
)
async def get_user_me(user: dependency.GetCurrentUser):
    return user


@router.post(
    "/",
    response_model=SchemaUser.UserResponse,
)
async def create_user(
    data: SchemaUser.CreateUser, session: dependency.AsyncSessionDepency
):
    user_service = UserService(session)

    try:
        user = await user_service.create_user(data.model_dump())
    except IntegrityError as err:
        if err.orig is not None and "uq_users_email" in err.orig.args[0]:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_409_CONFLICT,
                detail=f"User with {data.email} already exist",
            ) from err
        raise err
    return user
