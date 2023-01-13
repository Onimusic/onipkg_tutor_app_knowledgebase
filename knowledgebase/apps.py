from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class KnowledgebaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutor.apps.knowledgebase'
    verbose_name = _('Base de Conhecimento')
    label = 'knowledgebase'
