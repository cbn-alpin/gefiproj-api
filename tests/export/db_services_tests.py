import unittest

from src.api.exports.db_services import ExportDBService
from src.api.exports.utils import export_funding_item_from_row_proxy
from src.shared.test_base import DBBaseTestCase


class MyTestCase(DBBaseTestCase):
    def test_get_suivi_financement(self):
        result = ExportDBService.get_suivi_financement(1, 2020)

        export_data = []
        for res in result:
            export_data.append(export_funding_item_from_row_proxy(res))
        self.assertEqual([], export_data)


if __name__ == '__main__':
    unittest.main()
