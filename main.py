from fastapi import Depends, FastAPI
from app.security import verify_token
from app.master_router import master_router


app = FastAPI()

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

#provera pre-commit