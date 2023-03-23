# Generated by Django 3.2.5 on 2021-11-17 12:17

from django.db import migrations, models
import onipkg_contrib.validators
import knowledgebase.models.base


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0006_auto_20211021_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectionfile',
            name='file',
            field=models.FileField(help_text='Ex.: Arquivos de atividades, PDFs, etc', upload_to=knowledgebase.models.base.lecture_file_thumbnail_directory, validators=[onipkg_contrib.validators.validate_file_max_10000, onipkg_contrib.validators.validate_document_format], verbose_name='Arquivo'),
        ),
    ]
