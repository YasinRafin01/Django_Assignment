import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from Hotel_info.models import Property, PropertyImage, Location
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(String, unique=True)
    hotel_name = Column(String)
    hotel_url = Column(String)
    hotel_location = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    image_url = Column(String)
    price = Column(Float)
    city = Column(String)
    section = Column(String)


def download_image(url):
    '''
    this function is used for handling downloading images
    '''
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            temp_file = NamedTemporaryFile(delete=True)
            temp_file.write(response.content)
            temp_file.flush()
            return temp_file
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None


class Command(BaseCommand):
    help = 'Migrate data from Scrapy project database to Django'

    def handle(self, *args, **kwargs):
        '''
        this function maps between the database tables of scrapy project and Django project

        '''

        # Connect to Scrapy database
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch data from Scrapy database
        hotels = session.query(Hotel).all()

        for hotel in hotels:
            # Create or update Property object
            property, created = Property.objects.update_or_create(
                property_id=hotel.hotel_id,
                defaults={
                    'title': hotel.hotel_name,
                    'description': hotel.hotel_url,  # Using hotel_url as description for now
                }
            )

            # Create and associate Location object
            if hotel.hotel_location:
                location, _ = Location.objects.get_or_create(
                    name=hotel.hotel_location,
                    defaults={
                        'type': 'city',
                        'latitude': hotel.latitude if hotel.latitude is not None else 0,
                        'longitude': hotel.longitude if hotel.longitude is not None else 0,
                    }
                )
                property.locations.add(location)

            # Create PropertyImage object
            if hotel.image_url:
                # Prepend the base URL to the image URL
                full_image_url = f"https://ak-d.tripcdn.com/images{hotel.image_url}"
                
                temp_file = download_image(full_image_url)
                if temp_file:
                    file_name = os.path.basename(full_image_url)
                    property_image, created = PropertyImage.objects.get_or_create(
                        property=property,
                        defaults={'image': File(temp_file, name=file_name)}
                    )
                    if not created:
                        property_image.image.save(file_name, File(temp_file), save=True)
                    temp_file.close()


            self.stdout.write(self.style.SUCCESS(f'Migrated hotel: {hotel.hotel_name}'))

        session.close()
        self.stdout.write(self.style.SUCCESS('Successfully migrated data from Scrapy to Django'))