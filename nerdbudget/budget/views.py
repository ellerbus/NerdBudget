from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from category.models import Category

from .models import Budget


class BudgetListView(ListView):
    queryset = Category.objects.prefetch_related('budget_set').all()
    template_name = 'budget/list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variance'] = Budget.objects.aggregate(
            weekly_amount=Sum('weekly_amount'),
            monthly_amount=Sum('monthly_amount'),
            yearly_amount=Sum('yearly_amount'))
        return context

    def post(self, request, *args, **kwargs):
        sequence = 1
        for x in request.POST.getlist('id'):
            budget = Budget.objects.get(pk=x)
            budget.sequence = sequence
            budget.save()
            sequence += 1
        return super().get(request, *args, **kwargs)


class BudgetCreateView(CreateView):
    model = Budget
    template_name = 'budget/create.html'
    fields = ['category', 'name', 'frequency',
              'amount', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.sequence = Budget.objects.count() + 1
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('budget-list')

    def get_initial(self):
        return {'category': self.request.GET.get('category_id')}


class BudgetUpdateView(UpdateView):
    model = Budget
    template_name = 'budget/update.html'
    fields = ['category', 'name', 'frequency',
              'amount', 'start_date', 'end_date']

    def get_success_url(self):
        return reverse('budget-list')


class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'budget/delete.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('budget-list')
