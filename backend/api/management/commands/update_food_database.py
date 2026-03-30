"""
Django management command to update the food database with extracted data.
Usage: python manage.py update_food_database
"""

from django.core.management.base import BaseCommand
from api.models import Food
import json
import os

DEFAULT_GRAMS_PER_UNIT = 100.0
DEFAULT_UNIT = 'serving'

class Command(BaseCommand):
    help = 'Update food database with extracted Nigerian food data'

    def handle(self, *args, **options):
        # Load extracted food data
        json_path = '/app/extracted_foods.json'
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR('extracted_foods.json not found. Run extract_food_data.py first.'))
            return
        
        with open(json_path, 'r') as f:
            new_foods = json.load(f)
        
        # Get current database state
        existing_foods = {food.name.lower(): food for food in Food.objects.all()}
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write("FOOD DATABASE UPDATE REPORT")
        self.stdout.write(f"{'='*60}\n")
        self.stdout.write(f"Current database: {len(existing_foods)} foods")
        self.stdout.write(f"New data source: {len(new_foods)} foods\n")
        
        added_count = 0
        updated_count = 0
        skipped_count = 0
        
        foods_to_create = []
        
        for food_name, food_data in new_foods.items():
            food_name_lower = food_name.lower()
            
            if food_name_lower in existing_foods:
                # Food exists - check if we should update
                existing_food = existing_foods[food_name_lower]
                
                # Only update if new data seems more accurate
                if food_data['calories_per_100g'] != existing_food.calories_per_100g:
                    self.stdout.write(
                        f"  [UPDATE] {food_name}: "
                        f"{existing_food.calories_per_100g} → {food_data['calories_per_100g']} cal/100g"
                    )
                    existing_food.calories_per_100g = food_data['calories_per_100g']
                    existing_food.save()
                    updated_count += 1
                else:
                    skipped_count += 1
            else:
                # New food - add it
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  [NEW] {food_name}: {food_data['calories_per_100g']} cal/100g"
                    )
                )
                foods_to_create.append(
                    Food(
                        name=food_name,
                        calories_per_100g=food_data['calories_per_100g'],
                        grams_per_unit=food_data.get('grams_per_unit', DEFAULT_GRAMS_PER_UNIT),
                        default_unit=food_data.get('default_unit', DEFAULT_UNIT),
                    )
                )
                added_count += 1
        
        # Bulk create new foods
        if foods_to_create:
            Food.objects.bulk_create(foods_to_create)
        
        # Final report
        new_total = Food.objects.count()
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(self.style.SUCCESS("✓ Update Complete!"))
        self.stdout.write(f"{'='*60}\n")
        self.stdout.write(f"  Added: {added_count} new foods")
        self.stdout.write(f"  Updated: {updated_count} existing foods")
        self.stdout.write(f"  Skipped: {skipped_count} (already accurate)")
        self.stdout.write(f"\n  Database total: {new_total} foods (was {len(existing_foods)})\n")
