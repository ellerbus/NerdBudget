import calendar
import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from budget.models import Budget
from category.models import Category
from ledger.models import Ledger
from nerdbudget.utils import LoadRequestDateMixin


class AnalysisHomeView(LoadRequestDateMixin, ListView):
    queryset = Category.objects.prefetch_related('budget_set').all()
    template_name = 'analysis/home.html'
    context_object_name = 'categories'

    def get(self, *args, **kwargs):
        self.load_request_date()
        count = Ledger.objects \
            .filter(date__year=self.year, date__month=self.month, budget_id__isnull=True) \
            .count()
        if count > 0:
            return HttpResponseRedirect(reverse('ledger-check'))
        return super().get(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        lookup = self.get_actuals(qs)
        for category in qs:
            budgets = category.budget_set.all()
            for budget in budgets:
                self.load_budget_amounts(budget, lookup)
            self.load_category_amounts(category, budgets)
        return list(qs)

    def load_category_amounts(self, category, budgets):
        category.projected_amount = sum(b.projected_amount for b in budgets)
        category.variance_amount = sum(b.variance_amount for b in budgets)

    def load_budget_amounts(self, budget, lookup):
        y = self.year
        m = self.month
        t = self.date
        p = self.end_date
        budget.actual_amount = lookup.get(budget.id, 0)
        budget.budget_amount = budget.get_budget_amount(y, m, t)
        budget.variance_amount = budget.actual_amount - budget.budget_amount
        budget.projected_amount = budget.get_budget_amount(y, m, p)
        budget.projected_amount -= budget.budget_amount
        budget.projected_amount += budget.variance_amount

    def get_actuals(self, qs):
        actuals = Budget.objects \
            .filter(ledger__date__year=self.year, ledger__date__month=self.month) \
            .values('id') \
            .annotate(amount=Sum('ledger__amount')) \
            .order_by('id')
        lookup = {x.get('id'): x['amount'] for x in actuals}
        return lookup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = context['categories']
        context['summary'] = {
            'variance_amount': sum(c.variance_amount for c in categories),
            'projected_amount': sum(c.projected_amount for c in categories),
        }
        return context
