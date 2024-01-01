from django.db import models
from datetime import datetime, timezone

USER_ROLE = (
    ('user', 'User'),
    ('admin', 'Admin'),
)

USER_GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('unknown', 'Unknown'),
)

USER_STATUS = (
    ('pending', 'Pending'),
    ('activated', 'Activated'),
    ('disabled', 'Disabled'),
)

class ExternalUser(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    fullName = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLE, default="user")
    gender = models.CharField(max_length=20, choices=USER_GENDER, default="unknown")
    birthday = models.DateTimeField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=USER_STATUS, default="pending")
    password = models.CharField(max_length=255)
    versionKey = models.IntegerField(default=0)

    # Auto-set the field on creation and update.
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    createdBy = models.TextField(null=True, blank=True)
    updatedBy = models.TextField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        if '__v' in kwargs:
            kwargs['versionKey'] = kwargs.pop('__v')
        if '_id' in kwargs:
            kwargs['id'] = kwargs.pop('_id')
        super(ExternalUser, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'external-users'

    def __str__(self):
        if self.email:
            return f"{self.fullName} - {self.email}"
        return self.fullName

    def to_dict(self):
        birthday_string = None
        if self.birthday:
            birthday_string = self.birthday.strftime('%Y-%m-%d')
        return {
            "fullName": self.fullName,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "gender": self.gender,
            "image": self.image,
            "thumbnail": self.thumbnail,
            "birthday": birthday_string,
            "password": self.password,
            "status": self.status,
        }
