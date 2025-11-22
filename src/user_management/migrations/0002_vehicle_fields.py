# Generated manually to add carrier vehicle/location fields.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='base_rate_per_km',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Preferred rate per km for carriers', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='current_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='current_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='vehicle_capacity_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
