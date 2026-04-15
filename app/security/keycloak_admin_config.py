from keycloak import KeycloakAdmin

from app.core.config import keycloak_settings

keycloak_admin = KeycloakAdmin(
    server_url=keycloak_settings.KEYCLOAK_BASE_URL,
    realm_name=keycloak_settings.KEYCLOAK_REALM_NAME,
    client_id=keycloak_settings.ADMIN_CLIENT_ID,
    client_secret_key=keycloak_settings.ADMIN_CLIENT_SECRET,
    # verify=True
)
