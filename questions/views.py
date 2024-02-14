from django.shortcuts import render

# Create your views here.
import re
import pytz
import openai
from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from .models import Question,Verify
from datetime import datetime
from .forms import CreateQuestions,CreateAnswers
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.template import RequestContext

pattern = [r"I rate it (\d+(\.\d+)?)", r"\b(\d+(\.\d+)?)\b"]
def home(request):
    return render(request, "questions/index.html")

def index(request):
    try:
        latest_question_list = Question.objects.order_by("-day")[:5]
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    context = {
        "latest_question_list": latest_question_list,
    }

    return render(request, "questions/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def complete(request):
    #display all questions
    all_questions = Question.objects.filter(complete=False)
    print(all_questions)
    return render(request, 'questions/complete.html', {
                            'all_questions': all_questions,
                            }
                  )

def submit(request, question_id):
    if request.method == 'POST':
        form = CreateAnswers(request.POST)
        if form.is_valid():
            answer = form['answer'].value()
            Question.objects.filter(id=question_id).update(answer_text=answer)

            return HttpResponseRedirect('/')
    else:
        form = CreateAnswers()
    return render(request, 'questions/submit.html', {
        'form': form,
        'question_id': question_id
    }
                  )
    #onclick - update answer

def write(request):
    if request.method == 'POST':
        form = CreateQuestions(request.POST)
        if form.is_valid():
            question = form['question_form'].value()
            day = form['day_form'].value()
            new_obj = Question.objects.create(question_text=question,
                                              day=day)
            date_check()

            return HttpResponseRedirect('/questions/write')
    else:
        form = CreateQuestions()
    return render(request, 'questions/write.html', {
                            'form': form,
                            }
                  )

def check(request):
    dates = Question.objects.filter(complete=False).values('day').distinct()
    print(dates)
    date_check()
    for i in dates:
        print(i["day"])
    return render(request, 'questions/check.html', {
                            'dates': dates,
                            }
                  )
def status(request):
    status = Verify.objects.all()[:1]
    return render(request, 'questions/status.html', {
                            'verify': status
                            }
                  )
def gpt(request, mydate):
    openai.api_key = open("questions/key2.txt", "r").read().strip("\n")
    #read 3 day questions
    three_questions = Question.objects.filter(day=mydate).filter(complete=False)[:3]
    print(three_questions)
    data = []
    #submit 3 day questions
    for j,i in enumerate(three_questions):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
            messages=[{"role": "user", "content": "Rate the following Question and Answer on a scale of 1-10 based "
                                                  "on how correct and relevant the answer is. Answers should be around 100 words. Question: %s "
                                                  "Answer: %s. "
                                                  "Give a one sentence reply in the format: I rate it (rating)." % (i.question_text, i.answer_text)}]
        )
        reply_content = completion.choices[0].message.content
        data.append([i.question_text,i.answer_text,reply_content])
        for p in pattern:
            match = re.search(p, reply_content)
            if match:
                rating = float(match.group(1))
                print("Extracted Rating:", rating)
                if rating > 8:
                    Question.objects.filter(id=i.id).update(complete=True)
                break
            else:
                print("No Rating found in pattern p")
    date_check()
    return render(request, 'questions/gpt.html', {
                'data': data})
        # if greater than 7 uncheck those questions

def date_check():
    #Returns Boolean
    #True if all tasks of today and past are solved
    #False if there exist some tasks of today and past
    dates = Question.objects.filter(complete=False).values('day').distinct()
    print("___________")
    print(dates)
    today = datetime.today()
    print(today)
    return_value = 0
    for date in dates:
        # Compare dates
        print(date['day'])
        if date['day'].date() < today.date():
            print("Tasks are pending for today. Tasks were created for the past.")
            return_value = return_value + 1
        elif date['day'].date() > today.date():
            print("No tasks pending")

        else:
            print("Tasks are pending for today. Tasks were created for today.")
            return_value = return_value + 1
    if return_value == 0:
        Verify.objects.filter(id=1).update(complete=True)
    if return_value > 0:
        Verify.objects.filter(id=1).update(complete=False)