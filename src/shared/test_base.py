import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.shared.entity import Base


def clean_db(db):
    for table in reversed(Base.metadata.sorted_tables):
        # print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.execute("INSERT INTO public.utilisateur (id_u, nom_u, prenom_u, initiales_u, email_u, password_u, "
                       "active_u) VALUES (1, 'monnom', 'super', 'ms', 'testmaill@mail.ml', "
                       "'$pbkdf2-sha256$29000$fo8xBsD4f6.1FiLEeK/V.g$tAVL90p3.1hZilV7vDVci2hywMdoGrE5nVnFWsmtW4A', "
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
