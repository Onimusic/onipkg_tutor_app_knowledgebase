from django.http import HttpResponse
from oauth2_provider.views import ProtectedResourceView
from rest_framework import generics, permissions
from rest_framework.response import Response

from knowledgebase.api.serializers import PostCategorySerializer, \
    PostSerializer, SectionFileSerializer, SectionVideoSerializer, LectureSerializer, CourseSectionSerializer, \
    CourseSerializer, TutorialSerializer
from knowledgebase.utils.api_helpers import StandardResultsSetPagination
from knowledgebase.models import PostCategory, Post, SectionFile, SectionVideo, Lecture, \
    CourseSection, Course, Tutorial
from ..utils.permissions import HasCourseReadPermission, HasTutorialReadPermission, HasBlogReadPermission


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


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


class TutorialRetrieve(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTutorialReadPermission]
    required_scopes = ['read']
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer


class CourseList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, HasCourseReadPermission]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        category = request.query_params.get('category', None)
        if category:
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

        course = request.query_params.get('course_id', None)
        if course:
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
        section = request.query_params.get('section_id', None)
        if section:
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

        lecture = request.query_params.get('lecture_id', None)
        if lecture:
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

        lecture = request.query_params.get('lecture_id', None)
        if lecture:
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
