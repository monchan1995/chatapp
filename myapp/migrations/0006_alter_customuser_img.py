# Generated by Django 5.1.1 on 2024-10-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_customuser_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='img',
            field=models.ImageField(default='baby_role_towel_utsubuse.png', upload_to='', verbose_name='アイコン'),
        ),
    ]
