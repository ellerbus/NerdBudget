from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Category


class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'
    context_object_name = 'categories'
    ordering = ['sequence']

    def post(self, request, *args, **kwargs):
        sequence = 1
        for x in request.POST.getlist('id'):
            category = Category.objects.get(pk=x)
            category.sequence = sequence
            category.save()
            sequence += 1
        return super().get(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category/create.html'
    fields = ['name']

    def form_valid(self, form):
        form.instance.sequence = Category.objects.count() + 1
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category/update.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete.html'
    fields = ['name']

    def get_success_url(self):
        return reverse('category-list')
