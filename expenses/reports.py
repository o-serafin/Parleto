from collections import OrderedDict
from decimal import Decimal

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.db.models.functions import ExtractYear, ExtractMonth


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))

def total_amount(queryset):
    total = queryset.aggregate(total_amount=Sum('amount'))['total_amount']
    return total if total is not None else Decimal('0.00')

def summary_per_year_month(queryset):
    return queryset \
        .annotate(year=ExtractYear('date'), month=ExtractMonth('date')) \
        .values('year', 'month') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('-year', '-month')
