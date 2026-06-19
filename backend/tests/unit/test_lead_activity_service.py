import pytest
from unittest.mock import Mock
from app.services.lead_activity_service import LeadActivityService
from app.exceptions import LeadNotFound, InvalidActivityType
from app.models.lead import Lead
from app.models.lead_activity import LeadActivity
from app.models.enums import ActivityType

@pytest.fixture
def mock_lead_repo():
    return Mock()

@pytest.fixture
def mock_activity_repo():
    return Mock()

@pytest.fixture
def activity_service(mock_activity_repo, mock_lead_repo):
    return LeadActivityService(
        activity_repository=mock_activity_repo,
        lead_repository=mock_lead_repo
    )

# --- REGISTER ACTIVITY ---

def test_register_activity_success(activity_service, mock_lead_repo, mock_activity_repo):
    # Arrange
    lead = Lead(id=1, name="John Doe")
    mock_lead_repo.get_by_id.return_value = lead
    
    expected_activity = LeadActivity(id=10, lead_id=1, type=ActivityType.CALL.value, notes="Called the client")
    mock_activity_repo.create.return_value = expected_activity

    # Act
    result = activity_service.register_activity(lead_id=1, type="CALL", notes="Called the client")

    # Assert
    assert result == expected_activity
    mock_lead_repo.get_by_id.assert_called_once_with(1)
    mock_activity_repo.create.assert_called_once()
    created_act = mock_activity_repo.create.call_args[0][0]
    assert created_act.lead_id == 1
    assert created_act.type == ActivityType.CALL.value
    assert created_act.notes == "Called the client"

def test_register_activity_lead_not_found(activity_service, mock_lead_repo, mock_activity_repo):
    # Arrange
    mock_lead_repo.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(LeadNotFound) as exc_info:
        activity_service.register_activity(lead_id=99, type="CALL", notes="Some notes")
        
    assert "not found" in str(exc_info.value)
    mock_lead_repo.get_by_id.assert_called_once_with(99)
    mock_activity_repo.create.assert_not_called()

def test_register_activity_invalid_type(activity_service, mock_lead_repo, mock_activity_repo):
    # Arrange
    lead = Lead(id=1, name="John Doe")
    mock_lead_repo.get_by_id.return_value = lead

    # Act & Assert
    with pytest.raises(InvalidActivityType) as exc_info:
        activity_service.register_activity(lead_id=1, type="WHATSAPP", notes="Chatted on whatsapp")
        
    assert "not allowed" in str(exc_info.value)
    mock_lead_repo.get_by_id.assert_called_once_with(1)
    mock_activity_repo.create.assert_not_called()

# --- LIST ACTIVITIES ---

def test_list_activities_success(activity_service, mock_lead_repo, mock_activity_repo):
    # Arrange
    lead = Lead(id=1, name="John Doe")
    mock_lead_repo.get_by_id.return_value = lead
    
    expected_list = [LeadActivity(id=10, lead_id=1), LeadActivity(id=11, lead_id=1)]
    mock_activity_repo.list_by_lead_id.return_value = expected_list

    # Act
    result = activity_service.list_activities(1)

    # Assert
    assert result == expected_list
    mock_lead_repo.get_by_id.assert_called_once_with(1)
    mock_activity_repo.list_by_lead_id.assert_called_once_with(1)

def test_list_activities_lead_not_found(activity_service, mock_lead_repo, mock_activity_repo):
    # Arrange
    mock_lead_repo.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(LeadNotFound):
        activity_service.list_activities(99)
        
    mock_activity_repo.list_by_lead_id.assert_not_called()
