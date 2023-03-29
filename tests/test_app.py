import unittest

from src.app import create_app


class TestApp(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client()

    def test_index(self):

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("<title>LambdaTest</title>", html)

    def test_about(self):

        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("<title>About</title>", html)

    # def test_dashboard(self):

    #     response = self.client.get("/dashboard")
    #     self.assertEqual(response.status_code, 200)
    #     html = response.get_data(as_text=True)
    #     self.assertIn("<title>Dashboard</title>", html)

    # def test_dashboard_day(self):

    #     day = 0
    #     route = f"/dashboard/day"
    #     response = self.client.get(f"{route}/{day}")
    #     # redirects to same page when day == 0 and defaults to 1 if no data was provided
    #     self.assertEqual(response.status_code, 302)
    #     html = response.get_data(as_text=True)
    #     self.assertIn(
    #         f'You should be redirected automatically to the target URL: <a href="{route}/{1}">{route}/{1}</a>',
    #         html,
    #     )

    #     day = 1
    #     response = self.client.get(f"/dashboard/day/{day}")
    #     self.assertEqual(response.status_code, 200)
    #     html = response.get_data(as_text=True)
    #     self.assertIn(
    #         f"<title>Dashboard at day {day}</title>",
    #         html,
    #     )

    #     day = 366
    #     response = self.client.get(f"/dashboard/day/{day}")
    #     self.assertEqual(response.status_code, 302)
    #     html = response.get_data(as_text=True)
    #     # redirects to dashboard page when day > 365
    #     self.assertIn(
    #         'You should be redirected automatically to the target URL: <a href="/dashboard">/dashboard</a>',
    #         html,
    #     )
