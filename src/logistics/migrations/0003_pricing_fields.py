# Generated manually to add pricing-related fields.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='destination_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='load',
            name='destination_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='load',
            name='pickup_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='load',
            name='pickup_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='distance_km',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='selected_algorithm',
            field=models.CharField(choices=[('dynamic', 'Dynamic (market/urgency)'), ('distance', 'Location (haversine)'), ('weight', 'Vehicle weight fit')], default='dynamic', max_length=20),
        ),
    ]
