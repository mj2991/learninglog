"""Defines url pattern for learning_logs"""

from django.urls import path
from . import views


app_name = 'learning_logs'

urlpatterns = [
    #Home page
    path('', view=views.index, name='index'),
    path('topics', view=views.topics, name='topics'),
    path('topic/<int:topic_id>', view=views.topic, name='topic'),
    path('new_topic', view=views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>', view=views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>', view=views.edit_entry, name='edit_entry'),
    path('topic_search', view=views.topic_search, name='topic_search')
]
