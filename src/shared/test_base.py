import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.api.amounts.entities import Amount
from src.api.expenses.entities import Expense
from src.api.funders.entities import Funder
from src.api.fundings.entities import Funding
from src.api.projects.entities import Project
from src.api.receipts.entities import Receipt
from src.api.role_acces.entities import RoleAccess
from src.api.user_role.entities import UserRole
from src.api.users.entities import User, RevokedToken


def clean_db(db):
    ordered_tables = [RevokedToken, UserRole, RoleAccess, Receipt, Funding, Project, User, Funder, Expense, Amount]
    for table in ordered_tables:
        db.session.query(table).delete()

    # insert initial roles
    db.session.execute("INSERT INTO public.role_acces (id_ra, nom_ra, code_ra) VALUES (1, 'administrateur', 1)")
    db.session.execute("INSERT INTO public.role_acces (id_ra, nom_ra, code_ra) VALUES (2, 'consultant', 2)")

    # insert initial user with passwod = admin
    db.session.execute("INSERT INTO public.utilisateur (id_u, nom_u, prenom_u, initiales_u, email_u, password_u, "
                       "active_u) VALUES (1, 'monnom', 'super', 'ms', 'testmaill@mail.ml', "
                       "'$pbkdf2-sha256$29000$p1SqNUao1dr7X4vR2hvDGA$B65/miob/RZAB716l.jdkqfrX5zeGlhrGZBPy0STdqE', "
                       "true)")
    db.session.commit()


class DBBaseTestCase(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(cls):
        super(DBBaseTestCase, cls).setUpClass()
        cls.app = create_api('test')
        cls.db = SQLAlchemy()
        cls.db.app = cls.app
        cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_all()
        super(DBBaseTestCase, cls).tearDownClass()

    def setUp(self):
        super(DBBaseTestCase, self).setUp()

        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        clean_db(self.db)

    def tearDown(self):
        self.db.session.rollback()
        self.app_context.pop()

        super(DBBaseTestCase, self).tearDown()
