import re
from datetime import datetime

from django.db import models
from django.utils import timezone

from budget.models import Budget
from nerdbudget.utils import to_float


class Ledger(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    description = models.CharField(max_length=250)
    pattern = models.CharField(max_length=250)
    amount = models.FloatField()
    balance = models.FloatField()
    sequence = models.IntegerField()
    original_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)

    budget = models.ForeignKey(Budget, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-date', '-created_at', '-sequence']

    def save(self, *args, **kwargs):
        '''
        On Save update some automagic fields
        '''
        self.original_text = self.original_text.upper()
        if self.id:
            self.modified_at = timezone.now()

        return super().save(*args, **kwargs)

    def parse(self):
        if self.original_text:
            #  0           1       2        3       4       5       6
            #  DATE        MEMO    REF#     $W/D	$DEP    $BAL    {junk}
            data = self.original_text.upper().split('\t')

            self.date = self.get_date(data[0])
            self.description = re.sub(' +', ' ', data[1])
            self.pattern = self.get_pattern()
            self.amount = self.get_amount(data[3], data[4])
            self.balance = self.get_balance(data[5])

    def get_date(self, date):
        return datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

    def get_amount(self, withdrawal, deposit):
        if withdrawal != '':
            return to_float(withdrawal)*-1
        return to_float(deposit)

    def get_balance(self, balance):
        return to_float(balance)

    def get_pattern(self):
        tmp = self.description
        #  remove anything but numbers and letters
        tmp = re.sub('[^0-9A-Z#/]', '', tmp)
        #   CONF#[0-9]+ [CONF]
        tmp = re.sub('CONF#[0-9]+', '{CONF}', tmp)
        #   REF#[0-9]+ [CONF]
        tmp = re.sub('REF#[0-9]+', '{REF}', tmp)
        #  replace date numbers with [DATE]
        tmp = re.sub('[0-9]{2}/[0-9]{2}/[0-9]{2,4}', '{DATE}', tmp)
        #  replace date numbers with [PHONE]
        tmp = re.sub('[0-9]{3}-[0-9]{3}-[0-9]{4}', '{PHONE}', tmp)
        #  replace five or more numbers with [NBR]
        tmp = re.sub('[0-9]{5,}', '{NBR}', tmp)
        return tmp

    def find_budget(self):
        similar = Ledger.objects \
            .filter(pattern=self.pattern) \
            .order_by('-date').first()

        if similar is not None:
            self.budget = similar.budget
