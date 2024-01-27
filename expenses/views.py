from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_amount, summary_per_year_month
from django.db.models import Count


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            start_date = form.cleaned_data.get('start_date','')
            end_date = form.cleaned_data.get('end_date','')
            categories = form.cleaned_data.get('categories')
            sort_option = form.cleaned_data.get('sort')

            if name:
                queryset = queryset.filter(name__icontains=name)

            if sort_option:
                queryset = queryset.order_by(sort_option)

            if start_date:
                queryset = queryset.filter(date__gte=start_date)

            if end_date:
                queryset = queryset.filter(date__lte=end_date)

            if categories:
                queryset = queryset.filter(category__in=categories)
        
        return super().get_context_data(
            form=form,
            object_list=queryset,
            year_month_summary = summary_per_year_month(queryset),
            summary_per_category=summary_per_category(queryset),
            total_amount=total_amount(queryset),
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.annotate(expenses_count=Count('expense')).order_by('name')

