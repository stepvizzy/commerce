# Generated by Django 4.1.2 on 2022-11-25 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_image_alter_watchlist_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuctionListing',
            new_name='Listing',
        ),
    ]
