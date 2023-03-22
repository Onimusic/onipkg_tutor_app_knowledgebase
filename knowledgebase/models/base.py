from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _

from onipkg_contrib.api_helpers import strip_tags
from onipkg_contrib.models.base_model import BaseModel
from onipkg_contrib.models.general_helpers import generic_get_file_path
from onipkg_contrib.validators import validate_image_format, validate_image_max_300, validate_file_max_10000, \
    validate_document_format
from knowledgebase.utils.cons import POST_FROM_MAIL


def post_image_directory(instance, filename) -> str:
    """
    Retorna o path para o arquivo de imagem do post/tutorial.
    Args:
        instance: objeto BasePostModel
        filename: nome do arquivo da imagem

    Returns:
        path pra imagem
    """
    return generic_get_file_path('posts', 'knowledgebase/posts_or_tutorials/covers',
                                 filename)


def course_thumbnail_directory(instance, filename) -> str:
    """
    Retorna o path para o arquivo de thumbnail do curso.
    Args:
        instance: objeto Course
        filename: nome do arquivo da imagem

    Returns:
        path pra imagem
    """
    return generic_get_file_path(instance.id, 'courses/thumbnails', filename)


def lecture_file_thumbnail_directory(instance, filename) -> str:
    """
    Retorna o path para o arquivo de aula.
    Args:
        instance: objeto SectionFile
        filename: nome do arquivo da imagem

    Returns:
        path pro arquivo
    """
    return generic_get_file_path(instance.lecture.id, 'courses/files', filename)


class BasePostModel(BaseModel):
    """Base model com campos em comum de Tutorial e Post"""
    # todo implementar created_by
    slug = models.CharField(verbose_name=_('Slug'), help_text=_('Este campo é usado pra criar a url do post.'),
                            max_length=250, unique=True, blank=True, null=True)
    featured_image = models.ImageField(verbose_name=_('Imagem Destaque'), upload_to=post_image_directory,
                                       validators=[validate_image_format, validate_image_max_300],
                                       help_text=_('Dimensões') + ': 960x540; ' + _('Tam. Máx.') + ': 300kb; ' + _(
                                           'Somente os formatos .jpeg, .jpg e .png são permitidos.'))
    title = models.CharField(verbose_name=_('Título'), max_length=250)
    description = models.TextField(verbose_name=_('Descrição'))
    youtube_embedded = models.CharField(verbose_name=_('ID do Vídeo do Youtube '), null=True, blank=True,
                                        help_text=_('ID do vídeo do Youtube a ser embedado'), max_length=100)
    featured = models.BooleanField(verbose_name=_('Destaque'), default=False)
    order = models.IntegerField(verbose_name=_('Ordem'), default=0)

    class Meta:
        """Meta options for the model"""
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        """str method"""
        return self.title

    # def get_featured_image(self):
    #     """Retorna a imagem destaque do post"""
    #     return get_thumb_with_image_download_url(self.featured_image, self.featured_image, 540)
    #
    # def get_youtube_embedded(self):
    #     """Retorna o html formatado do youtube embedado para o front"""
    #     return default_get_youtube_embedded(self.youtube_embedded)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Sobrescrita do metodo save para chamar os metodos que ajustam o corpo do post"""
        self.fix_images_in_description()
        self.remove_color_from_font_in_description()
        super(BasePostModel, self).save()

    def fix_images_in_description(self):
        """Adiciona automaticamente a classe css responsavel por tornar imagens responsivas na descricao de posts e
            tutoriais.
        """
        if '<img ' in self.description and '<img class="fit-to-screen" ' not in self.description:
            self.description = self.description.replace('<img ', '<img class="fit-to-screen" ')

    def remove_color_from_font_in_description(self):
        """Remove quaisquer cores em fontes na descrição a partir de uma regex.
        """
        import re
        self.description = re.sub(r'color:#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', '', self.description)

    def get_sub_categories_display(self) -> list:
        """Retorna em formato de string todas as subcategorias do post"""
        return [subcategory.__str__() for subcategory in self.sub_categories.all()]

    def get_category_display(self) -> str:
        """Implementação necessária pois o método get_category_display padrão não funcionou neste modelo"""
        return self.category.__str__()

    def get_description_preview(self) -> str:
        """
        Escapa o HTML da descrição do post/tutorial
        """
        return strip_tags(self.description)


