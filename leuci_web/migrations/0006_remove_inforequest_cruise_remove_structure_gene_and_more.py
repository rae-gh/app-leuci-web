# Generated by Django 4.2 on 2023-04-07 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leuci_web', '0005_remove_cruise_destintations_cruise_destinations_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inforequest',
            name='cruise',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='gene',
        ),
        migrations.DeleteModel(
            name='Cruise',
        ),
        migrations.DeleteModel(
            name='Destination',
        ),
        migrations.DeleteModel(
            name='Gene',
        ),
        migrations.DeleteModel(
            name='InfoRequest',
        ),
        migrations.DeleteModel(
            name='Structure',
        ),
    ]
