import unittest

from src.api.user_role.user_role import UserRole
from src.api.users.db_services import UserDBService
from src.api.users.entities import RevokedToken
from src.shared.test_base import DBBaseTestCase


class UserDBServicesTestCase(DBBaseTestCase):
    def test_get_user_roles_by_id_or_email(self):
        user_role1 = UserRole(1, 1)
        self.db.session.add(user_role1)
        self.db.session.commit()

        roles = UserDBService.get_user_role_names_by_user_id_or_email(1)
        self.assertEqual(roles, ['administrateur'])

        roles = UserDBService.get_user_role_names_by_user_id_or_email(77)
        self.assertEqual(roles, [])

        roles = UserDBService.get_user_role_names_by_user_id_or_email('testmaill@mail.ml')
        self.assertEqual(roles, ['administrateur'])

        roles = UserDBService.get_user_role_names_by_user_id_or_email('')
        self.assertEqual(roles, [])

    def test_check_user_exists_by_id(self):
        user = UserDBService.check_user_exists_by_id(100)
        print(type(user))

    def test_revoked_token(self):
        revoked_token = UserDBService.revoke_token("token to revoke s id")

        self.assertEqual(revoked_token['jti'], "token to revoke s id")

    def test_is_token_revoked(self):
        revoked_token = RevokedToken('hyper revoked jti')
        self.db.session.add(revoked_token)
        self.db.session.commit()

        self.assertEqual(UserDBService.get_revoked_token_by_jti('hyper revoked jti').get('jti'), revoked_token.jti)
        self.assertEqual(UserDBService.get_revoked_token_by_jti('not yet revoked jti').get('jti'), None)


if __name__ == '__main__':
    unittest.main()
