from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.
class Folder(models.Model):
    
    name = models.CharField(max_length=250)
    parent = models.ForeignKey("self", related_name='sub_folders' ,on_delete=models.CASCADE)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_delete = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, related_name='folder_deleter', on_delete=models.CASCADE, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_delete:
            self.deleted_by = kwargs.get('deleted_by', None)
            self.deleted_at = timezone.now()
        super().save(*args, **kwargs)
    
class Document(models.Model):
    name = models.CharField(max_length=250)
    library_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='documents')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_delete = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, related_name='document_deleter', on_delete=models.CASCADE, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.is_delete:
            self.deleted_by = kwargs.get('deleted_by', None)
            self.deleted_at = timezone.now()
        super().save(*args, **kwargs)

    
    