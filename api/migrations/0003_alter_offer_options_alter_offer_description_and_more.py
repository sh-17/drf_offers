# Generated by Django 4.2.7 on 2023-12-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_offer_delete_student'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'ordering': ['status']},
        ),
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]