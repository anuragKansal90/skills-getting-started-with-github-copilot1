def test_get_activities_returns_all_activities(client):
    """Test GET /activities returns all activities with correct structure"""
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Basketball Team"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_activity_names
    assert "description" in activities["Chess Club"]
    assert "participants" in activities["Chess Club"]


def test_get_root_redirects_to_static_index(client):
    """Test GET / redirects to /static/index.html"""
    # Arrange (implicit)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_signup_for_activity_success(client):
    """Test POST /signup successfully adds participant to activity"""
    # Arrange
    activity_name = "Basketball Team"
    email = "john@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    # Verify participant was actually added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_already_registered_returns_400(client):
    """Test POST /signup returns 400 when student already signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test POST /signup returns 404 when activity doesn't exist"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_from_activity_success(client):
    """Test POST /unregister successfully removes participant from activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    # Verify participant was actually removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_not_registered_returns_400(client):
    """Test POST /unregister returns 400 when student not signed up"""
    # Arrange
    activity_name = "Basketball Team"
    email = "notregistered@mergington.edu"  # Not registered
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test POST /unregister returns 404 when activity doesn't exist"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
