from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _

from .models import PostCategory, Course, CourseSection, Lecture, SectionVideo, SectionFile, Tutorial, Post

import nested_admin


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label=_('Description'))

    class Meta:
        """Meta options for the model"""
        model = Post
        fields = [
            'slug',
            'title',
            'category',
            'sub_categories',
            'description',
            'youtube_embedded',
            'featured',
            'featured_image',
            'order',
        ]


class TutorialForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), label=_('Description'))

    class Meta:
        """Meta options for the model"""
        model = Tutorial
        fields = [
            'slug',
            'title',
            'category',
            'sub_categories',
            'description',
            'youtube_embedded',
            'featured',
            'featured_image',
            'order',
        ]


# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    """
    form = PostForm
    list_display = [
        'title',
        'featured_image',
        'category',
        'featured',
    ]
    search_fields = [
        'title',
    ]
    readonly_fields = ['created_at', 'updated_at']


# @admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):

    """
    """
    form = TutorialForm
    list_display = [
        'title',
        'featured_image',
        'category',
        'featured',
    ]
    search_fields = [
        'title',
    ]
    readonly_fields = ['created_at', 'updated_at']


# @admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    """
    fields = ['title']
    list_display = ['title']
    search_fields = ['title', ]
    readonly_fields = ['created_at', 'updated_at']


class SectionVideoInline(nested_admin.NestedStackedInline):
    extra = 1
    max_num = 1
    model = SectionVideo
    verbose_name = _('Vídeo de Aula')
    verbose_name_plural = _('Vídeo de Aula')
    fields = [
        'author',
        'name',
        'description',
        'vimeo_video_id',
        'video_length',
    ]


class SectionFileInline(nested_admin.NestedStackedInline):
    extra = 0
    model = SectionFile
    verbose_name = _('Arquivo de Aula')
    verbose_name_plural = _('Arquivos de Aula')
    fields = [
        'name',
        'file',
    ]


class LectureInline(nested_admin.NestedStackedInline):
    extra = 1
    model = Lecture
    verbose_name = _('Aula')
    verbose_name_plural = _('Aulas')
    fields = [
        'name',
        'description',
    ]
    inlines = [SectionVideoInline, SectionFileInline]


class CourseSectionInline(nested_admin.NestedStackedInline):
    extra = 1
    model = CourseSection
    verbose_name = _('Seção do Curso')
    verbose_name_plural = _('Seções do Curso')
    fields = [
        'name',
        'description',
    ]
    inlines = [LectureInline, ]


@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    """
    """
    fields = [
        'thumbnail',
        'thumbnail_landscape',
        'name',
        'categories',
        'description',
    ]
    search_fields = ['name', ]
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CourseSectionInline, ]


# @admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    """
    """
    fields = [
        'name',
        'description',
        'course',
    ]
    search_fields = ['name', 'course']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LectureInline,]


# @admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    """
    """
    fields = [
        'name',
        'description',
        'section',
    ]
    search_fields = ['name', 'section']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SectionVideoInline, SectionFileInline]


# @admin.register(SectionVideo)
class SectionVideoAdmin(admin.ModelAdmin):
    """
    """
    fields = [
        'author',
        'name',
        'description',
        'vimeo_video_id',
        'video_length',
        'lecture',
    ]
    search_fields = ['name', 'author', 'lecture', ]
    readonly_fields = ['created_at', 'updated_at']


# @admin.register(SectionFile)
class SectionFileAdmin(admin.ModelAdmin):
    """
    """
    fields = [
        'name',
        'file',
        'lecture',
    ]
    search_fields = ['name', 'lecture', ]
    readonly_fields = ['created_at', 'updated_at']
