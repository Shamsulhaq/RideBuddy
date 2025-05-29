import csv
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import TypeGroup, TypeValue, TypeGroupName, Country, Region, City, License

User = get_user_model()

data = [
    {'name':TypeGroupName.LICENSE_TYPE, 'values': ["Freezone", "Mainland", "Offshore"]},
    {'name':TypeGroupName.LOCATION_TYPE, 'values': ["Location", "Complex"]},
    {'name':TypeGroupName.LOCATION_AMENITIES, 'values': ["Petrol Station", "Metro Station", "Bus Station", "Mall", "Park"]},
    {'name':TypeGroupName.ASSET_TYPE, 'values':["Building", "Villa", "Land", "Warehouse", "Parking", "Factory", "Farm", "Petrol Station", "Townhouse"]},
    {'name':TypeGroupName.ASSET_SUB_TYPE, 'values':["Labour Camp (Building)", "Mall (Building)", "Hospital", "Clinic (Building or Villa)", "Sports Club", "Hotel", "Staff Accommodation"]},
    {'name':TypeGroupName.ASSET_AMENITIES, 'values':["Security Rooms", "Loading Docks", "Rooms", "Garbage Rooms", "Fire Hose Reel", "Podium Parking", "Basement Parking", "Automated Parking System", "Lobby", "Domotic System", "Emergency Lightning System", "First Aid Rooms", "Parking", "Visitor Parking", "Free Visitor Parking", "Allocated Car Parking", "Labour Service Rooms", "Sprinkler System", "Garden", "Service Blocks", "Supervisor Rooms", "Built-in Sound System", "Plate Recognition System", "Coffee Shop", "Fire Fighting System", "Laundry Services", "Childcare Facilities", "Secure Lockers", "Concierge Services", "Business Lounge", "Medical and Wellness Facilities", "Pick Up and Drop Off Area", "Bus Parking", "Ablution Rooms", "Prayer Rooms", "Stand Alone Property", "On Main Road", "Corner Plot", "Street Facing", "Server Rooms", "Face Recognition Gates", "Outdoor Seating Area", "Multilingual Staff", "Coworking Space", "Pet Friendly", "Walking Distance from Metro Station", "Walking Distance from Bus Station", "Fully Fenced Property", "Bike Parking", "Bicycle Parking", "Lifts", "Upgraded / Renovated", "Brand New / Never Occupied", "Solar Roof Panelling", "Swimming Pool", "Connected to Utility Services", "Service Lift", "Professionally Managed", "Floor to Ceiling Windows", "Maintenance Contract", "Car Wash Services", "Wet Pantry / Kitchen", "Cleaning & Maintenance Services", "Meeting Rooms", "Printing & Copying Machines", "Adjacent to Public Parking", "Security Gates", "Balconies / Terrasses", "Interlocked Parking", "CCTV", "Electric Vehicle Chargers", "People of Determination Parkings", "Covered Car Parking", "Ground Floor Parking", "Security On Site", "Toilets", "Bathrooms", "Washrooms", "Commercial Kitchen", "Dry Pantry / Kitchen", "Valet Parking", "Helipad", "Storage Rooms", "ATM", "Smart Lifts", "Conference Facilities", "Video Conference System", "24 Hour Access", "IT Support", "Break Out Areas", "Trolley Bus Services", "HealthClub / Gymnasium", "Tenant Benefit Package", "Fire Alarm", "Gated Property", "Built-in Showers", "Board / Conference Rooms", "Door Access Control System", "Dining Options", "Back Up Power System", "Catering Services", "High Speed Internet & Wifi", "Mosque", "Telephone Rooms", "Dining Halls", "Laundry Rooms", "Industrial Lift", "Loading Ramps", "Overhead Crane", "Insulated", "Mezzanine", "Open Sided Warehouse / Shed", "Sliding Doors", "Compacted Yard", "Automated Sectional Doors", "Roller Shutter Doors", "Sunken Loading", "Dock Shelters", "Hydraulic Dock Levelers", "Substation / Power Transformers", "VNA Racking System", "Drive-In", "Racking System", "Maid Rooms", "Open Space Area", "Chilled Store", "Frozen Store", "Dry Store"]},
    {'name':TypeGroupName.UNIT_TYPE, 'values':["Office Space", "Serviced Office", "Business Centre", "Retail Space", "Meeting Room", "Parking Space", "Storage Space", "Workshop", "Showroom", "Clinic", "Hotel Apartment", "Shop", "HealthClub / Gymnasium", "Hotel Room"]},
    {'name':TypeGroupName.UNIT_SUB_TYPE, 'values':["Internal (Serviced Office)", "External (Serviced Office)", "Virtual", "Desk", "Office Suite", "Full Floor (Office Space)", "Half Floor", "Combined Units", "Duplex (Hotel Apartment)"]},
    {'name':TypeGroupName.UNIT_AMENITIES, 'values':["Private Lift", "Reception", "Domotic System", "First Aid Rooms", "Visitor Parking", "Free Visitor Parking", "Allocated Car Parking", "Built-in Sound System", "Coffee Shop", "Secure Lockers", "Prayer Rooms", "Business Lounge", "On Main Road", "Street Facing", "Server Rooms", "Outdoor Seating Area", "Multilingual Staff", "Coworking Space", "Upgraded / Renovated", "Brand New / Never Occupied", "Swimming Pool", "Professionally Managed", "Floor to Ceiling Windows", "Wet Pantry / Kitchen", "Cleaning & Maintenance Services", "Meeting Rooms", "Printing & Copying Machines", "Balconies / Terrasses", "CCTV", "Toilets", "Bathrooms", "Dry Pantry / Kitchen", "Storage Rooms", "Conference Facilities", "Video Conference System", "24 Hour Access", "IT Support", "Break Out Areas", "Tenant Benefit Package", "Built-in Showers", "Board / Conference Rooms", "Door Access Control System", "Catering Services", "High Speed Internet & Wifi", "Telephone Rooms", "Mezzanine", "Security On Site", "Garden", "Open Space Area", "Maid Room", "Multimedia Equipments", "Manager Rooms", "Meeting Rooms", "Hot Desks", "Postal Address", "Answering Machines", "Rental Pool Option", "PRO Services", "Unlimited Tea & Coffee", "Administrative Support", "Global Network"]},
    {'name':TypeGroupName.FURNITURE_TYPE, 'values':["Unfurnished", "Fully Furnished", "Partly Furnished", "Brand New Furniture", "Only Kitchen Appliances"]},
    {'name':TypeGroupName.PAYMENT_TERMS, 'values':["Annually", "Bi-Annually", "Quarterly", "Monthly", "Daily", "Hourly"]},
    {'name':TypeGroupName.MINIMUM_LEASING_PERIOD, 'values':["1 Hour", "1 Day", "1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "3 Years", "5 Years"]},
    {'name':TypeGroupName.FLOORING_TYPE, 'values':["Carpet", "Carpet Tiles", "Hardwood", "Vinyl Flooring", "Ceramic Tiles", "Marble Tiles", "Concrete", "Laminate"]},
    {'name':TypeGroupName.AIR_CONDITIONING_SYSTEM, 'values':["Portable or Mobile Conditioners", "Under Floor System", "Split / Multi Split System"]},
    {'name': TypeGroupName.FUNCTION, 'values': ["Residential", "Office", "Industrial", "Retail", "Hospitality"]},
    {'name': TypeGroupName.STATUS, 'values': ["Completed", "Structurally Topped Out", "Under Construction", "Proposed", "On Hold", "Never Completed", "Vision", "Canceled", "Under Renovation", "Renovated", "Under Demolition", "Demolished"]},
    {'name': TypeGroupName.SUB_STATUS, 'values': ["Ready Secondary", "Under Construction Secondary", "Ready Primary", "Under Construction Primary"]},
    {'name': TypeGroupName.LAND_TYPE, 'values': ["Residential", "Agricultural", "Industrial", "Commercial", "Public Facilities", "Government Authority"]},
    {'name': TypeGroupName.TRANSACTION_TYPE, 'values': ["Buy", "Rent", "Lease to Own"]},
    {'name':TypeGroupName.TYPE_OF_CERTIFICATION, 'values':["BREEAM (Building Research Establishment Environmental Assessment Method)", "LEED (Leadership in Energy and Environmental Design)", "WELL"]},
    {'name':TypeGroupName.CERTIFICATION_RATINGS, 'values':["Outstanding", "Excellent", "Very Good", "Good", "Pass", "Unclassified", "Platinum", "Gold", "Silver", "Certified", "Platinum", "Gold", "Silver"]},
    {'name':TypeGroupName.INDUSTRY, 'values':["Legal", "Maintenance", "Finance", "Logistics", "Real Estate", "Construction", "Office Equipment & Others"]},
    {'name':TypeGroupName.SPECIALTY, 'values':["Contract Drafting", "Conveyancing", "Insurance", "Medical Insurance", "Company Setup", "PRO Services", "Lawyer Representation / Power Of Attorney", "Carpentry", "Cleaning", "Electrical", "Mechanical", "Plumbing", "Painting", "Pest Control", "Air Conditioning", "Swimming Pool", "Security", "Landscaping", "Facility Management", "Rope Access", "Mortgage", "Escrow Services", "Accounting & Bookkeeping", "Tax Consultancy", "Auditing", "Banks", "Storage", "Car Maintenance", "Car Rentals", "Packers and Movers", "Events", "Shipping", "Trustee Offices", "Valuation / Surveyors", "Photographer", "Commercial Brokerage", "Residential Brokerage", "Property Management", "Ejari Registration", "Project Manager", "Interior Design", "Fit Out", "Architect", "Furniture", "Art Galleries", "IT", "Telecommunication", "Copy & Print Center", "Laundry", "Digital Agency", "Typing Center", "Business Centre Corporate", "Developer / Owner"]},
    {'name':TypeGroupName.FLOOR_TYPE, 'values':["Low Floor", "Mid Floor", "High Floor", "Super High Floor"]},
    {'name':TypeGroupName.VIEW_TYPE, 'values':["Landmark", "Water", "Community", "Panoramic", "360°", "Green Spaces"]},
    {'name':TypeGroupName.VILLA_TYPE, 'values':["1 Bedroom", "2 Bedrooms", "3 Bedrooms", "4 Bedrooms", "5 Bedrooms", "6 Bedrooms"]},
    {'name':TypeGroupName.TOWNHOUSE_TYPE, 'values':["1 Bedroom", "2 Bedrooms", "3 Bedrooms", "4 Bedrooms", "5 Bedrooms"]},
    {'name':TypeGroupName.PARTITION_TYPE, 'values':["Gypsum", "Wood", "Glass"]},
    {'name':TypeGroupName.SERVICED_OFFICES_TYPE, 'values':["Internal", "External", "Office Suites"]},
    {'name':TypeGroupName.HOTEL_APARTMENTS_UNITS_TYPE, 'values':["Studio", "1 Bedroom", "2 Bedrooms", "3 Bedrooms", "4 Bedrooms", "5 Bedrooms"]},
    {'name':TypeGroupName.RESIDENTIAL_UNITS_TYPE, 'values':["Studio", "1 Bedroom", "2 Bedrooms", "3 Bedrooms", "4 Bedrooms", "5 Bedrooms"]},   
    {'name':TypeGroupName.FIT_OUT_TYPE, 'values':["Shell and Core", "Semi Fitted", "Fitted", "Fully Fitted"]},   
]

created_data = {'created_by': User.objects.get(id=1), 'created_on': timezone.now()}

def type_migrate():
    for d in data:
        group, created = TypeGroup.objects.get_or_create(**created_data, name=d['name'])
        for i in d['values']:
            value, created = TypeValue.objects.get_or_create(**created_data, group=group, name=i)
            print(f'created Done {group.name} - value {value.name}')

        
countries = [
    {'name': 'United Arab Emirates',
     'code': 'UAE',
     'phone_number_code': 971,
     'vat_rate': 5,
     'currency': 'AED',
     'regions':[
         {'name': 'Emirate of Dubai',
          'housing_fees': 2.5,
          'cities':['Dubai']
          },
         {'name': 'Emirate of Abu Dhabi',
          'housing_fees': 5,
          'cities':['Abu Dhabi']
          },
         {'name': 'Emirate of Ajman',
          'housing_fees': 5,
          'cities':['Ajman']
          },
         {'name': 'Emirate of Fujairah',
          'housing_fees': 5,
          'cities':['Fujairah']
          },
         {'name': 'Emirate of Ras Al Khaimah',
          'housing_fees': 5,
          'cities':['Ras Al Khaimah']
          },
         {'name': 'Emirate of Sharjah',
          'housing_fees': 5,
          'cities':['Sharjah']
          },
         {'name': 'Emirate of Umm Al Quwain',
          'housing_fees': 5,
          'cities':['Umm Al Quwain']
          }
     ]
     },
    {'name': 'Saudi Arabia',
     'code': 'SA',
     'phone_number_code': 966,
     'vat_rate': 10,
     'currency': 'SAR',
     'regions':[
         {'name': 'Central',
          'housing_fees': 0,
          'cities':['Djeddah']
          }
     ]
     }
]

def country_migration():
    for c in countries:
        country, created = Country.objects.get_or_create(**created_data,
                                                         name=c['name'],
                                                         code=c['code'],
                                                         phone_number_code=c['phone_number_code'],
                                                         vat_rate=c['vat_rate'],
                                                         currency=c['currency']
                                                         )
        for r in c['regions']:
            region, created = Region.objects.get_or_create(**created_data,
                                                           name=r['name'],
                                                           housing_fees=r['housing_fees'],
                                                           country=country)
            for ci in r['cities']:
                city, created = City.objects.get_or_create(**created_data,
                                                           name=ci,
                                                           region=region)
                

def percentage_migrate():
    data = [
        {'name': TypeGroupName.TRANSFER_FEES,
         'values':[
                {
                    'name':'Dubai Land Department',
                    'percentage': 4
                },
                {
                    'name':'DiFC',
                    'percentage': 5
                }
            ]
         
        },
        {'name': TypeGroupName.SUBLEASE_TAX, 'values':[
            {
                'name':'10%',
                'percentage': 10
            },
            {
                'name':'15%',
                'percentage': 15
            },
            {
                'name':'20%',
                'percentage': 20
            },
        ]
        },
    ]
    
    for d in data:
        group, created = TypeGroup.objects.get_or_create(**created_data, name=d['name'])
        for i in d['values']:
            value, created = TypeValue.objects.get_or_create(**created_data, group=group, name=i['name'], percentage=i['percentage'])
            print(f'created Done {group.name} - value {value.name}')

        
def import_license():  
    settings.BASE_DIR
    file_path=f"{settings.BASE_DIR}/migrations_files/license.csv"
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader, start=1):  # Keep track of row numbers
            try:
                name = row['License_Name']
                license_id = row['License_ID']
                previous_name = row['Previous_Name']
                if row['License_Type']:
                    try:
                       license_type = TypeValue.objects.get(group__name=TypeGroupName.LICENSE_TYPE, name=row['License_Type'])
                    except Exception as e:
                        print("License Type",e)
                description = row['Description']
                launched_in = row['Launched_In']
                if row['Country']:
                    try:
                        country = Country.objects.get(name=row['Country'])
                    except Exception as e:
                        print("Country ",e)    
                if row['Region']:
                    try:
                        region = Region.objects.get(name=row['Region'])
                    except Exception as e:
                        print("Region ",e) 
                        
                video_link = row['Video_Link']
                license_icon = row['License_Icon']
                location_map = row['Location_Map']
                is_live = row['Live']
                is_featured = row['Featured']
                obj, created = License.objects.get_or_create(
                    **created_data,
                    name=name,
                    country=country,
                    region=region,
                    license_id=license_id,
                    previous_name=previous_name,
                    license_type=license_type,
                    description=description,
                    video_link=video_link,
                    is_live=is_live,
                    is_featured=is_featured
                )
                    
                if created:
                    print(f"Imported License for {row['License_Name']} successfully.")
     
                else:
                    print(f"{row['License_Name']} is already in DB")
            except Exception as e:
                print(f"Error in row {index}: {e}")

        
   