# Generated by Django 3.2.5 on 2022-07-18 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0011_alter_course_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='categories',
            field=models.CharField(choices=[('IG', 'Instagram'), ('FB', 'Facebook'), ('YT', 'Youtube'), ('DS', 'Dsps'), ('CR', 'Carreira'), ('MB', 'Music Business'), ('CP', 'Direitos Autorais'), ('MM', 'Marketing Musical')], default='IG', max_length=2, verbose_name='Categoria'),
        ),
    ]
