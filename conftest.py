import pytest
import allure

def pytest_addoption(parser):
    parser.addoption(
        "--login", 
        action="store", 
        default='username', 
        help="Login for authentication"
    )
    parser.addoption(
        "--password", 
        action="store", 
        default='password', 
        help="Password for authentication"
    )

@pytest.fixture
def login(request):
    return request.config.getoption("--login")

@pytest.fixture
def password(request):
    return request.config.getoption("--password")