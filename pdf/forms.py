from django import forms


class MessageForm(forms.Form):
    '''
    表单验证
    '''
    name = forms.CharField(required=True)
    degree = forms.CharField(required=True)
    edu = forms.CharField(required=True)
    work = forms.CharField(required=True)
    tech = forms.CharField(required=True)
    phone = forms.CharField(required=True)