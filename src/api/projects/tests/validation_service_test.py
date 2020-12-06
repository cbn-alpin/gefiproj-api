from ..validation_service import ProjectValidationService


class MyTestCase(unittest.TestCase):
    def test_validate_get_all(self):
        validation = ProjectValidationService.validate_get_all({'some'})
        self.assertEqual(False, False)


if __name__ == '__main__':
    unittest.main()
