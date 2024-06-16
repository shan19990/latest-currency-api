from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone


# Create your models here.

class EmailModel(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class APIToken(models.Model):
    email = models.ForeignKey(EmailModel, on_delete=models.CASCADE)
    token = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    active = models.BooleanField()

    def __str__(self):
        return f"{self.email} - {self.active}"
    
# Signal receiver function
@receiver(post_save, sender=APIToken)
def deactivate_expired_tokens(sender, instance, created, **kwargs):
    if not created:
        if date.today() > instance.expiry_date:
            instance.active = False
            instance.save()

class DailyTokenUsage(models.Model):
    token = models.ForeignKey(APIToken, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    usage_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('token', 'date')
