import os
import pytest
import requests
from dotenv import load_dotenv
import urllib3

load_dotenv()

# Suppress SSL warnings for self-signed certificates (dev/testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== GLOBAL CONFIGURATION ====================
BASE_URL = os.getenv("BASE_URL", "https://devsfit.vvdntech.com/api-node")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
VERIFY_SSL = os.getenv("VERIFY_SSL", "false").lower() == "true"

COMMON_HEADERS = {
    "Content-Type": "application/json"
}

# ==================== TEST FUNCTIONS ====================
def test_tc001_get_unit_test_filenames_success():
    """TC001: Get Unit Test Filenames - Success | Expected: 200"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data
    assert "data" in response_data
    assert isinstance(response_data.get("data"), dict)
    data_dict = response_data.get("data", {})
    assert "userId" in data_dict
    assert "projectId" in data_dict
    assert "filenames" in data_dict
    assert isinstance(data_dict.get("filenames"), list)

def test_tc002_get_unit_test_filenames_missing_userid_parameter():
    """TC002: Get Unit Test Filenames - Missing userId Parameter | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc003_get_unit_test_filenames_missing_projectid_parameter():
    """TC003: Get Unit Test Filenames - Missing projectId Parameter | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc004_get_unit_test_filenames_both_required_parameters_missing():
    """TC004: Get Unit Test Filenames - Both Required Parameters Missing | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {}
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc005_get_unit_test_filenames_empty_string_userid():
    """TC005: Get Unit Test Filenames - Empty String userId | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc006_get_unit_test_filenames_empty_string_projectid():
    """TC006: Get Unit Test Filenames - Empty String projectId | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": ""
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc007_get_unit_test_filenames_data_not_found():
    """TC007: Get Unit Test Filenames - Data Not Found | Expected: 404"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_nonexistent"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 404, f"Expected 404, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc008_get_unit_test_filenames_missing_authorization_header():
    """TC008: Get Unit Test Filenames - Missing Authorization Header | Expected: 401"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data

def test_tc009_get_unit_test_filenames_invalid_jwt_token():
    """TC009: Get Unit Test Filenames - Invalid JWT Token | Expected: 401"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer invalid_token_xyz"}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert data.get("success") is False
    assert "message" in data

def test_tc010_get_unit_test_filenames_expired_jwt_token():
    """TC010: Get Unit Test Filenames - Expired JWT Token | Expected: 401"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer expired_token_xyz"}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert data.get("success") is False
    assert "message" in data

def test_tc011_get_unit_test_filenames_malformed_authorization_header_no_bearer_prefix():
    """TC011: Get Unit Test Filenames - Malformed Authorization Header (No Bearer Prefix) | Expected: 401"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 401, f"Expected 401, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert data.get("success") is False
    assert "message" in data

def test_tc012_get_unit_test_filenames_whitespace_only_userid():
    """TC012: Get Unit Test Filenames - Whitespace-only userId | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "   ",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert data.get("success") is False
    assert "message" in data

def test_tc013_get_unit_test_filenames_whitespace_only_projectid():
    """TC013: Get Unit Test Filenames - Whitespace-only projectId | Expected: 400"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "   "
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 400, f"Expected 400, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert data.get("success") is False
    assert "message" in data

def test_tc014_get_unit_test_filenames_extra_query_parameter():
    """TC014: Get Unit Test Filenames - Extra Query Parameter | Expected: 200"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456",
      "extraParam": "shouldBeIgnored"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert data.get("success") is True
    assert "message" in data

def test_tc015_get_unit_test_filenames_response_schema_validation():
    """TC015: Get Unit Test Filenames - Response Schema Validation | Expected: 200"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code} | {response.text[:200]}"
    data = response.json()
    assert isinstance(data.get("success"), bool)
    assert isinstance(data.get("message"), str)
    assert "data" in data
    response_data = data.get("data", {})
    assert isinstance(response_data.get("userId"), str)
    assert isinstance(response_data.get("projectId"), str)
    assert isinstance(response_data.get("sessionId"), str)
    assert isinstance(response_data.get("name"), str)
    assert isinstance(response_data.get("repo_url"), str)
    assert isinstance(response_data.get("filenames"), list)

def test_tc016_get_unit_test_filenames_performance_load_test():
    """TC016: Get Unit Test Filenames - Performance Load Test | Expected: 200"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_abc123",
      "projectId": "proj_xyz456"
    }
    for i in range(50):
        response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
        assert response.status_code == 200, f"Expected 200 on run {i+1}, got {response.status_code} | {response.text[:200]}"
        data = response.json()
        assert data.get("success") is True

def test_tc017_get_unit_test_filenames_large_filenames_array():
    """TC017: Get Unit Test Filenames - Large Filenames Array | Expected: 200"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN}
    params = {
      "userId": "user_large_data",
      "projectId": "proj_large_data"
    }
    response = requests.get(url, headers=headers, params=params, verify=VERIFY_SSL)
    assert response.status_code == 200, f"Expected 200, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data

def test_tc018_save_unit_test_filenames_high_level_success():
    """TC018: Save Unit Test Filenames - High-Level Success | Expected: 201"""
    url = f"{BASE_URL}/unittestcases"
    headers = {**COMMON_HEADERS, "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {
      "userId": "user_abc123",
      "projectId": "proj_new123",
      "name": "New Module Tests",
      "repo_url": "https://github.com/acme/new-feature",
      "filenames": [
        "src/feature/new.js",
        "src/feature/utils.js"
      ]
    }
    response = requests.post(url, headers=headers, json=payload, verify=VERIFY_SSL)
    assert response.status_code == 201, f"Expected 201, got {response.status_code} | {response.text[:200]}"
    response_data = response.json()
    assert "success" in response_data
    assert "message" in response_data