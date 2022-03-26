
from tabnanny import check
from django.db import models



class Commission(models.Model):
    reservation = models.CharField(max_length = 100)
    checkin_month = models.CharField(max_length = 10)
    checkin_year = models.CharField(max_length = 10)
    checkin_day = models.CharField(max_length = 10)
    checkout = models.DateField()
    flat = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    income = models.FloatField()
       

    @property
    def com(self):
        if self.city == "LONDON":
            return self.income * 0.10
        elif self.city == "PARIS":
            return self.income * 0.12
        elif self.city == "PORTO":
            return self.income * 0.09

    def save(self,*args,**kwargs):
        if self.checkin_month == '01':
            self.checkin_month ="January"
        elif self.checkin_month == "02":
            self.checkin_month="February"
        if self.checkin_month == '03':
            self.checkin_month ="March"
        elif self.checkin_month == "04":
            self.checkin_month="April"
        if self.checkin_month == '05':
            self.checkin_month ="May"
        elif self.checkin_month == "06":
            self.checkin_month="June"
        if self.checkin_month == '07':
            self.checkin_month ="july"
        elif self.checkin_month == "08":
            self.checkin_month="August"
        if self.checkin_month == '09':
            self.checkin_month ="September"
        elif self.checkin_month == "10":
            self.checkin_month="Octomber"
        if self.checkin_month == '11':
            self.checkin_month ="November"
        elif self.checkin_month == "12":
            self.checkin_month="December"
        self.checkin_month = self.checkin_month
        super().save(*args,**kwargs)
