from httpx import AsyncClient, HTTPError
from jose import jwt, jwk
from jose.exceptions import JWTError, ExpiredSignatureError
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.config import keycloak_settings
from fastapi import HTTPException, status, Depends
from pprint import pprint

from app.models.user import User

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl=keycloak_settings.AUTH_URL, tokenUrl=keycloak_settings.TOKEN_URL, scopes={'openid': 'OpenID Connect', 'profile': 'User profile'})


async def verify_token(token: str=Depends(oauth2_scheme)):
    try:
        async with AsyncClient() as client:
            response = await client.get(keycloak_settings.JWKS_URL)
            response.raise_for_status()
            jwks = response.json()
            print('==============================')
            print('JWKS')
            print(jwks)
            print('==============================')
    except HTTPError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Not available.')

    unverified_header = jwt.get_unverified_header(token)
    pprint('==============================')
    pprint('HEADER')
    pprint(unverified_header)
    pprint('==============================')
    kid = unverified_header.get('kid')
    pprint('==============================')
    pprint('KID')
    pprint(kid)
    pprint('==============================')

    if not kid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token missing \'kid\' header', headers={'WWW-Authenticate': 'Bearer'})

    key_data = next((key for key in jwks.get('keys', []) if key.get('kid') == kid), None)
    pprint('==============================')
    pprint('KEY_DATA')
    pprint(key_data)
    pprint('==============================')

    if not key_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Matching key not found in JWKS', headers={'WWW-Authenticate': 'Bearer'})
    
    public_key = jwk.construct(key_data).public_key()
    pprint('==============================')
    pprint('PUBLIC_KEY')
    pprint(public_key)
    pprint('==============================')
    try:
        payload = jwt.decode(token, key=public_key, algorithms=['RS256'], options={'verify_aud': False})
        pprint('==============================')
        pprint('PAYLOAD')
        pprint(payload)
        pprint('==============================')
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired!', headers={'WWW-Authenticate': 'Bearer'})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='An error occurred...', headers={'WWW-Authenticate': 'Bearer'})


def map_token_to_user(payload: dict) -> User:
    return User(
        id=payload.get("sub"),
        username=payload.get("preferred_username"),
        email=payload.get("email"),
        roles=payload.get("realm_access", {}).get("roles", [])
    )