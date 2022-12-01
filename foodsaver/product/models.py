from django.db import models
from django.conf import settings
from django.urls import reverse
# Handling Image resizing
from io import BytesIO
from PIL import Image
# Thumbnails
from django.core.files import File

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=255, default="lb")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    
    class Meta:
        ordering = ('-date_added',) # descending order
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.slug and self.category:
            return f'/{self.category.slug}/{self.slug}/'
        return ''
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        elif self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            self.save()
            return 'http://127.0.0.1:8000' + self.thumbnail.url
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def get_vendor_name(self):
        if self.vendor:
            return self.vendor.get_username()
        return ''