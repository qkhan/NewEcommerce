from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator
import random
import os

def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    print ("models.py|Base Name: %s"%(basename))
    name, ext = os.path.splitext(basename)
    return name, ext

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,38787873899)
    print ("models.py|File Name Received: %s"%(filename))
    name, ext = get_filename_ext(filename)
    print("Models.py|Name:%s -- EXT:%s",name, ext)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,
                                                 ext=ext)
    print("Models.py|Final File Name:%s"%(final_filename))

    print("Models.py|products/{new_filename}/{final_filename}".format(
                     new_filename=new_filename,
                     final_filename=final_filename
                 ))
    return "products/{new_filename}/{final_filename}".format(
                         new_filename=new_filename,
                         final_filename=final_filename
                     )


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query)|
                Q(description__icontains=query)|
                Q(price__icontains=query)|
                Q(tag__title__icontains=query)|
                Q(tag__slug__icontains=query)
                )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):


    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def features(self):
        return self.get_queryset().featured()

    def search(self, query):
        return self.get_queryset().active().search(query)

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}".format(slug=self.slug)
        return reverse("product:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return ("[%s] %s"%(self.id, self.title))

    def __unicode__(self):
        return ("[%s] %s"%(self.id, self.title))

    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
