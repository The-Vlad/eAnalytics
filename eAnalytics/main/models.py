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

class Connection(models.Model):
    CONNECTION_TYPE_CHOICES = [
        ('CSV', 'CSV file'),
        ('PG', 'PostgreSQL'),
    ]

    user_id = models.ForeignKey('AdvUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=45, null=False)
    connection_type = models.CharField(max_length=10, choices=CONNECTION_TYPE_CHOICES, default='CSV')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-datetime']
        db_table = 'connections'
        verbose_name = 'подключение'
        verbose_name_plural = 'подключения'
    
    def __str__(self):
        return str(self.name)

class CSV_File(models.Model):
    file = models.FileField(upload_to='csv_files')
    connection_id = models.ForeignKey('Connection', on_delete=models.CASCADE, null=False, default=1)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']
        db_table = 'csv_files'
        verbose_name = 'csv файл'
        verbose_name_plural = 'csv файлы'

    def __str__(self):
        return str(self.file)

