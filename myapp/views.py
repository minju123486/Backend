from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import openai
import os
import environ


user_data = dict()

from pathlib import Path
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
import openai
import os
from .models import course, professor_lecture, student_lecture, problem, answer
env = environ.Env()
environ.Env.read_env(Path(__file__).resolve().parent/'.env')
openai.api_key = env('Key')
Quest_dict = {'객관식-빈칸': 1, '객관식-단답형': 2, '객관식-문장형': 3, '단답형-빈칸': 4, '단답형-문장형': 5, 'OX선택형-O/X': 6, '서술형-코딩': 7}
history = []
def get_completion(prompt, numberKey,count):     
    history.append({'role':'user','content':gpt_prompt.prompt_1}) 
    query = openai.ChatCompletion.create( 
       model="gpt-4-turbo",
       messages=[{"role": "system", "content": gpt_prompt.System_lst[numberKey]}, {'role':'user','content':gpt_prompt.prompt_lst[numberKey](count)}], 
       max_tokens=1024, 
       n=1,
       stop=None,
       temperature=0.5, 
    ) 
    response = query.choices[0].message["content"]
    history.append({'role':'assistant', 'content':response})
    print(response)
    return response

def index(request):
    return HttpResponse("Communication start")
    
def query_view(request,numberKey, count): 
    prompt = request.data.get('username') 
    prompt=str(prompt)
    response = get_completion(prompt, numberKey,count)
    return JsonResponse({'response': response}), response 

def GenerateWriteProblem(tmp):
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    tempt = dict()
    for i in lst:
        if check:
            id = 0
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
            tempt['content'] = i[id::]
            check = False
            continue
        if i[0:2] == '문제':
            if len(i) == 2:
                check = True
                continue
            else:
                id = 2
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]
                tempt['content'] = b
        elif i[0:2] == '정답' or i[0:2] == '정닱':
            tempt['answer'] = i[4::]
            rtr.append(tempt)
            tempt = dict()
    # print(rtr)
    return rtr
            
def GenerateMultipleProblem(tmp):
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    idx = 1
    tempt = dict()
    for i in lst:
        if check:
            id = 0
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
            tempt['content'] = i[id::]
            check = False
            continue
        if i[0:2] == '문제':
            if len(i) == 2:
                check = True
            else:
                id = 2
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]
                tempt['content'] = b
                tempt['options'] = []
        elif len(i) > 0 and i[0]!= '-' and i[0] != ' ' and i[0:2] != '정답' and i[0:2] != '정닱'  and 1 <= int(i[0]) <= 4:
            b = i[4:]
            tempt['options'].append(b)
        elif i[0:2] == '정답' or i[0:2] == '정닱':
            tt = ''
            ch = 0
            ttt = 0
            for j in i:
                if ch == 3:
                    tt += j
                if ch == 1 or ch == 2:
                    ch += 1
                    continue
                if j == '1' or j == '2' or j == '3' or j == '4' :
                    ttt = int(j)
                    ch = 1
            tempt['answer'] = f'정답 : {ttt}번  {tt}'
            rtr.append(tempt)
            tempt = dict()
            continue
    # print(rtr)
    return rtr

def Code_problem(tmp):
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    idx = 1
    tempt = dict()
    toggle = True
    quest = ''
    for i in lst:
        if check:
            id = 0
            if len(i) == 0:
                continue
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
                
            quest += i[id::]+'\n'
            check = False
            continue
        if i[0:2] == '문제':
            if len(i) == 2:
                check = True
            else:
                id = 2
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]+'\n'
                quest += b
        elif i[0:3] == '```':
            if toggle == True:
                tempt['language'] = i[3::]
                toggle = False
            else:
                tempt['content'] = quest
                quest = ''
                toggle = True
                rtr.append(tempt)
                tempt = dict()
        elif not toggle:
            quest += i+'\n'
    # print(rtr)
    return rtr
            
            
@api_view(['POST'])
def GenerateQuestion(request):
    print(request.data.get('selections'))
    ans = {}
    ans['questions'] = []
    problem_lst = []
    for _ in range(10):
        problem_lst.append('')
    cnt = 0
    for m in range(1,8):
        for tempt in request.data.get('selections'):
            if 1 <= Quest_dict[tempt] <= 3 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt])
                tmp['items'] = GenerateMultipleProblem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                c = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                for k in tmp['items']:
                    tempt_content = f'{Quest_dict[tempt]}'
                    for i in k:
                        if i == 'content':
                            tempt_content += '$$'+k[i]
                        elif i == 'options':
                            for id, j in enumerate(k[i]):
                                tempt_content += '$$'+f'{id+1}번 : ' +j
                        elif i == 'answer':
                            tempt_content += '$$'+k[i]
                    tempt_content += f'$${c}'
                    problem_lst[cnt] = tempt_content
                    cnt += 1
            elif 4 <= Quest_dict[tempt] <= 6 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt])
                tmp['items'] = GenerateWriteProblem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                c = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                for k in tmp['items']:
                    tempt_content = f'{Quest_dict[tempt]}'
                    for i in k:
                        if i == 'content':
                            tempt_content += '$$'+k[i]
                        elif i == 'answer':
                            tempt_content += '$$'+k[i]
                    tempt_content +=  f'$${c}'
                    problem_lst[cnt] = tempt_content
                    cnt += 1
            elif Quest_dict[tempt] == 7 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt])
                tmp['items'] = Code_problem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                problem_lst.append(t)
    print(problem_lst)
    course_name = request.data.get('name') # course name 가져오기
    professor_user_name = request.user.username # professor username 가져오기
    professor_user_id = request.user.id # professor username 가져오기
    lecture = professor_lecture.objects.filter(name=course_name, username=professor_user_name).first()
    obj = problem(problem_1 = problem_lst[0], problem_2 = problem_lst[1] , problem_3 = problem_lst[2], problem_4 = problem_lst[3], problem_5 = problem_lst[4], problem_6 = problem_lst[5], problem_7 = problem_lst[6], problem_8 = problem_lst[7], problem_9 = problem_lst[8], problem_10 = problem_lst[9], lecture_id = lecture.id, professor_id = professor_user_id)
    obj.save()
    print(ans)
    return Response(ans, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def course_view(request):
    all_courses = course.objects.all()
    rtr = dict()
    rtr['lecture'] = []
    user_name = request.user.username
    for i in all_courses:
        tempt = dict()
        tempt['key'] = i.id
        tempt['name'] = i.name
        obj = professor_lecture.objects.filter(username = user_name, course_name = i.name)
        if obj == None: 
            rtr['lecture'].append(tempt)
    return Response(rtr, status=status.HTTP_200_OK)
    
@api_view(['GET'])    
def lecture_show(request): ## my 강의 
    id = request.user.id
    username = request.user.username
    lecture = professor_lecture.objects.filter(username = username)
    if lecture:
        rtr = dict()
        rtr['lecture'] = []
        for k in lecture:
            rtr['lecture'].append({'course_name':k.course_name, 'course_id':k.course_id})
        return Response(rtr, status = 200)
    else:
        return Response({}, status = 201) # 강의가 없는 경우
    
    
@api_view(['POST'])   
def lecture_generate(request): ## my 강의 
    try:
        user_name = request.user.username
        coursename = request.data.get('subject')
        obj = course.obj.filter(name = coursename).first()
        pl = professor_lecture.objects.create(username = user_name, course_name = coursename, course_id = obj.id)
        pl.save()
        return Response({'message':'success'}, status = 200)
    except:
        print("강의생성 되지않음")
        return Response({'message':'fail'}, status = 444)
    
    
    
    
