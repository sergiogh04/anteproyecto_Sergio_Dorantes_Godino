# Generated by Django 5.2.1 on 2025-05-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina_main', '0004_remove_character_anime_alter_season_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='image',
            field=models.URLField(blank=True, default='https://via.placeholder.com/150'),
        ),
    ]
