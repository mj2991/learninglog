from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from .views_helper_funs import check_topic_owner
from django.db.models import Q


# Create your views here.

def index(request):
    """The home page for learning logs"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by("-date_added")
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """show topic page with topic_id"""
    topic = get_object_or_404(Topic, topic_id)
    #make sure topics belong to current user
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adds new topic"""
    if request.method != 'POST':
        #no data submitted; create a blank form
        form = TopicForm
    else:
        #POST data submitted; submit data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    #Display a blank or invalid form
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Ads new entry to topic with topic_id"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #no data submitted; send blank form
        form = EntryForm()

    else:
        #post data submitted; process data
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            check_topic_owner(topic, request)
            new_entry.topic = topic 
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #Display a blank or invalid form
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Allows users to edit existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    #make sure entries belong to current user
    check_topic_owner(topic, request)
    topic = entry.topic

    if request.method != 'POST':
        #initial request; prefiled form with existing entry
        form = EntryForm(instance=entry)
    else:
        #POST data submitted
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)


def topic_search(request):
    """Show all topics with search bar"""
    query_result = []
    query = request.GET.get('search_input')
    for q in query.split():
        topics = Topic.objects.filter(owner=request.user).filter(text__icontains=q)
        for topic in topics:
            query_result.append(topic)
    context = {'topics': list(set(query_result))}
    return render(request, 'learning_logs/topic_search.html', context)
