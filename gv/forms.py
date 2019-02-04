from django.forms import formset_factory
from django import forms
from . import models
from .models import food_pool
from django.forms.widgets import NumberInput

##########################################

##############################################

class userInfoForm(forms.Form):
    stunum = forms.CharField(label='学籍番号')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class findForm(forms.Form):
    find = forms.CharField(label = '検索', required=False)


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
    year = forms.ChoiceField(widget=forms.Select, choices = [('','year')], required = False)
    season = forms.ChoiceField(widget=forms.Select, choices = season_list, required = False)
    category1 = forms.ChoiceField(widget=forms.Select, choices = [('','kind1')], required = False)
    grade = forms.ChoiceField(widget=forms.Select, choices = grade_list, required = False)



class food_pool_Form(forms.ModelForm):
    #price = forms.IntegerField(widget=NumberInput(attrs={'type':'range', 'min':'0', 'max':'10', 'step': '2'}))
    class Meta:
        model = food_pool
        fields = '__all__'
        read_only_fields = ('created_at')
        widget = {'type':'range'}


class find_shop(forms.Form):
    five_list = [
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    ]
    utilization_time_list = [['朝食','朝食'],['ブランチ','ブランチ'],['昼食','昼食'],['おやつ','おやつ'],\
    ['夕食','夕食'],['夜食','夜食'],['飲み会','飲み会']]
    sex_list = [['女','女'],['男','男'],['その他','その他']]
    area_list = [['池袋駅・北','池袋駅・北'],['池袋駅・東','池袋駅・東'],['池袋駅・南','池袋駅・南'],['池袋駅・西','池袋駅・西']]
    genre_list = [['和食','和食'],['洋食','洋食'],['中華料理','中華料理'],['ラーメン','ラーメン'],['カレー','カレー'],['焼肉','焼肉'],\
    ['鍋','鍋'],['居酒屋・ダイニングバー','居酒屋・ダイニングバー'],['ファミレス','ファミレス'],]
    price_list = [['','価格'],[100,'~200円'],[300,'201円~400円'],[500,'401円~600円'],[700,'601円~800円'],\
    [900,'801円~1000円'],[1250,'1001円~1500円'],[1750,'1501円~2000円'],[2500,'2001円~3000円'],\
    [3001,'3001円~'],[4001,'4001円~']]
    number_list = [[1,'1人'],[2,'2人'],[3,'3人'],[4,'4人'],[5,'5人'],[6,'6人'],\
    [10,'7人~13人'],[14,'14人~']]
    duration_list = [[10,'~10分'],[15,'11分~20分'],[25,'21分~30分'],[30,'31分-60分'],[61,'1時間以上']]




    shop_name = forms.CharField(label='科目名/先生', required = False)
    price = forms.ChoiceField(choices=price_list, required = False)


class find_course(forms.Form):
    category1 = forms.ChoiceField(widget=forms.Select, choices = [('','全体')], required = False)

class find_teacher(forms.Form):
    t_sub_list = [['','全ての教科']]
    t_name = forms.CharField(label='先生')
    t_sub = forms.ChoiceField(choices=t_sub_list, required = False)

class ggs_counter_Form(forms.Form):
    gakunenn_list = [
    (0,'学年選択'),
    (18,'1年生'),
    (17,'2年生'),
    (16,'3年生'),
    (15,'4年生'),
        ]

    gg_name = forms.CharField(label='学科コードを入力')
    gakunenn = forms.ChoiceField(choices=gakunenn_list, required = False,label='学年で絞る')



class find_sub(forms.Form):
    s_name = forms.CharField(label='教科')
