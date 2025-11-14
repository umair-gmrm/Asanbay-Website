from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models.
    All Django models should inherit from this BaseModel.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
