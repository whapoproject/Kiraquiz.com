from django.contrib import admin
from .models import Question, Answer, QuizType

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuizType)
