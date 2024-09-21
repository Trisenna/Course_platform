from django.shortcuts import render

from student.models import *

#查询某个学生的所有课程
def my_course_list(request, s_id):
    courses = Course.objects.filter(C_id__in=StudentCourse.objects.filter(S_id=s_id).values('C_id'))
    # 这里你可以返回一个渲染后的页面或者 JSON 数据
    return {'courses': list(courses.values('name'))}


#查询某个学生的所有通知
def my_notice(request, s_id):
    notices = Information.objects.filter(I_id__in=Releasement.objects.filter(S_id=s_id).values('I_id'))
    return {'notices': list(notices.values('content'))}


#查询某个学生的所有笔记，s_id为查询者id，b_id为被查询者id
def my_note(request, s_id, b_id):
    notes = Note.objects.filter(N_id__in=StudentNote.objects.filter(S_id=b_id, type=1).values('N_id'))
    personal_notes = Note.objects.filter(N_id__in=StudentNote.objects.filter(S_id=s_id).values('N_id'))

    combined_notes = list(notes) + list(personal_notes)
    return {'notes': list(map(lambda n: n.addr, combined_notes))}

#批量导入学生信息
def import_student(request):
