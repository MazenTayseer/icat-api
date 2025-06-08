from django.contrib import admin

from apps.dal.models import (Assessment, EssayAnswerRubric, EssayQuestion,
                             McqAnswer, McqQuestion, Module)

# Register your models here.
admin.site.register(Module)
admin.site.register(Assessment)
admin.site.register(McqQuestion)
admin.site.register(EssayQuestion)
admin.site.register(McqAnswer)
admin.site.register(EssayAnswerRubric)
