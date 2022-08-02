from django.db import models
from django.utils import timezone

class Employee(models.Model):
    fname = models.CharField(max_length=26, null=True, blank = True)
    lname = models.CharField(max_length=26, null=True, blank = True)
    email = models.CharField(max_length=50, null=True, blank = True)
    department = models.CharField(max_length=26, null=True, blank = True)
    contact = models.CharField(max_length=26, null=True, blank = True)
    position = models.CharField(max_length=26, null=True, blank = True)
    pin = models.CharField(max_length=26, null=True, blank = True)
    username = models.CharField(max_length=26, null=False, blank = False)
    password = models.CharField(max_length=26, null=False, blank=False)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.username

check_choices = (
    ('checkin','checkin'),
    ('checkout','checkout')
)

class DailyLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=10, choices=check_choices, null=False, default = 'checkin', blank = False)
    time = models.DateTimeField(default=timezone.now())
    message = models.TextField(max_length=1000, null=True, blank = True )

    def __str__(self):
        return str(self.employee) + ' ' + str(self.check_type) + ' ' + str(self.time)
