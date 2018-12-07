from django.db import models
import datetime

# Create your models here.
class studentInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length = 8)
    student_grade = models.IntegerField()
    enteryear = models.IntegerField()
    seasons = models.IntegerField()
    gpa = models.FloatField()
    def __str__(self):
        return self.user_id

class subjectInfo(models.Model):
    subjectnum = models.CharField(max_length = 15)
    managementnum = models.CharField(max_length = 20)
    user_id = models.CharField(max_length = 10)
    subjectname = models.CharField(max_length = 40)
    unit_int = models.IntegerField()
    grade = models.CharField(max_length = 10)
    grade_score_int = models.IntegerField()
    result_score_int = models.IntegerField()
    year_int = models.IntegerField()
    season = models.CharField(max_length = 10)
    teacher = models.CharField(max_length = 20)
    gpa_int = models.FloatField()
    category1 = models.CharField(max_length = 30)
    category2 = models.CharField(max_length = 30)
    last_login = models.CharField(max_length = 20)
    #studentInfoとの紐づけ
    stu_id = models.ForeignKey(studentInfo, on_delete=models.CASCADE)
    def __str__(self):
        subjectname = self.subjectname
        user_id = self.user_id
        return user_id + 'の' + subjectname
#################################################################
                                #10/03
#################################################################

class food_pool(models.Model):
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
    price_list = [[100,'~200円'],[300,'201円~400円'],[500,'401円~600円'],[700,'601円~800円'],\
    [900,'801円~1000円'],[1250,'1001円~1500円'],[1750,'1501円~2000円'],[2500,'2001円~3000円'],\
    [3001,'3001円~'],[4001,'4001円~']]
    number_list = [[1,'1人'],[2,'2人'],[3,'3人'],[4,'4人'],[5,'5人'],[6,'6人'],\
    [10,'7人~13人'],[14,'14人~']]
    duration_list = [[10,'~10分'],[15,'11分~20分'],[25,'21分~30分'],[30,'31分-60分'],[61,'1時間以上']]

    shop_name  = models.CharField(max_length = 30)
    utilization_time = models.CharField(max_length = 30, choices=utilization_time_list)
    area = models.CharField(max_length = 30, choices=area_list)
    sex = models.CharField(max_length = 30, choices=sex_list)
    genre = models.CharField(max_length = 30, choices=genre_list)
    duration = models.IntegerField(choices=duration_list)
    price = models.IntegerField(choices=price_list)
    number_of_people = models.IntegerField(choices=number_list)
    evaluation_quality = models.IntegerField(choices=five_list)
    evaluation_amount = models.IntegerField(choices=five_list)
    photograph_shine = models.IntegerField(choices=five_list)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        created_at = self.created_at
        created_at = created_at + datetime.timedelta(hours=9)
        return created_at.strftime('%Y/%m/%d %H:%M')+ self.shop_name

###########################################
###########################################


from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
