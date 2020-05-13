from django.http import Http404

def check_topic_owner(topic, request):
    """check if user owns topic"""
    if topic.owner != request.user:
        raise Http404
