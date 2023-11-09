from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from knowledgebase.api.serializers import PostCategorySerializer, \
    PostSerializer, SectionFileSerializer, SectionVideoSerializer, LectureSerializer, CourseSectionSerializer, \
    CourseSerializer, TutorialSerializer
from knowledgebase.utils.api_helpers import StandardResultsSetPagination
from knowledgebase.models import PostCategory, Post, SectionFile, SectionVideo, Lecture, \
    CourseSection, Course, Tutorial
from ..utils.permissions import HasCourseReadPermission, HasTutorialReadPermission, HasBlogReadPermission

class PostCategoryList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasBlogReadPermission]
    required_scopes = ['read']
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


class PostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasBlogReadPermission]
    required_scopes = ['read']
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination


class PostRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasBlogReadPermission]
    required_scopes = ['read']
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TutorialList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTutorialReadPermission]
    required_scopes = ['read']
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    pagination_class = StandardResultsSetPagination


class GetWordpressBlogPosts(APIView):
    def get(self, request):
        import requests

        response = requests.get('https://amplifyus.app/wp-json/wp/v2/posts')
        if response.status_code == 200:
            data = response.json()
            results = []
            for post in data:
                title = post.get('title').get('rendered')
                description = post.get('yoast_head_json').get('og_description')
                date = post.get('date')
                og_image_url = post.get('yoast_head_json').get('og_image')[0]['url']
                type = post.get('type')
                estimated_time = post.get('yoast_head_json').get('twitter_misc')['Est. tempo de leitura']
                article_section = post.get('yoast_head_json').get('schema').get('@graph')[0].get('articleSection')[0]
                content_html = post.get('content').get('rendered')
                link = post.get('link')

                post_dict = {
                    'title': title,
                    'description': description,
                    'date': date,
                    'og_image_url': og_image_url,
                    'type': type,
                    'content': content_html,
                    'estimated_time': estimated_time,
                    'article_section': article_section,
                    'link': link.replace('\\', '')+'?vm=mobileapp'
                }
                results.append(post_dict)
            return Response(results)
        return Response(status=400)


class TutorialRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTutorialReadPermission]
    required_scopes = ['read']
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def retrieve(self, request, *args, **kwargs):
        print('retrivarei')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        from knowledgebase.models.base import UserTutorialRead
        try:
            print('cacarei')
            UserTutorialRead.objects.get(tutorial=instance, user_id=request.user.id)
            print('achei')
        except UserTutorialRead.DoesNotExist:
            print('num achei')
            UserTutorialRead.objects.create(tutorial=instance, user_id=request.user.id)
            print('criei')
        print('retornarei')
        return Response(serializer.data)


class CourseList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if category := request.query_params.get('category', None):
            queryset = queryset.filter(categories=category)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CourseRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseSectionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if course := request.query_params.get('course_id', None):
            queryset = queryset.filter(course_id=course)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CourseSectionRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer


class LectureList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        course = request.query_params.get('course_id', None)
        if section := request.query_params.get('section_id', None):
            queryset = queryset.filter(section_id=section)
        elif course:
            queryset = queryset.filter(section__course_id=course)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LectureRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    required_scopes = ['read']
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class SectionVideoList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = SectionVideo.objects.all()
    serializer_class = SectionVideoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if lecture := request.query_params.get('lecture_id', None):
            queryset = queryset.filter(lecture_id=lecture)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SectionVideoRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    required_scopes = ['read']
    queryset = SectionVideo.objects.all()
    serializer_class = SectionVideoSerializer


class SectionFileList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = SectionFile.objects.all()
    serializer_class = SectionFileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if lecture := request.query_params.get('lecture_id', None):
            queryset = queryset.filter(lecture_id=lecture)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SectionFileRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    required_scopes = ['read']
    queryset = SectionFile.objects.all()
    serializer_class = SectionFileSerializer
