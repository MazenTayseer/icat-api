from functools import wraps
from unittest.mock import Mock, patch


def mock_phishing_clients(test_func):
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        with (
            patch('common.tasks.tasks.OllamaClient') as mock_ollama_class,
            patch('common.tasks.tasks.MailerClient') as mock_mailer_class
        ):

            mock_mailer_instance = Mock()
            mock_ollama_instance = Mock()
            mock_mailer_class.return_value = mock_mailer_instance
            mock_ollama_class.return_value = mock_ollama_instance

            mock_ollama_instance.chat.return_value = "Dear <<NAME>>, test phishing email content"
            mock_mailer_instance.send_email.return_value = None

            return test_func(
                self,
                mock_mailer_instance,
                mock_ollama_instance,
                *args,
                **kwargs
            )
    return wrapper


def mock_ollama_for_assessment(test_func):
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        with patch('apps.dashboard.rest.serializers.user_assessment.OllamaClient') as mock_ollama_class:
            mock_ollama_instance = Mock()
            mock_ollama_class.return_value = mock_ollama_instance
            mock_ollama_instance.chat.return_value = {
            "scores": [
                {
                    "id": "uuid-1",
                    "score": 0,
                    "explanation": "Option A is wrong because sending any amount of money without verification first could be a scam."
                },
                {
                    "id": "uuid-2",
                    "score": 0,
                    "explanation": "Option A is wrong because clicking on suspicious links can lead to phishing attacks where your credentials are stolen. Option B is the correct approach, as using the retailer\u2019s own app ensures a safer login process."
                },
                {
                    "id": "uuid-3",
                    "score": 0.75,
                    "explanation": "You mentioned not doing anything but it would be better to take steps first: check with staff and ensure you're on their official website before making any payments."
                }
            ],
            "overall": {
                "score": 1.75,
                "max_score": 3.0,
                "percentage": 58,
                "feedback": "You demonstrated a good understanding of not taking immediate actions in phishing scenarios, but there's room for improvement by following specific steps like checking with staff and verifying the website."
            }
            }
            return test_func(self, mock_ollama_instance, *args, **kwargs)
    return wrapper
