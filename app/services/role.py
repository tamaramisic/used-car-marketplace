from uuid import UUID

from fastapi import HTTPException
from keycloak import KeycloakGetError

from app.security.keycloak_admin_config import keycloak_admin


class RoleService:
    def __init__(self):
        self.keycloak_admin = keycloak_admin

    def assign_role_to_user(self, keycloak_id: UUID, role_name: str):
        try:
            role_to_assign = self.keycloak_admin.get_realm_role(role_name)
        except KeycloakGetError:
            raise HTTPException(status_code=404, detail="Given role doesn't exist!")

        keycloak_id_str = str(keycloak_id)
        realm_roles = self.keycloak_admin.get_realm_roles_of_user(
            user_id=keycloak_id_str
        )
        role_names = [role["name"] for role in realm_roles if role["name"] == role_name]

        try:
            if not role_names:
                self.keycloak_admin.assign_realm_roles(
                    user_id=keycloak_id_str, roles=[role_to_assign]
                )

                return {"detail": f"Role {role_name} assigned successfully"}
            else:
                raise HTTPException(
                    status_code=404, detail="User already has given role"
                )

        except KeycloakGetError as e:
            raise HTTPException(
                status_code=403, detail=f"Keycloak Permission Error: {e.error_message}"
            )

        # delete role for user - keycloak_admin.delete_realm_roles_of_user()
