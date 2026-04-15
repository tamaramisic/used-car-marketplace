from keycloak import KeycloakAdmin


class RoleService:
    def __init__(self, keycloak_admin: KeycloakAdmin):
        self.keycloak_admin = keycloak_admin

    def assign_role_to_user(self, user_id: str, role_name: str):
        self.keycloak_admin.assign_realm_roles(user_id=user_id, roles=role_name)
