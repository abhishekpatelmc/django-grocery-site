from django import forms
from myapp1.models import OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'ordered_item',
            'ordered_by',
            'no_of_order'
        ]
        labels = {
            'ordered_item': 'Item',
            'ordered_by': 'Client Name',
            'no_of_order': 'Quantity'
        }
        widgets = {'ordered_by': forms.RadioSelect}


class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    interested = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=INTEREST_CHOICES,
        label='Are you interested in this item?',
        initial=1,
    )
    quantity = forms.IntegerField(
        min_value=1,
        label='How many units are you interested in?',
        initial=1,
    )
    comments = forms.CharField(
        widget=forms.Textarea,
        label='Additional Comments',
        required=False,
    )
