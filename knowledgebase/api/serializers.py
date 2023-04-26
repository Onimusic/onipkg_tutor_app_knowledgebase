from rest_framework import serializers

from knowledgebase.models import PostCategory, Post, Course, CourseSection, Lecture, \
    SectionVideo, SectionFile, Tutorial


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = [
            'title',
        ]


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField('%d/%m/%Y')
    updated_at = serializers.DateTimeField('%d/%m/%Y')
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'youtube_embedded',
            'featured',
            'created_at',
            'updated_at',
            'order',
            'slug',
            'category',
            'get_category_display',
            'featured_image',
            'sub_categories',
            'get_sub_categories_display',
        ]

    def get_preview(self, obj):
        return obj.get_description_preview()


class TutorialSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField('%d/%m/%Y')
    updated_at = serializers.DateTimeField('%d/%m/%Y')
    preview = serializers.SerializerMethodField()
    seen = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        fields = [
            'id',
            'title',
            'preview',
            'description',
            'youtube_embedded',
            'featured',
            'created_at',
            'updated_at',
            'order',
            'slug',
            'category',
            'get_category_display',
            'featured_image',
            'sub_categories',
            'get_sub_categories_display',
            'seen',
        ]

    def get_preview(self, obj):
        return obj.get_description_preview()

    def get_seen(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            from knowledgebase.models.base import UserTutorialRead
            return UserTutorialRead.objects.filter(tutorial=obj.id, user_id=user.id).exists()
        else:
            return False


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'thumbnail',
            'name',
            'categories',
            'get_categories_display',
            'description',
            'get_total_video_length',
            'get_number_of_videos',
            'get_number_of_sections',
        ]


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = [
            'id',
            'name',
            'description',
            'course',
            'get_total_video_length',
            'get_number_of_videos',
            'get_number_of_files',
            'get_number_of_lectures',
        ]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            'id',
            'name',
            'description',
            'section',
            'get_total_video_length',
            'get_number_of_videos',
            'get_number_of_files',
        ]


class SectionVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionVideo
        fields = [
            'id',
            'author',
            'name',
            'description',
            'vimeo_video_id',
            'video_length',
            'lecture',
            'get_embedded_video_html',
        ]


class SectionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionFile
        fields = [
            'id',
            'name',
            'file',
            'lecture',
        ]
