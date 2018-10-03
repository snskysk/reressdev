
from django import forms
######################################################################################
                #10/01追加
###################################################################################

from . import models
from django.forms import formset_factory


from .models import food_pool



class userInfoForm(forms.Form):
    stunum = forms.CharField(label='学籍番号')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class findForm(forms.Form):
    find = forms.CharField(label = '検索', required=False)

######################################################################################
                #10/01追加
###################################################################################


season_list = (
    ('', 'Seaosn'),
    ('春学期', '春学期'),
    ('秋学期', '秋学期'),
    ('通年', '通年'),
)
grade_list = (
    ('', 'grade'),
    ('4','S'),
    ('3','A'),
    ('2','B'),
    ('1','C'),
    ('0','D')
)



class find_my_sub_Form(forms.Form):
    #def __init__(self):
        #self.year_list = get_year_list()
    subname_teacher = forms.CharField(label='科目名/先生', required = False)
    season = forms.ChoiceField(widget=forms.Select, choices = season_list, required = False)
    grade = forms.ChoiceField(widget=forms.Select, choices = grade_list, required = False)
    year = forms.ChoiceField(widget=forms.Select, choices = [('','year')], required = False)
    gv = forms.ChoiceField(widget=forms.RadioSelect(), choices=[('gv', '最新の成績')], required = False)
    category1 = forms.ChoiceField(widget=forms.Select, choices = [('','kind1')], required = False)


class food_pool_Form(forms.ModelForm):
    class Meta:
        model = food_pool
        fields = '__all__'
        read_only_fields = ('created_at')
        widget = {'type':'range'}
