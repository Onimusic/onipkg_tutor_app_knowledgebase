from django.shortcuts import render


def get_knowledgebase_index(request):
    return render(request, 'knowledgebase/index.html')