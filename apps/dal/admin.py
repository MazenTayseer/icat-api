from django.contrib import admin

from apps.dal.models import (Assessment, EssayAnswerRubric,
                             EssayAnswerSubmission, EssayQuestion, Leaderboard,
                             LeaderboardEntry, McqAnswer, McqAnswerSubmission,
                             McqQuestion, Module, PhishingScenario, Simulation,
                             UserAssessments, UserModule, UserPhishingScenario)

admin.site.register(Assessment)
admin.site.register(UserAssessments)
admin.site.register(McqAnswerSubmission)
admin.site.register(EssayAnswerSubmission)
admin.site.register(Module)
admin.site.register(UserModule)
admin.site.register(Simulation)
admin.site.register(Leaderboard)
admin.site.register(LeaderboardEntry)
admin.site.register(McqQuestion)
admin.site.register(EssayQuestion)
admin.site.register(McqAnswer)
admin.site.register(EssayAnswerRubric)
admin.site.register(PhishingScenario)
admin.site.register(UserPhishingScenario)
