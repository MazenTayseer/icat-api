from functools import wraps
from unittest.mock import Mock, patch


def mock_phishing_clients(test_func):
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        with (
            patch('common.tasks.tasks.GeminiClient') as mock_gemini_class,
            patch('common.tasks.tasks.MailerClient') as mock_mailer_class
        ):

            mock_mailer_instance = Mock()
            mock_gemini_instance = Mock()
            mock_mailer_class.return_value = mock_mailer_instance
            mock_gemini_class.return_value = mock_gemini_instance

            mock_gemini_instance.chat.return_value = "Dear <<NAME>>, test phishing email content"
            mock_mailer_instance.send_email.return_value = None

            return test_func(
                self,
                mock_mailer_instance,
                mock_gemini_instance,
                *args,
                **kwargs
            )
    return wrapper


def mock_gemini_for_assessment(test_func):
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        with patch('apps.dashboard.rest.serializers.user_assessment.GeminiClient') as mock_gemini_class:
            mock_gemini_instance = Mock()
            mock_gemini_class.return_value = mock_gemini_instance
            mock_gemini_instance.chat.return_value = {
                'scores': [
                    {'id': '725f9300-0b12-4e21-9689-2348c473d221', 'score': 1.0, 'explanation': 'Correct.'},
                    {'id': 'ec4877e3-481b-42af-b35f-5c9b31245d37', 'score': 1.5, 'explanation': 'You correctly identified the risk of phishing or malware. To make your answer even better, consider suggesting verifying links before clicking or explaining how attackers trick users into revealing information.'},
                    {'id': '02b7ac22-1136-46b5-94d2-daa195262f16', 'score': 2.0, 'explanation': 'Great job! You nailed both the use of strong passwords and enabling two-factor authentication as key ways to protect your online accounts.'}
                ],
                'overall': {
                    'essay_total_score': 3.5,
                    'feedback': "You've got a solid grasp of password security and recognizing phishing risks. To enhance your skills, delve deeper into how attackers manipulate users and strategies for verifying suspicious links. Keep up the great work!"
                }
            }
            return test_func(self, mock_gemini_instance, *args, **kwargs)
    return wrapper
