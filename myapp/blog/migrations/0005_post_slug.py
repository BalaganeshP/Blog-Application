# Generated by Django 5.1.3 on 2024-12-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_post_slug_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(max_length=255,blank=True,null=True),
            preserve_default=False,
        ),
    ]