class PostCategory(BaseModel):
    """Post Category"""
    title = models.CharField(verbose_name=_('Título'), max_length=250)

    class Meta:
        """Meta options for the model"""
        verbose_name = _('Categoria de Post')
        verbose_name_plural = _('Categorias de Post')
        ordering = ['-created_at']

    def __str__(self):
        """str method"""
        return self.title


class Post(BasePostModel):
    """Posts do blog"""

    category = models.ForeignKey(verbose_name=_('Categoria'), to='PostCategory', on_delete=models.PROTECT,
                                 related_name='post_category')
    sub_categories = models.ManyToManyField(verbose_name=_('Subcategorias'), to='PostCategory', blank=True,
                                            related_name='post_subcategories')

    class Meta:
        """Meta options for the model"""
        verbose_name = _('Post do Blog')
        verbose_name_plural = _('Posts do Blog')
        ordering = ['-created_at']


class Tutorial(BasePostModel):
    """Tutoriais"""

    category = models.ForeignKey(verbose_name=_('Categoria'), to='PostCategory', on_delete=models.PROTECT,
                                 related_name='tutorial_category')
    sub_categories = models.ManyToManyField(verbose_name=_('Subcategorias'), to='PostCategory', blank=True,
                                            related_name='tutorial_subcategories')

    class Meta:
        verbose_name = _('Tutorial')
        verbose_name_plural = _('Tutoriais')
        ordering = ['-created_at']


class Course(BaseModel):
    class CourseCategories(models.TextChoices):
        INSTAGRAM = 'IG', _('Instagram')
        FACEBOOK = 'FB', _('Facebook')
        YOUTUBE = 'YT', _('Youtube')
        DSPS = 'DS', _('Dsps')
        CARRER = 'CR', _('Carrer')
        MUSIC_BUSINESS = 'MB', _('Music Business')
        COPYRIGHT = 'CP', _('Copyright')
        MUSIC_MARKETING = 'MM', _('Music Marketing')

    thumbnail = models.ImageField(verbose_name=_('Thumbnail do Curso'), upload_to=course_thumbnail_directory,
                                  validators=[validate_image_format, validate_image_max_300],
                                  help_text=_('Dimensões') + ': 960x540; ' + _('Tam. Máx.') + ': 300kb; ' + _(
                                      'Somente os formatos .jpeg, .jpg e .png são permitidos.'))
    name = models.CharField(verbose_name=_('Nome do Curso'), max_length=250)
    categories = models.CharField(verbose_name=_('Categoria'), choices=CourseCategories.choices,
                                  default=CourseCategories.INSTAGRAM, max_length=2)
    description = models.TextField(verbose_name=_('Descrição'), blank=True)

    class Meta:
        verbose_name = _('Curso')
        verbose_name_plural = _('Cursos')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}'

    def get_total_video_length(self) -> int:
        """
        Retorna o tempo total em vídeo do curso
        Returns:
            int representando a duração em minutos do tempo total
        """
        return sum(
            section.get_total_video_length()
            for section in self.coursesection_set.all()
        )

    def get_number_of_videos(self) -> int:
        """
        Retorna o número de vídeos do curso
        Returns:
            Número de vídeos
        """
        return sum(
            section.get_number_of_videos()
            for section in self.coursesection_set.all()
        )

    def get_number_of_sections(self) -> int:
        """
        Retorna o número de seções do curso
        Returns:
            inteiro representando o número de seções
        """
        return self.coursesection_set.count()


