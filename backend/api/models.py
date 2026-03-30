from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    calories_per_100g = models.FloatField()
    grams_per_unit = models.FloatField(null=True, blank=True)   
    default_unit = models.CharField(max_length=50, null=True, blank=True)  


    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories_per_100g} cal/100g)"