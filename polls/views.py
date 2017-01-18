import pdb
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.
from .models import Choice, Question, QuestionForm
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.db.models import Sum

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def most_voted(request):
    latest_question_list = Question.objects.annotate(num_choices=Sum('choice__votes')).order_by('-num_choices')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def create_poll(request):
    BookFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',),can_delete=False)
    question = Question()
    if request.method == 'POST':
	question_form = QuestionForm(request.POST)
        book_form = BookFormSet(request.POST,instance=question)
	#pdb.set_trace()
	if question_form.is_valid():
            question = question_form.save(commit=False)
            book_form = BookFormSet(request.POST,instance=question)
            if book_form.is_valid():
                question.save()
                book_form.save()
                return HttpResponseRedirect(reverse('polls:index'))		
        return render(request, 'polls/create.html', {'question_form':question_form,'book_form': book_form})
    else:
        question_form = QuestionForm(instance=question) # setup a form for the parent
        book_form = BookFormSet(instance=question)
    return render(request, 'polls/create.html', {'question_form':question_form,'book_form': book_form})
