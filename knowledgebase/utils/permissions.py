from rest_framework.permissions import BasePermission


class HasCourseReadPermission(BasePermission):
    """Permissão para ver Cursos e modelos dependentes deste"""
    def has_permission(self, request, view) -> bool:
        # todo posteriormente checar tipo do perfil
        return True


class HasBlogReadPermission(BasePermission):
    """Permissão para ver Post e modelos dependentes deste"""
    def has_permission(self, request, view) -> bool:
        # todo posteriormente checar tipo do perfil
        return True


class HasTutorialReadPermission(BasePermission):
    """Permissão para ver Tutoriais e modelos dependentes deste"""
    def has_permission(self, request, view) -> bool:
        # todo posteriormente checar tipo do perfil
        return True