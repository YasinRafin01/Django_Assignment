import re
import json
import requests
from django.core.management.base import BaseCommand
from Hotel_info.models import Property, Amenity

class Command(BaseCommand):
    help = 'Update amenities from Trip.com website'

    def handle(self, *args, **options):
        url = 'https://uk.trip.com/hotels/?locale=en-GB&curr=USD#ctm_ref=ih_h_6_1'

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Referer': 'https://uk.trip.com/',
            'X-Requested-With': 'XMLHttpRequest'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching data: {str(e)}'))
            return

        # Debugging: Print a portion of the response text to inspect it
        #print(response.text[:5000])  # Print the first 500 characters of the response
        
        try:
            # Use regular expression to match the JSON part
            match = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', response.text, re.DOTALL)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
            else:
                self.stdout.write(self.style.ERROR('Unable to locate JSON data'))
                return

        except (ValueError, json.JSONDecodeError) as e:
            self.stdout.write(self.style.ERROR(f'Error extracting or parsing JSON: {str(e)}'))
            return



        # Process each property in the JSON data
        #print(data)
        all_sections = ['inboundCities', 'outboundCities', 'fiveStarHotels', 'cheapHotels', 'hostelHotels']
        hotels_data = data['initData']['htlsData']
        for section in all_sections:
            if section in hotels_data:
                self.process_section(hotels_data[section], section)
            else:
                self.stdout.write(f"Section {section} not found in the data.")

    def process_section(self, section_data, section_name):
        self.stdout.write(f"Processing section: {section_name}")
        if section_name in ['inboundCities', 'outboundCities']:
            for city in section_data:
                city_name = city.get('name', 'Unknown City')
                for hotel in city.get('recommendHotels', []):
                    self.extract_hotel_info(hotel, city_name, section_name)
        else:
            for hotel in section_data:
                self.extract_hotel_info(hotel, 'N/A', section_name)

    def extract_hotel_info(self, hotel, city_name, section_name):
        hotel_data = {
            'hotel_id': hotel.get('hotelId'),
            'hotelFacilityList':hotel.get('hotelFacilityList')
        }
        # print("--------------------------------------")
        # print(hotel_data)

        try:
            # Fetch the property by hotel_id
            property = Property.objects.get(property_id=hotel_data['hotel_id'])

            # Extract the amenities from the hotelFacilityList
            amenities = [facility['name'] for facility in hotel_data['hotelFacilityList']]
            print(f"Processing amenities for hotel ID {hotel_data['hotel_id']}: {amenities}")

            # Add each amenity to the property
            for amenity_name in amenities:
                amenity, created = Amenity.objects.get_or_create(name=amenity_name)
                property.amenities.add(amenity)

            self.stdout.write(self.style.SUCCESS(f'Updated amenities for {property.title}'))
        except Property.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"Property with ID {hotel_data['hotel_id']} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing property {hotel_data["hotel_id"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Finished updating amenities'))



        # print(hotel_data['hotelId'])
        # for data in hotel_data:
        #     try:
        #         property = Property.objects.get(property_id=data['hotel_id'])

        #         amenities = data['brief']
        #         print(amenities)
        #         for amenity_name in amenities:
        #             amenity, created = Amenity.objects.get_or_create(name=amenity_name)
        #             property.amenities.add(amenity)
        #         self.stdout.write(self.style.SUCCESS(f'Updated amenities for {property.title}'))
        #     except Property.DoesNotExist:
        #         self.stdout.write(self.style.WARNING(f"Property with ID {data['hotel_id']} not found"))
        #     except Exception as e:
        #         self.stdout.write(self.style.ERROR(f'Error processing property {data.get('hotel_id', 'unknown')}: {str(e)}'))


        # self.stdout.write(self.style.SUCCESS('Finished updating amenities'))