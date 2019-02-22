from django.db import models
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["destination"]) < 3:
            errors["destination"] = "Destination should be at least 3 character."
        if len(postData["plan"]) < 3:
            errors["plan"] = "Description should be at least 3 characters."
        start_date = datetime.strptime(postData["start_date"], '%Y-%m-%d')
        end_date = datetime.strptime(postData["end_date"], '%Y-%m-%d')
        recent_date = datetime.now()
        if start_date < recent_date:
            errors["start_date"] = "Start date should be in the furture"
        if end_date < start_date:
            errors["end_date"] = "End date should not be before the start date."

        # release_date = datetime.strptime(postData["release_date"], '%Y-%m-%d')
        # recent_date = datetime.now()
        # if release_date > recent_date:
        #     errors["release_date"] = "Release date should be in the past"
        # if len(self.filter(title=postData["title"])) > 0:
        #     errors["existed"] = "This  title already existed!"
        return errors

# Create your models here.


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    user_created_by = models.ForeignKey(
        "login_app.User", related_name="created_trips")
    users_who_joined = models.ManyToManyField(
        "login_app.User", related_name="joined_trips")
    plan = models.TextField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()
