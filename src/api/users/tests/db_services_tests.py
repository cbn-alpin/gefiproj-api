import unittest

from src.api.user_role.user_role import UserRole
from src.api.users.db_services import UserDBService
from src.shared.entity import Session
from src.shared.test_base import DBBaseTestCase


class DBServicesTestCase(DBBaseTestCase):
    def test_get_user_roles_by_id(self):
        user_role1 = UserRole(1, 1)
        session = Session()
        session.add(user_role1)
        session.commit()

        roles = UserDBService.get_user_role_names_by_user_id(1)
        self.assertEqual(roles, ['administrateur'])


if __name__ == '__main__':
    unittest.main()
