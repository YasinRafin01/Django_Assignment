from django.db import models

class Location(models.Model):
    '''
    this is the location model for storing hotel name, in which origin it is situated, latitude and longitude
    '''

    name = models.CharField(max_length=1000)
    type = models.CharField(null=True,blank=True,max_length=500, choices=[
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ])
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Amenity(models.Model):
    '''
    this model has primarily nothing to fetch from scrapy project database but admin can insert by logging into admin panel, this has a many to many relation with Property
    '''
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Property(models.Model):
    '''
    this model is the main Property model which describe hotel_id, hotel_name, hotel description, location of the hotel etc.
    '''

    property_id = models.CharField(max_length=150, unique=True)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    locations = models.ManyToManyField(Location)
    amenities = models.ManyToManyField(Amenity)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

def property_image_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/property_images/<property_id>/<filename>
    return f'property_images/{instance.property.property_id}/{filename}'

class PropertyImage(models.Model):
    '''
    this is the image model where the images path are stored
    '''

    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=property_image_path)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.property.title}"