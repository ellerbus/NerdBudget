import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from .models import FREQUENCIES, Budget


class BudgetTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_monthly_amount(self):
        amount = 100

        for freq, _ in FREQUENCIES:
            bud = Budget(amount=amount, frequency=freq)

            monthly_amount = bud.get_monthly_amount()

            if bud.frequency == 'NO':
                self.assertEqual(monthly_amount, 0)
            elif bud.frequency == 'W1':
                expected = bud.amount * 52.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'W2':
                expected = bud.amount * 52.0 / 2.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'W3':
                expected = bud.amount * 52.0 / 3.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'W4':
                expected = bud.amount * 52.0 / 4.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'W5':
                expected = bud.amount * 52.0/5.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'W6':
                expected = bud.amount * 52.0 / 6.0/12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'M1':
                expected = bud.amount
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'M2':
                expected = bud.amount * 6.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'MT':
                expected = bud.amount * 24.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'Q1':
                expected = bud.amount * 4.0 / 12.0
                self.assertEqual(monthly_amount, expected)
            elif bud.frequency == 'Y1':
                expected = bud.amount / 12.0
                self.assertEqual(monthly_amount, expected)

    def test_get_yearly_amount(self):
        amount = 100

        for freq, _ in FREQUENCIES:
            bud = Budget(amount=amount, frequency=freq)

            yearly_amount = bud.get_yearly_amount()
            expected = bud.get_monthly_amount() * 12

            if bud.frequency == 'NO':
                self.assertEqual(yearly_amount, 0)
            elif bud.frequency == 'W1':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'W2':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'W3':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'W4':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'W5':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'W6':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'M1':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'M2':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'MT':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'Q1':
                self.assertEqual(yearly_amount, expected)
            elif bud.frequency == 'Y1':
                self.assertEqual(yearly_amount, expected)

    def test_get_next_date(self):
        date = parser.parse('2020-01-01')

        for freq, _ in FREQUENCIES:
            bud = Budget(frequency=freq)
            if bud.frequency == 'NO':
                continue
            dt = bud.get_next_date(date).strftime('%Y-%m-%d')

            if bud.frequency == 'W1':
                expected = datetime.date(2020, 1, 8).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'W2':
                expected = datetime.date(2020, 1, 15).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'W3':
                expected = datetime.date(2020, 1, 22).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'W4':
                expected = datetime.date(2020, 1, 29).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'W5':
                expected = datetime.date(2020, 2, 5).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'W6':
                expected = datetime.date(2020, 2, 12).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'M1':
                expected = datetime.date(2020, 2, 1).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'M2':
                expected = datetime.date(2020, 3, 1).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'MT':
                expected = datetime.date(2020, 2, 15).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'Q1':
                expected = datetime.date(2020, 4, 1).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)
            elif bud.frequency == 'Y1':
                expected = datetime.date(2021, 1, 1).strftime('%Y-%m-%d')
                self.assertEqual(dt, expected)

    def test_get_start_date(self):
        bud = Budget(frequency='W1', start_date='2019-01-04')
        start = bud.get_start_date(2020, 3).strftime('%Y-%m-%d')
        expected = '2020-03-06'
        self.assertEqual(start, expected)

    def test_get_start_date_000(self):
        bud = Budget(frequency='W1', start_date='2020-01-01')
        start = bud.get_start_date(2020, 1).strftime('%Y-%m-%d')
        expected = '2020-01-01'
        self.assertEqual(start, expected)

    def test_get_budget_amount(self):
        bud = Budget(amount=1, frequency='W1', start_date='2020-01-01')
        budget_amount = bud.get_budget_amount(2020, 1, '2020-01-31')
        self.assertEqual(budget_amount, 5)

    def test_get_budget_amount_000(self):
        end = datetime.date(2020, 3, 17)
        bud = Budget(amount=125, frequency='W1', start_date='2020-01-03')
        budget_amount = bud.get_budget_amount(2020, 3, end)
        self.assertEqual(budget_amount, 250)
