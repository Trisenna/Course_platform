import os

from django.db import models

#学生
class Student(models.Model):
    S_id = models.IntegerField(primary_key=True)
    account = models.CharField(max_length=200, null=True, blank=True,unique=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    attention_num = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Student ID: {self.S_id}"


#回复
class Reply(models.Model):
    R_id = models.IntegerField(primary_key=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Reply ID: {self.R_id}"

#课程
class Course(models.Model):
    C_id = models.AutoField(primary_key=True,auto_created=True)
    introduction = models.CharField(max_length=1000, null=True, blank=True)
    Syllabus = models.FileField( null=True, blank=True)
    calendar = models.FileField( null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    #时段1-8
    period = models.IntegerField(null=True, blank=True)
    #学分
    credit = models.IntegerField(null=True, blank=True)
    #学时
    hours = models.IntegerField(null=True, blank=True)
    #上课地点
    place = models.CharField(max_length=100, null=True, blank=True)

    #重写save方法
    def save(self, *args, **kwargs):
        if self.C_id:
            username = self.C_id.__str__()  # 获取用户名
            # 设置文件的上传路径
            self.Syllabus.name = os.path.join('Course','Syllabus', username, self.Syllabus.name)
            self.calendar.name = os.path.join('Course','calendar', username, self.calendar.name)
        super().save(*args, **kwargs )




    def __str__(self):
        return f"Course ID: {self.C_id}"

#学生关注学生
class StudentStudent(models.Model):
    S_id = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='followers', null=True, blank=True)
    follow = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='following', null=True, blank=True)


    def __str__(self):
        return f"Follower ID: {self.S_id}, Followed ID: {self.follow}"


#学生上课课程
class StudentCourse(models.Model):
    S_id = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    C_id = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Student ID: {self.S_id}, Course ID: {self.C_id}"


#资源，type为资源类型，0为课件，1为试题，2为习题
class Resource(models.Model):
    R_id = models.AutoField(primary_key=True,auto_created=True)
    file= models.FileField(upload_to='resource/', null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return f"Resource ID: {self.R_id}"










#老师讲课
class CourseTeacher(models.Model):
    C_id = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    T_id = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return f"Course ID: {self.C_id}, Teacher ID: {self.T_id}"

#课程的资源
class CourseResource(models.Model):
    R_id = models.ForeignKey('Resource', on_delete=models.CASCADE, null=True, blank=True)
    C_id = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Course ID: {self.C_id}, Resource ID: {self.R_id}"


#讨论贴
class Discuss(models.Model):
    D_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=1000, null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Discuss ID: {self.D_id}"


#学生完成作业
class DoWork(models.Model):
    S_id = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    W_id = models.ForeignKey('Work', on_delete=models.CASCADE, null=True, blank=True)
    C_id = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    T_id = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)
    is_push = models.BooleanField(default=False, null=True, blank=True)
    file = models.FileField(upload_to='work/students', null=True, blank=True)
    score = models.IntegerField(null=True, blank=True,default=0)

    def save(self, *args, **kwargs):
        if self.W_id and self.file:
            username = getattr(self.S_id, 'account', '')  # 使用account作为用户名
            work_id = str(self.W_id.W_id)  # 确保work_id是一个字符串

            # 检查变量是否为None，并提供默认值
            if username is None:
                username = ''
            if work_id is None:
                work_id = ''
            if self.file.name is None:
                self.file.name = ''

            # 使用有效的字符串值拼接文件名
            self.file.name = os.path.join( work_id, username, self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Do Work ID: {self.W_id}"



    def __str__(self):
        return f"Do Work ID: {self.W_id}"



#作业
class Work(models.Model):
    W_id = models.AutoField(primary_key=True,auto_created=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    content = models.FileField(upload_to='work/teacher', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Work ID: {self.W_id}"




#教师
class Teacher(models.Model):
    T_id = models.AutoField(primary_key=True,auto_created=True)
    account = models.CharField(max_length=20, null=True, blank=True)
    passward = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Teacher ID: {self.T_id}"





#讨论贴的回复
class DiscussReply(models.Model):
    D_id = models.ForeignKey('Discuss', on_delete=models.CASCADE, null=True, blank=True)
    R_id = models.ForeignKey('Reply', on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return f"Discuss ID: {self.D_id}, Reply ID: {self.R_id}"



#课程的讨论贴
class DisCou(models.Model):
    C_id = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    D_id = models.ForeignKey('Discuss', on_delete=models.CASCADE, null=True, blank=True)



    def __str__(self):
        return f"Course ID: {self.C_id}, Discuss ID: {self.D_id}"
#通知
class Information(models.Model):
    I_id = models.AutoField(primary_key=True,auto_created=True)
    content = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f"Informaiton ID: {self.I_id}"
#发布通知，0是系统通知，1是老师发布的课程通知
class Releasement(models.Model):
    R_id = models.AutoField(primary_key=True,auto_created=True)
    I_id = models.ForeignKey('Information', on_delete=models.CASCADE, null=True, blank=True)
    S_id = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    T_id = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=True, blank=True)
    C_id = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Releasement ID: {self.R_id}"
#收藏夹
class Favorite(models.Model):
    S_id = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    F_id = models.AutoField (primary_key=True, unique=True,auto_created=True)
    type = models.IntegerField(null=True, blank=True)
    #链接到F_id
    link = models.ForeignKey('Favorite', on_delete=models.CASCADE, null=True, blank=True)
    follow_num = models.IntegerField(null=True, blank=True,default=0)
    like_num = models.IntegerField(null=True, blank=True,default=0)

    def __str__(self):
        return f"Favorite ID: {self.name}"


class Note(models.Model):
    N_id = models.AutoField(primary_key=True,auto_created=True)
    file = models.FileField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    F_id = models.ForeignKey('Favorite', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.F_id:
            username = self.F_id.S_id.S_id.__str__()  # 获取用户名
            favorite_name = self.F_id.name  # 获取收藏夹名称

            # 设置文件的上传路径
            self.file.name = os.path.join('favorite', username, favorite_name, self.file.name)

        super().save(*args, **kwargs)



    def __str__(self):
        return f"Note ID: {self.N_id}"
#用户是否点赞了收藏夹
class Like(models.Model):
    S_id = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    F_id = models.ForeignKey('Favorite', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Student ID: {self.S_id}, Favorite ID: {self.F_id}"


















































