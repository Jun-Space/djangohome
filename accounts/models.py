from django.contrib.auth.models import User
from django.db import models


class Subscriber(models.Model):
    sex = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=1, null=True, choices=sex)
    age = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, null=True)
    date_enrolled = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)  # 여기에 self.user로만 하면 admin페이지에서 에러, 폼 생성 에러 등 수많은 에러 발생, str(self.user)로 하면 문제 해결


class Interest(models.Model):
    field_of_hobby = (
        ('Sport', 'Sport'),
        ('Game', 'Game'),
        ('Music', 'Music'),
        ('Society', 'Society'),
        ('Education', 'Education'),
    )
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    hobby = models.CharField(max_length=20, null=True, choices=field_of_hobby)
    detail = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.hobby + ' : ' + self.detail
