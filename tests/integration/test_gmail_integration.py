"""
Integration tests for Gmail functionality.
"""
import pytest
from unittest.mock import MagicMock, patch
from utils.gmail_client import GmailClient
from agent.auth_manager import AuthManager

@pytest.fixture
def mock_gmail_service():
    """Mock Gmail service."""
    service = MagicMock()
    
    # Mock messages.list response
    service.users().messages().list.return_value.execute.return_value = {
        "messages": [
            {"id": "msg1"},
            {"id": "msg2"}
        ]
    }
    
    # Mock messages.get response
    def mock_get_message(userId, id):
        messages = {
            "msg1": {
                "id": "msg1",
                "snippet": "Test email 1",
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": "Test Subject 1"},
                        {"name": "From", "value": "sender1@test.com"}
                    ]
                }
            },
            "msg2": {
                "id": "msg2",
                "snippet": "Test email 2",
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": "Test Subject 2"},
                        {"name": "From", "value": "sender2@test.com"}
                    ]
                }
            }
        }
        mock_response = MagicMock()
        mock_response.execute.return_value = messages[id]
        return mock_response
    
    service.users().messages().get = mock_get_message
    return service

@pytest.fixture
def gmail_client(mock_gmail_service):
    """Create Gmail client with mocked service."""
    auth_manager = AuthManager()
    auth_manager.get_gmail_service = MagicMock(return_value=mock_gmail_service)
    return GmailClient(auth_manager)

def test_get_recent_emails(gmail_client):
    """Test fetching recent emails."""
    emails = gmail_client.get_recent_emails(max_results=2)
    
    assert len(emails) == 2
    assert emails[0]["subject"] == "Test Subject 1"
    assert emails[0]["from"] == "sender1@test.com"
    assert emails[1]["subject"] == "Test Subject 2"
    assert emails[1]["from"] == "sender2@test.com"

def test_search_emails(gmail_client):
    """Test searching emails."""
    emails = gmail_client.search_emails("test query", max_results=2)
    
    assert len(emails) == 2
    assert all("subject" in email for email in emails)
    assert all("from" in email for email in emails)

@pytest.mark.asyncio
async def test_batch_operations(gmail_client):
    """Test batch email operations."""
    message_ids = ["msg1", "msg2"]
    
    # Test archiving
    with patch.object(gmail_client.service.users().messages(), 'batchModify') as mock_batch:
        mock_batch.return_value.execute.return_value = {}
        result = gmail_client.archive_messages(message_ids)
        assert result is True
        mock_batch.assert_called_once()

    # Test marking as read
    with patch.object(gmail_client.service.users().messages(), 'batchModify') as mock_batch:
        mock_batch.return_value.execute.return_value = {}
        result = gmail_client.mark_as_read(message_ids)
        assert result is True
        mock_batch.assert_called_once() 