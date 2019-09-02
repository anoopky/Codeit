import datetime
import json
from difflib import SequenceMatcher
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

import onlinecompiler.core.compiler as com
from onlinecompiler.models import Questions, TestCases, Result


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        if user.is_active:
            if user.is_staff:
                return redirect('/add')
            else:
                return redirect('/')
    else:
        if request.user.is_active:
            if request.user.is_staff:
                return redirect('/add')
            else:
                return redirect('/')
        else:
            return render(request, 'login.html')


@login_required(login_url='/login/')
def dashboard(request):
    if request.user.is_staff:
        return redirect('/add')
    else:
        ques = Questions.objects.all()
        return render(request, 'dashboard.html', {'ques': ques})


@login_required(login_url='/login/')
def add_question(request):
    if request.method == 'POST':
        title = request.POST.get("title", "")
        explanation = request.POST.get("explanation", "")
        description = request.POST.get("description", "")
        input_public = request.POST.get("input", "")
        output_public = request.POST.get("output", "")
        private = request.POST.get("privateCases", "")
        verification = request.POST.get("verification", "")
        verify = 0
        if verification == "on":
            verify = 1
        ques = Questions.objects.create(title=title, description=description, input_public=input_public,
                                        output_public=output_public, explanation=explanation, verification=verify)
        # adding private test cases
        for x in range(1, int(private) + 1):
            input_private = request.POST.get("inputP" + str(x), "")
            output_private = request.POST.get("outputP" + str(x), "")
            TestCases.objects.create(questionId=ques, input_private=input_private, output_private=output_private)

    return render(request, 'add_question.html', context=None)


@login_required(login_url='/login/')
def question(request, idn):
    if request.user.is_staff:
        return redirect('/add')
    else:
        ques = Questions.objects.get(id=idn)
        return render(request, 'question.html', {'ques': ques})


@login_required(login_url='/login/')
def result(request):
    if request.user.is_staff:
        return redirect('/add')
    else:
        results = Result.objects.all()
        return render(request, 'result.html', {'results': results})


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login/')
def compile_test_cases(request):
    lang = request.POST.get("lang", "")
    code = request.POST.get("code", "")
    idn = request.POST.get("id", "")
    ques = Questions.objects.get(id=idn)
    similarity_ratio = [0]
    # performing code verification
    if ques.verification:
        results = Result.objects.filter(Q(questionId_id=ques) & ~Q(user_id=request.user) & ~Q(status="Copied"))
        for res in results:
            similarity_ratio.append(SequenceMatcher(None, code, res.code).ratio())
    test_cases = TestCases.objects.filter(Q(questionId_id=ques))
    in_data = []
    match_data = []
    for test in test_cases:
        in_data.append(test.input_private)
        match_data.append(test.output_private)
    # executing code
    code_compiler = com.Compiler(code, lang, request.user.id, in_data)
    i = 0
    output = []
    score = 0
    while i < len(code_compiler.output):
        if str(code_compiler.output[i]).strip() == str(match_data[i]).replace("\r\n", "\n"):
            output.append(1)
            score += 1
        else:
            output.append(0)
        i += 1

    json_string = json.dumps(output)
    status = "Accepted"
    score = (score / len(code_compiler.output)) * 10
    if float(max(similarity_ratio)) > 0.9:
        status = "Copied"
        score = 0
        json_string = json.dumps("-1")
    # updating score
    defaults = {'code': code, 'language': lang, 'execution_time': str(code_compiler.time / 100000.0),
                'score': str(score), 'status': status}
    Result.objects.update_or_create(questionId_id=ques.id, user_id=request.user.id,
                                    defaults=defaults)
    return HttpResponse(json_string)


@login_required(login_url='/login/')
def compile_debug(request):
    lang = request.POST.get("lang", "")
    code = request.POST.get("code", "")
    idn = request.POST.get("id", "")
    custom = request.POST.get("custom", "")
    c_input = request.POST.get("cinput", "")
    ques = Questions.objects.get(id=idn)
    # checking for custom input
    if custom == "1":
        in_data = [c_input]
    else:
        in_data = [ques.input_public]

    match_data = ques.output_public
    code_compiler = com.Compiler(code, lang, request.user.id, in_data)
    output = list()
    output.append(in_data[0])
    output.append(code_compiler.output)
    if custom == "1":
        output.append("")
    else:
        output.append(match_data)
    if code_compiler.output == match_data:
        output.append(1)
    else:
        output.append(0)
    json_string = json.dumps(output)
    return HttpResponse(json_string)
