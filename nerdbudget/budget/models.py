import calendar
import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone

from category.models import Category
from nerdbudget.utils import to_date

FREQUENCIES = [
    ('NO', 'None'),
    ('W1', 'Weekly'),
    ('W2', 'Every 2 Weeks'),
    ('W3', 'Every 3 Weeks'),
    ('W4', 'Every 4 Weeks'),
    ('W5', 'Every 5 Weeks'),
    ('W6', 'Every 6 Weeks'),
    ('M1', 'Monthly'),
    ('M2', 'Every 2 Months'),
    ('MT', 'Twice Montly (15th/EOM)'),
    ('Q1', 'Quarterly'),
    ('Y1', 'Yearly'),
]


def this_year():
    today = datetime.date.today()
    dt = datetime.date(today.year, 1, 1)
    return dt


class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    frequency = models.CharField(max_length=2, choices=FREQUENCIES)
    sequence = models.IntegerField()
    start_date = models.DateField(null=True, blank=True, default=this_year)
    end_date = models.DateField(null=True, blank=True)
    amount = models.FloatField()
    weekly_amount = models.FloatField()
    monthly_amount = models.FloatField()
    yearly_amount = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ['sequence']

    def save(self, *args, **kwargs):
        """
        On Save update some automagic fields
        """
        self.name = self.name.upper()
        if self.id:
            self.modified_at = timezone.now()
        if self.category.multiplier == -1:
            self.amount = abs(self.amount) * -1

        self.weekly_amount = self.get_weekly_amount()
        self.monthly_amount = self.get_monthly_amount()
        self.yearly_amount = self.get_yearly_amount()

        return super().save(*args, **kwargs)

    def get_monthly_amount(self):
        if self.frequency == 'NO':
            return 0.0
        if self.frequency == 'W1':
            return self.amount * 52.0 / 12.0
        if self.frequency == 'W2':
            return self.amount * 52.0 / 2.0 / 12.0
        if self.frequency == 'W3':
            return self.amount * 52.0 / 3.0 / 12.0
        if self.frequency == 'W4':
            return self.amount * 52.0 / 4.0 / 12.0
        if self.frequency == 'W5':
            return self.amount * 52.0 / 5.0 / 12.0
        if self.frequency == 'W6':
            return self.amount * 52.0 / 6.0 / 12.0
        if self.frequency == 'M1':
            return self.amount
        if self.frequency == 'M2':
            return self.amount * 6.0 / 12.0
        if self.frequency == 'MT':
            return self.amount * 24.0 / 12.0
        if self.frequency == 'Q1':
            return self.amount * 4.0 / 12.0
        if self.frequency == 'Y1':
            return self.amount / 12.0

        msg = f'{self.frequency} Frequency Not Implemented'
        raise NotImplementedError(msg)

    def get_weekly_amount(self):
        return self.get_monthly_amount() * 12.0 / 52.0

    def get_yearly_amount(self):
        return self.get_monthly_amount() * 12.0

    def get_budget_amount(self, year, month, projected_date):
        #   roll weekly starting at month/1/year
        #   sum as you go
        if self.frequency == 'NO':
            return self.amount
        budget_amount = 0
        start = self.get_start_date(year, month)
        end = self.get_end_date(year, month, projected_date)
        while start <= end:
            if start.year == year and start.month == month:
                budget_amount += self.amount
            start = self.get_next_date(start)
        return budget_amount

    def get_start_date(self, year, month):
        start = to_date(self.start_date)
        if start < datetime.date.today():
            while True:
                if start.year == year and start.month == month:
                    break
                start = self.get_next_date(start)
        return start

    def get_end_date(self, year, month, limit):
        limit = to_date(limit)
        _, days = calendar.monthrange(year, month)
        end = datetime.date(year, month, days)
        if limit < end:
            end = limit
        return to_date(end)

    def get_next_date(self, date):
        date = to_date(date)

        if self.frequency == 'W1':
            return date + relativedelta(days=7*1)
        if self.frequency == 'W2':
            return date + relativedelta(days=7*2)
        if self.frequency == 'W3':
            return date + relativedelta(days=7*3)
        if self.frequency == 'W4':
            return date + relativedelta(days=7*4)
        if self.frequency == 'W5':
            return date + relativedelta(days=7*5)
        if self.frequency == 'W6':
            return date + relativedelta(days=7*6)
        if self.frequency == 'M1':
            return date + relativedelta(months=1)
        if self.frequency == 'M2':
            return date + relativedelta(months=2)
        if self.frequency == 'MT':
            if date.day == 15:
                # end of month
                _, days = calendar.monthrange(date.year, date.month)
                return datetime.date(date.year, date.month, days)
            else:
                # increment one month
                date = date + relativedelta(months=1)
                return datetime.date(date.year, date.month, 15)
        if self.frequency == 'Q1':
            return date + relativedelta(months=3)
        if self.frequency == 'Y1':
            return date + relativedelta(years=1)

        msg = f'{self.frequency} Frequency Not Implemented'
        raise NotImplementedError(msg)

    def __str__(self):
        return self.category.name + ' - ' + self.name
