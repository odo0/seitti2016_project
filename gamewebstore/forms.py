from django import forms
from .models import UserData, Category, OnlineGame, Company
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import AppendedText, FormActions

class UserDataForm(forms.ModelForm):
    #name = forms.CharField(required=False)
    role = forms.ChoiceField(choices=(('C', 'Customer'), ('D', 'Developer')))

    class Meta:
        model = UserData
        fields = ['name', 'role']

    def clean_full_name(self):
        name = self.cleaned_data.get('name')
        #write validation code.
        return name
    """
    def save(self, commit=True):

        UserData.name = self.cleaned_data['name']
        UserData.role = self.cleaned_data['role']

        if commit:
            UserData.save()
        return UserData"""


class GameInfoForm(forms.ModelForm):
    class Meta:
        model = OnlineGame
        fields = ['name', 'price', 'categories', 'active', 'url', 'description']

    name = forms.CharField(max_length=255)

    price = forms.DecimalField(initial=0, decimal_places=2, max_digits=5)

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    url = forms.URLField()

    description = forms.CharField(widget=forms.Textarea)

    active = forms.BooleanField(
        help_text="Inactive games do not show up in the marketplace and cannot be played by their owners.",
        required=False,
        initial=True
    )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'name',
        AppendedText('price', '€'),
        'categories',
        'active',
        'url',
        'description',
        FormActions(
            Submit('save', 'Save', css_class="btn-primary")
        )
    )


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

    name = forms.CharField(max_length=255)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'name',
        HTML('<div class="col-xs-12"><span class="text-muted">Please ask site staff for assistance if you need to have'
             ' additional user accounts linked to this company.</span></div>'),
        FormActions(
            Submit('save', 'Save', css_class="btn-primary")
        )
    )


class CompanyDeleteForm(forms.Form):

    selection = forms.ChoiceField([
        ("no", "No, don't do anything"),
        ("yes", "Yes, remove the company, but keep its games available"),
        ("yes_and_deactivate", "Yes, remove the company and make its games unavailable")
    ], required=True, initial='no', widget=forms.RadioSelect)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'selection',
        FormActions(
            Submit('save', 'Proceed', css_class="btn-primary")
        )
    )

class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    name = forms.CharField(max_length=255)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        'name',
        FormActions(
            Submit('save', 'Save', css_class="btn-primary")
        )
    )