from fastapi import Depends, FastAPI, Request
from starlette.responses import JSONResponse

from app.security.security import verify_token
from app.routers.master_router import master_router
from app.services.exceptions.listing_already_exists import ListingAlreadyExists
from app.services.exceptions.listing_delete_permission import ListingDeletePermission
from app.services.exceptions.listing_not_found import ListingNotFound
from app.services.exceptions.comment import add_exception_handlers

app = FastAPI()

add_exception_handlers(app=app)

app.include_router(master_router)


app.swagger_ui_init_oauth = {
    "clientId": "used-car-backend",
    "appName": "Keycloak Login",
    "usePkceWithAuthorizationCodeGrant": True,
    "scopes": "openid profile",
}


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.get("/protected")
async def protected_method(payload: dict = Depends(verify_token)):
    return {"user": payload.get("preferred_username"), "sub": payload.get("sub")}


@app.exception_handler(ListingNotFound)
async def listing_not_found_exception_handler(request: Request, exc: ListingNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Listing with id: {exc.listing_id} not found"},
    )


@app.exception_handler(ListingAlreadyExists)
async def listing_already_exists_exception_handler(
    request: Request, exc: ListingAlreadyExists
):
    return JSONResponse(
        status_code=404,
        content={"message": f"Listing with a title:{exc.title} already exists!"},
    )


@app.exception_handler(ListingDeletePermission)
async def listing_delete_permission_exception_handler(
    request: Request, exc: ListingDeletePermission
):
    return JSONResponse(status_code=403, content=str(exc))
