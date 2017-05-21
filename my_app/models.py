from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    ipv4=models.CharField(max_length=15,blank=True,null=True)
    transfer_speed=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)       #mb/s
    mac_address=models.CharField(max_length=16,null=True,blank=True)

    def __str__(self):
        return self.mac_address+' : '+self.ipv4

    class Meta:
        db_table='Users'

class Test(models.Model):
    user=models.ForeignKey('User', related_name='test_u',null=True,blank=True)
    date=models.DateTimeField(default=timezone.now,null=True,blank=True)

    class Meta:
        db_table='Tests'

class Batch(models.Model):
    page = models.ForeignKey('Page', related_name='batch_p',null=True,blank=True)
    test = models.ForeignKey('Test', related_name='batch_t',null=True,blank=True)
    levels = models.IntegerField()

    class Meta:
        db_table='Batch'

    # def __init__(self, levels, page):
    #     self.levels=levels
    #     self.page=page


class Page_Test(models.Model):
    page=models.ForeignKey('Page',related_name='page_test_p',null=True,blank=True)
    test=models.ForeignKey('Test',related_name='page_test_t',null=True,blank=True)
    # with_pictures=models.BooleanField(default=False)
    is_working=models.NullBooleanField(default=True,null=True,blank=True)
    redirection=models.ForeignKey('Page',related_name='page_test_r',null=True,blank=True)
    response_code=models.IntegerField(1000,null=True,blank=True)
    download_time=models.IntegerField(2000,null=True,blank=True)

    class Meta:
        db_table = 'Pages_Tests'

# class Force_Tests(models.Model):
#     page=models.ForeignKey('Page')
#     levels=models.IntegerField()

    # def __str__(self):
    #     return self.date


# class Server(models.Model):
#     name=models.CharField(max_length=2000)
#     ipv4=models.CharField(max_length=15)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table='Servers'

class Page_Host(models.Model):
    domain_name=models.CharField(max_length=2000,null=True,blank=True)
    ipv4=models.CharField(max_length=15,null=True,blank=True)

    class Meta:
        db_table="Page_hosts"

    def __str__(self):
        return "a"

class Page(models.Model):
    address=models.CharField(max_length=5000,null=True,blank=True)
    weight=models.IntegerField(null=True,blank=True)   #kB
    weight_w_pictures=models.IntegerField(null=True,blank=True) #kB
    encoding=models.CharField(max_length=50,null=True,blank=True)
    cookies_present=models.NullBooleanField(default=None,null=True,blank=True)
    avg_download_time=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)  #ms
    force_test = models.NullBooleanField(default=False,null=True,blank=True)
    global_working_percentage=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    last_month_working_percentage=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    redirection_percentage=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    host = models.ForeignKey('Page_Host',related_name='page_h',null=True,blank=True)

    # def __str__(self):
    #     return self.date

    class Meta:
        db_table='Pages'


class Page_Connection(models.Model):
    page_1=models.ForeignKey('Page', related_name='page_connection_1',blank=True)
    page_2=models.ForeignKey('Page', related_name='page_connection_2',blank=True)

    class Meta:
        db_table='Pages_Connections'

    def __str__(self):
        return "a"


class Button(models.Model):
    page = models.ForeignKey('Page', related_name='button_p',null=True,blank=True)
    locator=models.CharField(max_length=5000)
    global_working_percentage = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    last_month_working_percentage = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.locator

    class Meta:
        db_table='Buttons'


class T_P_B(models.Model):
    button = models.ForeignKey('Button', related_name='t_p_b_b',null=True,blank=True)
    is_working=models.NullBooleanField(null=True,blank=True)
    page_test=models.ForeignKey('Page_Test',related_name='p_t_b_pt',null=True,blank=True)

    class Meta:
        db_table='T_P_B'
