from django.urls import path

from .views import PostList, PostRetrieve, PostCategoryList, \
    CourseList, CourseRetrieve, CourseSectionList, CourseSectionRetrieve, LectureList, LectureRetrieve, \
    SectionVideoList, SectionVideoRetrieve, SectionFileList, SectionFileRetrieve, TutorialList, TutorialRetrieve, \
    GetWordpressBlogPosts

router = [
    path('tutorials', TutorialList.as_view()),
    path('tutorials/<pk>', TutorialRetrieve.as_view()),
    path('posts', GetWordpressBlogPosts.as_view()),
    path('posts/<pk>', PostRetrieve.as_view()),
    path('post-categories', PostCategoryList.as_view()),
    path('courses', CourseList.as_view()),
    path('courses/<pk>', CourseRetrieve.as_view()),
    path('course-sections', CourseSectionList.as_view()),
    path('course-sections/<pk>', CourseSectionRetrieve.as_view()),
    path('lectures', LectureList.as_view()),
    path('lectures/<pk>', LectureRetrieve.as_view()),
    path('section-videos', SectionVideoList.as_view()),
    path('section-videos/<pk>', SectionVideoRetrieve.as_view()),
    path('section-files', SectionFileList.as_view()),
    path('section-files/<pk>', SectionFileRetrieve.as_view()),
]
