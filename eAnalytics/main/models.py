from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                verbose_name='Прошёл активацию?')
    send_notifications = models.BooleanField(default=True,
        verbose_name='Отправлять уведомления о новых комментариях?')
    
    class Meta(AbstractUser.Meta):
        pass