from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpRequest,JsonResponse,Http404,HttpResponseRedirect
from . models import Question,Choice
from django.template import loader
from django.urls import reverse 
from django.views import generic
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published Questions.
        return Question.objects.order_by('-pub_date')[:5]

# def index(request:HttpRequest) -> HttpResponse:
#     #select * from post_questions order by pub_date desc limit 5
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {
#         "latest_question_list":latest_question_list
#         }
#     return render(request,'polls/index.html',context)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def detail(request: HttpRequest, question_id: int)->HttpResponse:
    question = get_object_or_404(Question,id=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request: HttpRequest,question_id: int)->HttpResponse:
    question = get_object_or_404(Question,pk=question_id)
    return render(request,"polls/results.html",{"question":question})

def vote(request: HttpRequest, question_id: int)->HttpResponse:
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice : Choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' : question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))
