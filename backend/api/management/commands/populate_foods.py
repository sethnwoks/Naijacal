from django.core.management.base import BaseCommand
from api.models import Food

DEFAULT_GRAMS_PER_UNIT = 100.0
DEFAULT_UNIT = 'serving'

CALORIE_DATABASE = {
    # Swallows & Staples
    'eba': {'calories_per_100g': 360, 'unit': 'g'},  # Updated for accuracy
    'fufu': {'calories_per_100g': 180, 'unit': 'g'},
    'amala': {'calories_per_100g': 250, 'unit': 'g'},
    'pounded yam': {'calories_per_100g': 267, 'unit': 'g'},  # Updated
    'semovita': {'calories_per_100g': 600, 'unit': 'g'},  # Updated (was 107)
    'tuwo masara': {'calories_per_100g': 450, 'unit': 'g'}, # New
    'lafun': {'calories_per_100g': 357, 'unit': 'g'},
    'yam flour': {'calories_per_100g': 356, 'unit': 'g'},
    'plantain flour': {'calories_per_100g': 350, 'unit': 'g'},
    'cassava flour': {'calories_per_100g': 160, 'unit': 'g'},
    'wheat flour': {'calories_per_100g': 455, 'unit': 'g'},
    'oat flour': {'calories_per_100g': 404, 'unit': 'g'},
    'semolina': {'calories_per_100g': 360, 'unit': 'g'},
    'fonio': {'calories_per_100g': 360, 'unit': 'g'},
    'sorghum': {'calories_per_100g': 329, 'unit': 'g'},
    'millet': {'calories_per_100g': 378, 'unit': 'g'},
    'maize': {'calories_per_100g': 365, 'unit': 'g'},
    'maize flour': {'calories_per_100g': 365, 'unit': 'g'},
    'barley': {'calories_per_100g': 354, 'unit': 'g'},
    'teff': {'calories_per_100g': 367, 'unit': 'g'},
    'quinoa': {'calories_per_100g': 368, 'unit': 'g'},
    'rice flour': {'calories_per_100g': 366, 'unit': 'g'},
    'ofada rice': {'calories_per_100g': 360, 'unit': 'g'},
    'white rice': {'calories_per_100g': 130, 'unit': 'g'},
    'brown rice': {'calories_per_100g': 112, 'unit': 'g'},
    'basmati rice': {'calories_per_100g': 121, 'unit': 'g'},
    
    # Dishes
    'jollof rice': {'calories_per_100g': 130, 'unit': 'g'},
    'fried rice': {'calories_per_100g': 150, 'unit': 'g'},
    'moi moi': {'calories_per_100g': 200, 'unit': 'g'},
    'okpa': {'calories_per_100g': 216, 'unit': 'g'},
    'abacha': {'calories_per_100g': 367, 'unit': 'g'},
    'egusi soup': {'calories_per_100g': 593, 'unit': 'g'},
    'banga soup': {'calories_per_100g': 440, 'unit': 'g'},
    'ogbono soup': {'calories_per_100g': 400, 'unit': 'g'},
    'afang soup': {'calories_per_100g': 350, 'unit': 'g'},
    'efo riro': {'calories_per_100g': 300, 'unit': 'g'},
    'nsala soup': {'calories_per_100g': 450, 'unit': 'g'},
    'oha soup': {'calories_per_100g': 400, 'unit': 'g'},
    'okro soup': {'calories_per_100g': 105, 'unit': 'g'},  # Updated (was 250)
    'gbegiri soup': {'calories_per_100g': 200, 'unit': 'g'},
    'ewedu soup': {'calories_per_100g': 97, 'unit': 'g'},
    'ewa aganyin': {'calories_per_100g': 520, 'unit': 'g'}, # Added
    
    # Proteins & Meats
    'goat meat': {'calories_per_100g': 143, 'unit': 'g'},
    'beef': {'calories_per_100g': 250, 'unit': 'g'},
    'chicken': {'calories_per_100g': 239, 'unit': 'g'},
    'chicken breast': {'calories_per_100g': 165, 'unit': 'g'}, # New
    'chicken drumstick': {'calories_per_100g': 172, 'unit': 'g'}, # New
    'chicken thigh': {'calories_per_100g': 177, 'unit': 'g'}, # New
    'chicken liver': {'calories_per_100g': 173, 'unit': 'g'}, # New
    'chicken wings': {'calories_per_100g': 200, 'unit': 'g'}, # New
    'gizzard': {'calories_per_100g': 239, 'unit': 'g'}, # New
    'liver': {'calories_per_100g': 165, 'unit': 'g'}, # New
    'turkey': {'calories_per_100g': 135, 'unit': 'g'},
    'turkey breast': {'calories_per_100g': 135, 'unit': 'g'}, # New
    'snail': {'calories_per_100g': 90, 'unit': 'g'},
    'fish': {'calories_per_100g': 128, 'unit': 'g'},
    'prawn': {'calories_per_100g': 105, 'unit': 'g'}, # New
    'shrimp': {'calories_per_100g': 99, 'unit': 'g'}, # New
    'sardines': {'calories_per_100g': 208, 'unit': 'g'}, # New
    'crayfish': {'calories_per_100g': 280, 'unit': 'g'},
    'stockfish': {'calories_per_100g': 200, 'unit': 'g'},
    'suya': {'calories_per_100g': 250, 'unit': 'g'},
    'isi ewu': {'calories_per_100g': 300, 'unit': 'g'},
    
    # Snacks & Sides
    'kuli kuli': {'calories_per_100g': 500, 'unit': 'g'},
    'akara': {'calories_per_100g': 71, 'unit': 'g'}, # New
    'gala': {'calories_per_100g': 297, 'unit': 'g'}, # New
    'samosa': {'calories_per_100g': 80, 'unit': 'g'}, # New
    'puff puff': {'calories_per_100g': 150, 'unit': 'g'}, # New
    'meat pie': {'calories_per_100g': 300, 'unit': 'g'}, # New
    'egg roll': {'calories_per_100g': 250, 'unit': 'g'}, # New
    
    # Breads
    'white bread': {'calories_per_100g': 266, 'unit': 'g'},
    'whole wheat bread': {'calories_per_100g': 260, 'unit': 'g'},
    'banana bread': {'calories_per_100g': 326, 'unit': 'g'},
    'almond bread': {'calories_per_100g': 313, 'unit': 'g'},
    
    # Beans
    'beans': {'calories_per_100g': 127, 'unit': 'g'},
    
    # Oils & Nuts
    'groundnut oil': {'calories_per_100g': 884, 'unit': 'g'},
    'palm oil': {'calories_per_100g': 884, 'unit': 'g'},
    'groundnut': {'calories_per_100g': 567, 'unit': 'g'},
    'cashew nuts': {'calories_per_100g': 553, 'unit': 'g'},
    'almonds': {'calories_per_100g': 579, 'unit': 'g'},
    'walnuts': {'calories_per_100g': 654, 'unit': 'g'},
    'coconut': {'calories_per_100g': 660, 'unit': 'g'},
    'locust bean': {'calories_per_100g': 350, 'unit': 'g'}, # New
    
    # Tubers & Roots
    'yam': {'calories_per_100g': 116, 'unit': 'g'},
    'sweet potato': {'calories_per_100g': 86, 'unit': 'g'},
    'irish potato': {'calories_per_100g': 77, 'unit': 'g'},
    'cassava': {'calories_per_100g': 160, 'unit': 'g'},
    'coco yam': {'calories_per_100g': 168, 'unit': 'g'},
    
    # Vegetables
    'ugwu': {'calories_per_100g': 14, 'unit': 'g'}, # New
    'waterleaf': {'calories_per_100g': 20, 'unit': 'g'}, # New
    'bitter leaf': {'calories_per_100g': 25, 'unit': 'g'}, # New
    'uziza leaf': {'calories_per_100g': 30, 'unit': 'g'}, # New
    'utazi leaf': {'calories_per_100g': 28, 'unit': 'g'}, # New
    'carrot': {'calories_per_100g': 41, 'unit': 'g'},
    'cucumber': {'calories_per_100g': 16, 'unit': 'g'},
    'lettuce': {'calories_per_100g': 15, 'unit': 'g'},
    
    # Fruits
    'banana': {'calories_per_100g': 89, 'unit': 'g'},
    'orange': {'calories_per_100g': 47, 'unit': 'g'},
    'pineapple': {'calories_per_100g': 50, 'unit': 'g'},
    'pawpaw': {'calories_per_100g': 43, 'unit': 'g'},
    'mango': {'calories_per_100g': 60, 'unit': 'g'},
}

class Command(BaseCommand):
    help = "Load 101+ Nigerian foods into database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting food database population/update...")
        
        created_count = 0
        updated_count = 0
        
        for name, data in CALORIE_DATABASE.items():
            food, created = Food.objects.update_or_create(
                name=name,
                defaults={
                    "calories_per_100g": data["calories_per_100g"],
                    "grams_per_unit": data.get("grams_per_unit", DEFAULT_GRAMS_PER_UNIT),
                    "default_unit": data.get("default_unit", DEFAULT_UNIT),
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        self.stdout.write(
            self.style.SUCCESS(
                f"Sync Complete! Added {created_count} new, Updated {updated_count} existing. "
                f"Total in DB: {Food.objects.count()} foods."
            )
        )
