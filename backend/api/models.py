from django.db import models

class Food(models.Model):
    """
    Represents a standard nutritional entry in the Nigerian food database.
    
    This model stores the baseline caloric density and standard measurement 
    weights used by the calculation engine to standardize user logs.
    """
    name = models.CharField(
        max_length=100, 
        unique=True, 
        db_index=True,
        help_text="The unique name of the food item (e.g., 'jollof rice')."
    )
    calories_per_100g = models.FloatField(
        help_text="The energy content in kilocalories for 100 grams of this food."
    )
    grams_per_unit = models.FloatField(
        null=True, 
        blank=True,
        help_text="The average weight in grams for a single standard unit (e.g., 1 wrap)."
    )   
    default_unit = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        help_text="The common measurement unit for this food (e.g., 'wrap', 'piece')."
    )  

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories_per_100g} kcal/100g)"