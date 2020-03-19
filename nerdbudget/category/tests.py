from django.test import TestCase

from .models import Category


class CategoryTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_ui_state(self):
        cat = Category(multiplier=1)
        self.assertEqual(cat.get_ui_state(), 'ui-state-disabled')
