import unittest

from src.api.user_role.user_role import UserRole
from src.api.users.db_services import UserDBService
from src.shared.entity import Session
from src.shared.test_base import DBBaseTestCase


class DBServicesTestCase(DBBaseTestCase):
    def test_get_user_roles_by_id_or_email(self):
        user_role1 = UserRole(1, 1)
        session = Session()
        session.add(user_role1)
        session.commit()

        roles = UserDBService.get_user_role_names_by_user_id_or_email(1)
        self.assertEqual(roles, ['administrateur'])

        roles = UserDBService.get_user_role_names_by_user_id_or_email(77)
        self.assertEqual(roles, [])

        roles = UserDBService.get_user_role_names_by_user_id_or_email('testmaill@mail.ml')
        self.assertEqual(roles, ['administrateur'])

        roles = UserDBService.get_user_role_names_by_user_id_or_email('')
        self.assertEqual(roles, [])


if __name__ == '__main__':
    unittest.main()
