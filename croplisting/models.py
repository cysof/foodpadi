from django.db import models
from accounts.models import FarmPadiUser
from django.core.exceptions import ValidationError

class CropListing(models.Model):
    farmer = models.ForeignKey(FarmPadiUser, on_delete=models.CASCADE, related_name='crop_listings')
    crop_name = models.CharField(max_length=250)
    crop_description = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField(default=0) 
    unit = models.CharField(max_length=100, help_text="eg: kg, bags")
    location = models.CharField(max_length=250)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    harvested_date = models.DateField(help_text="what is the date you harvested your crop")
    img = models.ImageField(upload_to='cropImage/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        """
        Return a string representation of the CropListing model instance.
        
        The string representation should include the farmer's name and the crop name.
        """
        return f'{self.farmer} {self.crop_name}'

    def clean(self):
        """Validate that only farmers can create crop listings"""
        if self.farmer and self.farmer.account_type != 'FARMER':
            raise ValidationError("Only users with Farmer account type can create crop listings")
    
    def save(self, *args, **kwargs):
        """
        Validate the CropListing model instance before saving to the database.
        
        The clean() method is called to validate that only farmers can create crop listings.
        """
        self.clean()
        super().save(*args, **kwargs)