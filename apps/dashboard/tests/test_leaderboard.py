
from apps.dashboard.tests.base import DashboardBaseTestCase
from common.tests.factory.LeaderboardFactory import (LeaderboardEntryFactory,
                                                     LeaderboardFactory)


class LeaderboardTestCases(DashboardBaseTestCase):
    def setUp(self):
        super().setUp()
        self.leaderboard_1 = LeaderboardFactory()
        LeaderboardEntryFactory(leaderboard=self.leaderboard_1)
        LeaderboardEntryFactory(leaderboard=self.leaderboard_1)


    def test_get_all_leaderboards(self):
        url = f"{self.dashboard_url}/leaderboard/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_leaderboard_detail(self):
        url = f"{self.dashboard_url}/leaderboard/{self.leaderboard_1.id}/"
        response = self.send_auth_request("get", url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("id"), self.leaderboard_1.id)
        self.assertEqual(response.data.get("name"), self.leaderboard_1.name)
        self.assertEqual(len(response.data.get("users")), 2)
        self.assertTrue(
            response.data.get("users")[0].get("total_score") >= response.data.get("users")[1].get("total_score")
        )
