import calendar
import datetime
import re

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.views.generic.base import ContextMixin


def to_float(x):
    x = re.sub('[$,]', '', x)
    return float(x)


def to_date(x):
    if isinstance(x, str):
        x = parser.parse(x)
    if isinstance(x, datetime.datetime):
        x = x.date()
    return x


class LoadRequestDateMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = {
            'date': self.date,
            'start': self.start_date,
            'end': self.end_date,
            'next': self.date + relativedelta(months=1),
            'prev': self.date - relativedelta(months=1),
            'current': self.date.strftime('%Y-%m') == datetime.date.today().strftime('%Y-%m')
        }
        return context

    def load_request_date(self):
        date = self.request.GET.get('date', datetime.date.today())
        self.date = to_date(date)
        self.year = self.date.year
        self.month = self.date.month
        _, days = calendar.monthrange(self.year, self.month)
        self.start_date = self.date.replace(day=1)
        self.end_date = self.date.replace(day=days)
        if self.date < datetime.date.today():
            self.date = self.end_date
        self.next_date = self.date + relativedelta(months=1),
        self.prev_date = self.date - relativedelta(months=1)
