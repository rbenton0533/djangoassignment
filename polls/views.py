from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from .models import Choice, Question, Comments

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
                Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def comments(request):
    if request.method == 'POST':
        name_field = request.POST.get('name_field')
        comment_text = request.POST.get('comment_text')
        commentObject = Comment(name_field = name_field, comment_text = comment_text)
        commentObject.save()
        comments = Comment.objects.all()
    return render(request, 'polls/comment.html',{'comment': comments})

def commentslist(request):
    commentslist = Comment.objects.all()
    return render(request, 'polls/list.html', {'commentslist': commentslist})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args= (question.id,)))
