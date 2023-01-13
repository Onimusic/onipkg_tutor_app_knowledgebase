from django.urls import path, include

from ...api.knowledgebase.routes import router

app_name = 'knowledgebase'
urlpatterns = [
    path('api/v1/', include(router)),
]
