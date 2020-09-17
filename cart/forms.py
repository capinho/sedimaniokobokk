from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ValidationError

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]



class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = "Quantite"
#        self.fields['quantity'].validators.append(test_employee)
#        user = self.user

#        if user.is_staff:
#            if self.fields['quantity'].value >6:
#                raise forms.ValidationError('Wouu sa doole mayoula lolou!')

    def clean(self):
        cleaned_data = super(CartAddProductForm, self).clean()
        quantity = cleaned_data.get('quantity')
        update = cleaned_data.get('update')


class CartAddProductForm1(forms.Form):
    quantity = forms.IntegerField(label=" ",min_value=1,required=True,widget=forms.TextInput(attrs={'placeholder': 'Quantité'}))
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
                                
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CartAddProductForm1, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(CartAddProductForm1, self).clean()
        quantity = cleaned_data.get('quantity')
        update = cleaned_data.get('update')
