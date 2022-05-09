from django.db import models

from accounts.models import User

# Create your models here.
class Catalogue(models.Model):
    fcg = models.CharField(max_length=100)
    first = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    RAJ2000 = models.CharField(max_length=100)
    DEJ2000 = models.CharField(max_length=100)
    size_arcmin = models.DecimalField(max_digits=10, decimal_places=2)
    u_size = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100)
    grp = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    com = models.CharField(max_length=200)
    tno = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.fcg

class Label(models.Model):
    label = models.CharField(max_length=100)
    labelled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.labelled_by, self.catalogue)

