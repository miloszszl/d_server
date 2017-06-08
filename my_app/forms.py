from django import forms
from .models import Page

class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('address','weight','cookies_present','host')

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['cookies_present'].widget.attrs.update({'class': 'form-control'})
        self.fields['host'].widget.attrs.update({'class': 'form-control'})