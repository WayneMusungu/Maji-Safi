from django.db import models


class Roles(models.TextChoices):
    WATER_SUPPLIER = "Supplier", "Supplier"
    CUSTOMER = "Customer", "Customer"
