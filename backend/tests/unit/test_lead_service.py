import pytest
from unittest.mock import Mock
from app.services.lead_service import LeadService
from app.exceptions import LeadNotFound, DuplicateEmail, InvalidStatus
from app.models.lead import Lead
from app.models.enums import LeadStatus

@pytest.fixture
def mock_lead_repo():
    return Mock()

@pytest.fixture
def lead_service(mock_lead_repo):
    return LeadService(lead_repository=mock_lead_repo)

# --- CREATE LEAD ---

def test_create_lead_success(lead_service, mock_lead_repo):
    # Arrange
    mock_lead_repo.get_by_email.return_value = None
    expected_lead = Lead(id=1, name="John Doe", email="john@example.com", status=LeadStatus.NEW.value)
    mock_lead_repo.create.return_value = expected_lead

    # Act
    result = lead_service.create_lead(name="John Doe", email="john@example.com", company="Acme Inc", phone="123456")

    # Assert
    assert result == expected_lead
    mock_lead_repo.get_by_email.assert_called_once_with("john@example.com")
    mock_lead_repo.create.assert_called_once()
    created_lead = mock_lead_repo.create.call_args[0][0]
    assert created_lead.name == "John Doe"
    assert created_lead.email == "john@example.com"
    assert created_lead.status == LeadStatus.NEW.value
    assert created_lead.company == "Acme Inc"
    assert created_lead.phone == "123456"

def test_create_lead_raises_duplicate_email(lead_service, mock_lead_repo):
    # Arrange
    existing_lead = Lead(id=1, name="John Doe", email="john@example.com")
    mock_lead_repo.get_by_email.return_value = existing_lead

    # Act & Assert
    with pytest.raises(DuplicateEmail) as exc_info:
        lead_service.create_lead(name="John Duplicate", email="john@example.com")
        
    assert "already registered" in str(exc_info.value)
    mock_lead_repo.get_by_email.assert_called_once_with("john@example.com")
    mock_lead_repo.create.assert_not_called()

# --- GET LEAD ---

def test_get_lead_success(lead_service, mock_lead_repo):
    # Arrange
    expected_lead = Lead(id=1, name="John Doe", email="john@example.com")
    mock_lead_repo.get_by_id.return_value = expected_lead

    # Act
    result = lead_service.get_lead(1)

    # Assert
    assert result == expected_lead
    mock_lead_repo.get_by_id.assert_called_once_with(1)

def test_get_lead_not_found(lead_service, mock_lead_repo):
    # Arrange
    mock_lead_repo.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(LeadNotFound) as exc_info:
        lead_service.get_lead(99)
        
    assert "not found" in str(exc_info.value)
    mock_lead_repo.get_by_id.assert_called_once_with(99)

# --- UPDATE LEAD ---

def test_update_lead_success_all_fields(lead_service, mock_lead_repo):
    # Arrange
    existing_lead = Lead(id=1, name="John Doe", email="john@example.com", status=LeadStatus.NEW.value)
    mock_lead_repo.get_by_id.return_value = existing_lead
    mock_lead_repo.get_by_email.return_value = None
    
    updated_lead_state = Lead(id=1, name="John Smith", email="john.smith@example.com", company="New Co", phone="987654", status=LeadStatus.CONTACTED.value)
    mock_lead_repo.update.return_value = updated_lead_state

    # Act
    result = lead_service.update_lead(
        lead_id=1,
        name="John Smith",
        email="john.smith@example.com",
        company="New Co",
        phone="987654",
        status="CONTACTED"
    )

    # Assert
    assert result == updated_lead_state
    mock_lead_repo.get_by_id.assert_called_once_with(1)
    mock_lead_repo.get_by_email.assert_called_once_with("john.smith@example.com")
    mock_lead_repo.update.assert_called_once_with(existing_lead)

def test_update_lead_email_duplicate(lead_service, mock_lead_repo):
    # Arrange
    existing_lead = Lead(id=1, name="John Doe", email="john@example.com")
    other_lead = Lead(id=2, name="Alice", email="alice@example.com")
    mock_lead_repo.get_by_id.return_value = existing_lead
    mock_lead_repo.get_by_email.return_value = other_lead

    # Act & Assert
    with pytest.raises(DuplicateEmail):
        lead_service.update_lead(lead_id=1, email="alice@example.com")
        
    mock_lead_repo.get_by_email.assert_called_once_with("alice@example.com")
    mock_lead_repo.update.assert_not_called()

def test_update_lead_invalid_status(lead_service, mock_lead_repo):
    # Arrange
    existing_lead = Lead(id=1, name="John Doe", email="john@example.com", status=LeadStatus.NEW.value)
    mock_lead_repo.get_by_id.return_value = existing_lead

    # Act & Assert
    with pytest.raises(InvalidStatus) as exc_info:
        lead_service.update_lead(lead_id=1, status="SUPER_QUALIFIED")
        
    assert "not allowed" in str(exc_info.value)
    mock_lead_repo.update.assert_not_called()

# --- LIST LEADS ---

def test_list_leads(lead_service, mock_lead_repo):
    # Arrange
    expected_list = [Lead(id=1), Lead(id=2)]
    mock_lead_repo.list.return_value = expected_list

    # Act
    result = lead_service.list_leads(status="NEW", query="Acme", skip=10, limit=20)

    # Assert
    assert result == expected_list
    mock_lead_repo.list.assert_called_once_with(status="NEW", query="Acme", skip=10, limit=20)

# --- DELETE LEAD ---

def test_delete_lead_success(lead_service, mock_lead_repo):
    # Arrange
    existing_lead = Lead(id=1, name="John Doe", email="john@example.com")
    mock_lead_repo.get_by_id.return_value = existing_lead

    # Act
    lead_service.delete_lead(1)

    # Assert
    mock_lead_repo.get_by_id.assert_called_once_with(1)
    mock_lead_repo.delete.assert_called_once_with(1)

def test_delete_lead_not_found(lead_service, mock_lead_repo):
    # Arrange
    mock_lead_repo.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(LeadNotFound):
        lead_service.delete_lead(99)
        
    mock_lead_repo.delete.assert_not_called()

# --- GET METRICS ---

def test_get_metrics(lead_service, mock_lead_repo):
    # Arrange
    repo_metrics = {"NEW": 5, "QUALIFIED": 3}
    mock_lead_repo.get_metrics.return_value = repo_metrics

    # Act
    result = lead_service.get_metrics()

    # Assert
    assert result == {
        "NEW": 5,
        "CONTACTED": 0,
        "QUALIFIED": 3,
        "LOST": 0
    }
    mock_lead_repo.get_metrics.assert_called_once()
