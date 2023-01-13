# Generated by Django 4.1.2 on 2023-01-10 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_listing_bid_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listingBuyers', to=settings.AUTH_USER_MODEL),
        ),
    ]
