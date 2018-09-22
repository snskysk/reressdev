from django import forms
class userInfoForm(forms.Form):
    stunum = forms.CharField(label='学籍番号')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class findForm(forms.Form):
    find = forms.CharField(label = '検索', required=False)
