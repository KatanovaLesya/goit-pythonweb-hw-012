
from services.email_service import send_email
from unittest.mock import patch, MagicMock

@patch("smtplib.SMTP")
def test_send_email(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email("to@example.com", "Test Subject", "Hello Body")

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
