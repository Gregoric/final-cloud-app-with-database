import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/', null=True)
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()


# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

#==============================================================================================================
# <HINT> Create a Question Model with:
    # Used to persist question content for a course
    # Has a One-To-Many (or Many-To-Many if you want to reuse questions) relationship with course
    # Has a grade point for each question
    # Has question content
    # Other fields and methods you would like to design
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)   # Foreign key to lesson
    question_text = models.TextField()                             # question text
    question_text = models.TextField()                             # question grade/mark

def __str__(self):                            #============caso der erro excluir esse bloco de código abaixo ==============          
        return self.question_text                                                                     

def get_grade_point(self):
        return self.grade_point

def set_grade_point(self, new_grade_point):
        self.grade_point = new_grade_point
        self.save()

def get_course(self):
        return self.course

def set_course(self, new_course):
        self.course = new_course
        self.save()

def get_question_text(self):
        return self.question_text

def set_question_text(self, new_question_text):
        self.question_text = new_question_text
        self.save()  

class Meta:
        verbose_name_plural = 'Questions'
#============================================================================================
# <HINT> A sample model method to calculate if learner get the score of the question
def is_get_score(self, selected_ids):
    all_answers = self.choice_set.filter(is_correct=True).count()
    selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
    if all_answers == selected_correct:
        return True
    else:
        return False

#==========================================================================================
#  <HINT> Create a Choice Model with:
    # Used to persist choice content for a question
    # One-To-Many (or Many-To-Many if you want to reuse choices) relationship with Question
    # Choice content
    # Indicate if this choice of the question is a correct one or not
    # Other fields and methods you would like to design
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text

    def get_choice_text(self):
        return self.choice_text

    def set_choice_text(self, new_choice_text):
        self.choice_text = new_choice_text
        self.save()

    def get_is_correct(self):
        return self.is_correct

    def set_is_correct(self, new_is_correct):
        self.is_correct = new_is_correct
        self.save()

    def get_question(self):
        return self.question

    def set_question(self, new_question):
        self.question = new_question
        self.save()

    class Meta:
        verbose_name_plural = 'Choices'

#=============================================================================================
# <HINT> The submission model
# One enrollment could have multiple submission
# One submission could have multiple choices
# One choice could belong to multiple submissions
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
#    Other fields and methods you would like to design
    def __str__(self):
        return f'Submission {self.pk}'

    def get_enrollment(self):
        return self.enrollment

    def set_enrollment(self, new_enrollment):
        self.enrollment = new_enrollment
        self.save()

    def get_choices(self):
        return self.choices.all()

    def add_choice(self, choice):
        self.choices.add(choice)
        self.save()

    def remove_choice(self, choice):
        self.choices.remove(choice)
        self.save()

    class Meta:
        verbose_name_plural = 'Submissions'