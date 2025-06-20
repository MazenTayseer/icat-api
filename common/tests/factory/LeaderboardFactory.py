import factory

from apps.dal.models import Leaderboard, LeaderboardEntry
from apps.dal.models.enums.leaderboard_type import LeaderboardType
from common.tests.factory.UserFactory import UserFactory


class LeaderboardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Leaderboard

    type = LeaderboardType.GLOBAL

class LeaderboardEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeaderboardEntry

    leaderboard = factory.SubFactory(LeaderboardFactory)
    user = factory.SubFactory(UserFactory)
    total_score = factory.Faker('random_int', min=0, max=100)
