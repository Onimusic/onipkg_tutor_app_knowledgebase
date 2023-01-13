# Generated by Django 3.2.5 on 2021-09-14 12:31

from django.db import migrations, models
import django.db.models.deletion
import contrib.validators


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0003_auto_20210914_0836'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tutorial',
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Post do Blog', 'verbose_name_plural': 'Posts do Blog'},
        ),
        migrations.RemoveField(
            model_name='post',
            name='type',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post_category', to='knowledgebase.postcategory', verbose_name='Categoria'),
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('slug', models.CharField(blank=True, help_text='Este campo é usado pra criar a url do post.', max_length=250, null=True, unique=True, verbose_name='Slug')),
                ('featured_image', models.ImageField(blank=True, help_text='Dimensões: 960x540; Tam. Máx.: 300kb; Somente os formatos .jpeg, .jpg e .png são permitidos.', null=True, upload_to='posts/covers/', validators=[contrib.validators.validate_image_format, contrib.validators.validate_image_max_300], verbose_name='Imagem Destaque')),
                ('title', models.CharField(max_length=250, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('youtube_embedded', models.CharField(blank=True, help_text='ID do vídeo do Youtube a ser embedado', max_length=100, null=True, verbose_name='ID do Vídeo do Youtube ')),
                ('featured', models.BooleanField(default=False, verbose_name='Destaque')),
                ('order', models.IntegerField(default=0, verbose_name='Ordem')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tutorial_category', to='knowledgebase.postcategory', verbose_name='Categoria')),
                ('sub_categories', models.ManyToManyField(blank=True, related_name='tutorial_subcategories', to='knowledgebase.PostCategory', verbose_name='Subcategorias')),
            ],
            options={
                'verbose_name': 'Tutorial',
                'verbose_name_plural': 'Tutoriais',
            },
        ),
    ]
