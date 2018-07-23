from django import forms
from myapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('product', 'client', 'num_units')
        # fields = ('product', 'num_units')
        widgets = {
            'client': forms. RadioSelect(attrs={'class': 'radio'}),
        }
        labels = {
            'client': "Client Name",
            'num_units': "Quantity",
        }


class InterestForm(forms.Form):
    interested = forms.BooleanField(widget=forms.RadioSelect(choices=[(1, 'Yes'), (0, 'No')]))
    quantity = forms.IntegerField(initial=1)
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea, required=False)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'required': True, 'class': 'validate', 'placeholder': 'Username'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': True, 'class': 'validate input-field', 'placeholder': 'Password'}),
        label="")
