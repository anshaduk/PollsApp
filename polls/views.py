from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpRequest,JsonResponse,Http404
from . models import Question
from django.template import loader
# Create your views here.

def index(request:HttpRequest) -> HttpResponse:
    #select * from post_questions order by pub_date desc limit 5
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list":latest_question_list
        }
    return render(request,'polls/index.html',context)


def detail(request: HttpRequest, question_id: int)->HttpResponse:
    question = get_object_or_404(Question,id=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request: HttpRequest,question_id: int)->HttpResponse:
    respons = f"You're looking at the results of question {question_id}."
    return HttpResponse(respons)

def vote(request: HttpRequest, question_id: int)->HttpResponse:
    return HttpResponse(f"You're voting on question {question_id}.")
