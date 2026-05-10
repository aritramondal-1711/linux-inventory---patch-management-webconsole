from django.db import models

# Create your models here.
class linux_inventory(models.Model):
    servername=models.TextField()
    servergroup=models.TextField()
    os_version=models.TextField()
    uptime=models.TextField()

    def __str__(self):
        return self.servername
