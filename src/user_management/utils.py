from django.db import models

class UserTypeChoice(models.TextChoices):
    CARRIER = 'carrier', 'Carrier'
    CONSIGNOR = 'consignor', 'Consignor'
