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

            mock_ollama_instance.chat.return_value = {
                "message": {"content": "Dear <<NAME>>, test phishing email content"}
            }
            mock_mailer_instance.send_email.return_value = None

            return test_func(
                self,
                mock_mailer_instance,
                mock_ollama_instance,
                *args,
                **kwargs
            )
    return wrapper
