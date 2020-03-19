import datetime

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from category.models import Category
from nerdbudget.utils import LoadRequestDateMixin

from .models import Ledger


class LedgerCheckView(TemplateView):
    template_name = 'ledger/check.html'

    def get(self, request):
        ledger = Ledger.objects.filter(budget_id__isnull=True).first()
        if ledger is None:
            return HttpResponseRedirect(reverse('analysis-home'))
        return HttpResponseRedirect(reverse('ledger-update', kwargs={'pk': ledger.id}))


class LedgerListView(LoadRequestDateMixin, ListView):
    queryset = Ledger.objects.prefetch_related('budget__category')
    template_name = 'ledger/list.html'
    context_object_name = 'ledgers'

    def get_queryset(self):
        self.load_request_date()
        qs = super().get_queryset()
        return qs.filter(date__year=self.year, date__month=self.month)


class LedgerUpdateView(TemplateView):
    template_name = 'ledger/update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ledger'] = Ledger.objects.get(pk=self.kwargs.get('pk'))
        context['categories'] = Category.objects.order_by('sequence')
        return context

    def post(self, request, *args, **kwargs):
        id = request.POST.get('budget')
        ledger = Ledger.objects.get(pk=self.kwargs.get('pk'))
        ledger.budget_id = id
        ledger.save()
        ledgers = Ledger.objects.filter(pattern=ledger.pattern)
        ledgers.update(budget_id=id)
        return HttpResponseRedirect(reverse('ledger-check'))


class LedgerDeleteView(DeleteView):
    model = Ledger
    template_name = 'ledger/delete.html'
    fields = ['date', 'amount', 'balance', 'description']

    def get_success_url(self):
        return reverse('ledger-list')


class LedgerImportView(TemplateView):
    template_name = 'ledger/import.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest'] = Ledger.objects.order_by('-id').first()
        return context

    def post(self, request, *args, **kwargs):
        trx = request.POST.get('transactions')
        if trx != '':
            seq = 1
            for line in reversed(trx.splitlines()):
                if line != '':
                    ledger = Ledger(original_text=line, sequence=seq)
                    ledger.parse()
                    ledger.find_budget()
                    ledger.save()
                    seq += 1
        return HttpResponseRedirect(reverse('ledger-check'))
