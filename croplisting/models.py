from django.db import models
from accounts.models import FarmPadiUser
from django.core.exceptions import ValidationError

AVAILABILITY_CROP = (
    ('AVAILABLE', 'Available'),
    ('OUT OF STOCK', 'Out of Stock'),
)

class CropListing(models.Model):
    farmer = models.ForeignKey(FarmPadiUser, on_delete=models.CASCADE, related_name='crop_listings')
    crop_name = models.CharField(max_length=250)
    crop_description = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField(default=0) 
    unit = models.CharField(max_length=100, help_text="eg: kg, bags")
    location = models.CharField(max_length=250)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    harvested_date = models.DateField(help_text="what is the date you harvested your crop")
    is_Organic = models.BooleanField(default=True)
    availability = models.CharField(max_length=24, choices=AVAILABILITY_CROP, default='Available')
    img = models.ImageField(upload_to='cropImage/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        """
        Return a string representation of the CropListing model instance.
        
        The string representation should include the farmer's name and the crop name.
        """
     
        return f'{self.farmer.first_name} {self.farmer.last_name} - {self.crop_name}'
    
    @property
    def image_url(self):
        """Get the full Cloudinary URL for the image"""
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        return None
    
    @property
    def thumbnail_url(self):
        """Get a thumbnail version from Cloudinary"""
        if self.img:
            # Cloudinary automatically generates thumbnails
            return self.img.url.replace('/upload/', '/upload/c_thumb,w_150,h_150/')
        return None

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