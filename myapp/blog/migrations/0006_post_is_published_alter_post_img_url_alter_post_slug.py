# Generated by Django 5.1.3 on 2024-12-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='img_url',
            field=models.ImageField(null=True, upload_to='posts/images'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            #field=models.SlugField(default='example.slug', unique=True),
            field=models.CharField(max_length=255,blank=True,null=True),
            preserve_default=False,
        ),
    ]
