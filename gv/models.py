from django.db import models

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
    shop_name  = models.CharField(max_length = 30)
    utilization_time = models.CharField(max_length = 30)
    utilization_time_list = ['1','2']
    area_list = [['西池袋','西池袋'],['東池袋','東池袋']]
    area = models.CharField(max_length = 30, choices=area_list)
    genre = models.CharField(max_length = 30)
    price = models.IntegerField()
    number_of_people = models.IntegerField()
    evaluation_quality = models.IntegerField()
    evaluation_amount = models.IntegerField()
    duration = models.IntegerField()
    sex = models.CharField(max_length = 30)
    photograph_shine = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    '''
    def __str__(self):
        created_at = self.created_at
        return created_at
        '''

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
