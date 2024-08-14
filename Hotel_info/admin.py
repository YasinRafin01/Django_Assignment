from django.contrib import admin
from .models import Location,Amenity,Property,PropertyImage

# Register your models here.
# admin.site.register(Location)
# admin.site.register(Amenity)
# admin.site.register(Property)
# admin.site.register(PropertyImage)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'caption')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    search_fields = ('property_id', 'title', 'description')
    filter_horizontal = ('locations', 'amenities')
    inlines = [PropertyImageInline]

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image', 'caption')
    list_filter = ('property',)
    search_fields = ('property__title', 'caption')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
