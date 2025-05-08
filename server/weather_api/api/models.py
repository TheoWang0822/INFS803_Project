from django.db import models

class CityList(models.Model):
    id = models.AutoField(primary_key=True)
    cityname = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    pwd_hash = models.CharField(max_length=255, blank=True, null=True)
    avatar_id = models.IntegerField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserSession(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserFavorite(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CityWeatherCurrent(models.Model):
    id = models.AutoField(primary_key=True)
    data_dt = models.DateTimeField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temp_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temp_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    simple_desc = models.CharField(max_length=255, blank=True, null=True)
    sunrise = models.DateTimeField(blank=True, null=True)
    sunset = models.DateTimeField(blank=True, null=True)
    pressure = models.IntegerField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)
    temp_feels = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    detail_desc = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CityWeatherForecast(models.Model):
    id = models.AutoField(primary_key=True)
    data_dt = models.DateTimeField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temp_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temp_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    simple_desc = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
