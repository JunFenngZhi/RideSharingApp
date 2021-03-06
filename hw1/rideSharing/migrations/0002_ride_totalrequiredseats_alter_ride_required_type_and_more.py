# Generated by Django 4.0.1 on 2022-01-29 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rideSharing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='totalRequiredSeats',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ride',
            name='required_type',
            field=models.CharField(choices=[('SU', 'SUV'), ('CT', 'Compact'), ('SD', 'Sedan'), ('CP', 'Coupe'), ('OT', 'Other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('F', 'Confirmed'), ('C', 'Complete')], default='O', max_length=1),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='owner_vehicle', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('SU', 'SUV'), ('CT', 'Compact'), ('SD', 'Sedan'), ('CP', 'Coupe'), ('OT', 'Other')], max_length=2),
        ),
    ]
