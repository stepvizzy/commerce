# Generated by Django 4.1.2 on 2022-11-22 10:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_stating_bid_auctionlisting_starting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 11, 22, 10, 43, 44, 171712, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
