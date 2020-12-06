import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api


def clean_db(db):
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())


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
