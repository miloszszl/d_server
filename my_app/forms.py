from django import forms
from .models import Page

class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('address','weight','encoding','cookies_present','avg_download_time','host')

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['encoding'].widget.attrs.update({'class': 'form-control'})
        self.fields['avg_download_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['host'].widget.attrs.update({'class': 'form-control'})