class CourseSection(BaseModel):
    name = models.CharField(verbose_name=_('Nome da Seção'), max_length=250)
    description = models.TextField(verbose_name=_('Descrição'), blank=True)
    course = models.ForeignKey(Course, verbose_name=_('Curso'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Seção do Curso')
        verbose_name_plural = _('Seções dos Cursos')
        ordering = ['id']

    def __str__(self):
        return f'{self.course} - {self.name}'

    def get_total_video_length(self) -> int:
        """
        Retorna o tempo total em vídeo da seção
        Returns:
            int representando a duração em minutos do tempo total
        """
        return sum(
            lecture.get_total_video_length() for lecture in self.lecture_set.all()
        )

    def get_number_of_videos(self) -> int:
        """
        Retorna o número de vídeos da seção
        Returns:
            Número de vídeos
        """
        return sum(
            lecture.get_number_of_videos() for lecture in self.lecture_set.all()
        )

    def get_number_of_files(self) -> int:
        """
        Retorna o número de arquivos na seção
        Returns:
            inteiro representando o número de arquivos
        """
        return sum(lecture.get_number_of_files() for lecture in self.lecture_set.all())

    def get_number_of_lectures(self) -> int:
        """
        Retorna o número de aulas na seção
        Returns:
            inteiro representando o número de aulas
        """
        return self.lecture_set.count()


class Lecture(BaseModel):
    name = models.CharField(verbose_name=_('Nome da Aula'), max_length=250)
    description = models.TextField(verbose_name=_('Descrição'), blank=True)
    section = models.ForeignKey(CourseSection, verbose_name=_('Seção desta aula'), on_delete=models.CASCADE)

    def get_total_video_length(self) -> int:
        """
        Retorna o tempo total em vídeo da aula (uma aula pode ter mais de um vídeo)
        Returns:
            int representando a duração em minutos do tempo total
        """
        return sum(video.video_length for video in self.sectionvideo_set.all())

    def get_number_of_videos(self) -> int:
        """
        Retorna o número de vídeos da seção
        Returns:
            Número de vídeos
        """
        return self.sectionvideo_set.count()

    def get_number_of_files(self) -> int:
        """
        Retorna o número de arquivos na seção
        Returns:
            inteiro representando o número de arquivos
        """
        return self.sectionfile_set.count()

    class Meta:
        verbose_name = _('Aula')
        verbose_name_plural = _('Aulas')
        ordering = ['id']

    def __str__(self):
        return f'{self.section} - {self.name}'


class SectionVideo(BaseModel):
    author = models.CharField(max_length=50, blank=True)
    name = models.CharField(verbose_name=_('Título do Vídeo'), max_length=100)
    description = models.TextField(verbose_name=_('Descrição'), blank=True)
    vimeo_video_id = models.CharField(verbose_name=_('ID do vídeo no Vimeo'), max_length=150,
                                      help_text=_('ID do vídeo que será embedado.'))
    video_length = models.SmallIntegerField(verbose_name=_('Duração do vídeo (em minutos'))
    lecture = models.ForeignKey(Lecture, verbose_name=_('Aula Relacionada'), on_delete=models.CASCADE)

    def get_embedded_video_html(self):
        """
        Retorna o html do vídeo para ser embedado
        Returns:
            html a embedar
        """
        return f'{self.vimeo_video_id}'

    class Meta:
        verbose_name = _('Vídeo de Aula')
        verbose_name_plural = _('Vídeos de Aula')
        ordering = ['id']

    def __str__(self):
        return f'{self.lecture} - {self.name} ({self.author})'


class SectionFile(BaseModel):
    name = models.CharField(verbose_name=_('Título do Arquivo'), max_length=100)
    file = models.FileField(upload_to=lecture_file_thumbnail_directory, verbose_name=_('Arquivo'),
                            validators=[validate_file_max_10000, validate_document_format],
                            help_text=_('Ex.: Arquivos de atividades, PDFs, etc'))
    lecture = models.ForeignKey(Lecture, verbose_name=_('Aula Relacionada'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Arquivo de Aula')
        verbose_name_plural = _('Arquivos de Aula')
        ordering = ['id']

    def __str__(self):
        return f'{self.lecture} - {self.name}'


@receiver(post_save, sender=Post)
def send_mail_after_save(sender, instance, using, **kwargs):
    # caso seja um post_save de criação podemos realizar o envio do email
    if kwargs.get('created', False):
        pass
        # from tutor.apps.core.tasks import send_email
        # # params
        # subject = _('Novo Post')
        # plain_msg = _('Confira o post {} no blog.').format(instance.title)
        # from_mail = POST_FROM_MAIL
        # to_mail = get_user_model().get_all_emails_from_non_staff_users()
        # send_email.apply_async((subject, plain_msg, from_mail, to_mail), eta=timezone.now() + timezone.timedelta(
        #     seconds=15))
