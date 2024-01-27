from django import forms
from .models import Expense, Category

SORT_CHOICES = (
        ('', 'No Sorting'),
        ('category', 'Category Ascending'),
        ('-category', 'Category Descending'),
        ('date', 'Date Ascending'),
        ('-date', 'Date Descending'),
    )

class ExpenseSearchForm(forms.ModelForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False)

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

