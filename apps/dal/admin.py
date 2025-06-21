from django.contrib import admin

from apps.dal.models import (Assessment, EssayAnswerRubric, EssayQuestion,
                             McqAnswer, McqQuestion, Module, PhishingScenario,
                             Simulation, UserPhishingScenario)

# Register your models here.
admin.site.register(Module)
admin.site.register(Assessment)
admin.site.register(McqQuestion)
admin.site.register(EssayQuestion)
admin.site.register(McqAnswer)
admin.site.register(EssayAnswerRubric)
admin.site.register(Simulation)
admin.site.register(PhishingScenario)
admin.site.register(UserPhishingScenario)
