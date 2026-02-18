import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from modules.user_mgmt.sub_modules import audit, groups, users
from utils import scripts


# Fixtures
@pytest.fixture(scope="session")
def project_root():
    """Fixture for project root directory."""
    return str(Path(__file__).parent.parent.parent.parent)


@pytest.fixture(scope="class")
def test_group_name():
    """Fixture for test group name."""
    return "test_group_cyber"


@pytest.fixture(scope="class")
def test_username():
    """Fixture for test username."""
    return "test_user_cyber"


@pytest.fixture
def existing_user():
    """Fixture for an existing user to test with."""
    return "root"


# Shell Script Tests
class TestShellScripts:
    """Test shell scripts to ensure they execute without errors."""

    def test_list_users_script(self, project_root):
        """Test list_users.sh script execution."""
        result = scripts.run_script("modules/user_mgmt/shell/list_users.sh", cwd=project_root)
        assert result['returncode'] == 0, "list_users.sh failed to execute"
        assert result['stdout'], "list_users.sh returned empty output"

    def test_list_groups_script(self, project_root):
        """Test list_groups.sh script execution."""
        result = scripts.run_script("modules/user_mgmt/shell/list_groups.sh", cwd=project_root)
        assert result['returncode'] == 0, "list_groups.sh failed to execute"
        assert result['stdout'], "list_groups.sh returned empty output"

    def test_group_members_script(self, project_root, existing_user):
        """Test group_members.sh script execution."""
        result = scripts.run_script("modules/user_mgmt/shell/group_members.sh", "root", cwd=project_root)
        assert result['returncode'] == 0, "group_members.sh failed to execute"

    def test_user_exists_script(self, project_root, existing_user):
        """Test user_exists.sh script execution."""
        result = scripts.run_script("modules/user_mgmt/shell/user_exists.sh", existing_user, cwd=project_root)
        assert result['returncode'] == 0, f"user_exists.sh failed for user {existing_user}"


# Audit Tests
class TestAudits:
    """Test audit functions for users and groups."""

    def test_audit_users(self):
        """Test audit_users function."""
        expected_users = ["root", "nobody"]
        user_audit = audit.audit_users(expected_users)

        assert "found_users" in user_audit, "Missing 'found_users' key"
        assert "missing_users" in user_audit, "Missing 'missing_users' key"
        assert "unexpected_users" in user_audit, "Missing 'unexpected_users' key"
        assert isinstance(user_audit['found_users'], list), "'found_users' should be a list"
        assert isinstance(user_audit['missing_users'], list), "'missing_users' should be a list"
        assert isinstance(user_audit['unexpected_users'], list), "'unexpected_users' should be a list"

    def test_audit_groups(self):
        """Test audit_groups function."""
        expected_groups = ["root", "sudo", "adm"]
        group_audit = audit.audit_groups(expected_groups)

        assert "found_groups" in group_audit, "Missing 'found_groups' key"
        assert "missing_groups" in group_audit, "Missing 'missing_groups' key"
        assert "unexpected_groups" in group_audit, "Missing 'unexpected_groups' key"
        assert isinstance(group_audit['found_groups'], list), "'found_groups' should be a list"
        assert isinstance(group_audit['missing_groups'], list), "'missing_groups' should be a list"
        assert isinstance(group_audit['unexpected_groups'], list), "'unexpected_groups' should be a list"


# Group Management Tests (requires sudo)
@pytest.mark.sudo
class TestGroupManagement:
    """Test group management functions (requires sudo permissions)."""

    def test_create_group(self, test_group_name):
        """Test create_group function."""
        result = groups.create_group(test_group_name)
        assert result is True, f"Failed to create group {test_group_name}"

    def test_add_user_to_group(self, existing_user, test_group_name):
        """Test add_user_to_group function."""
        # Ensure group exists first
        groups.create_group(test_group_name)
        result = groups.add_user_to_group(existing_user, test_group_name)
        assert result is True, f"Failed to add user {existing_user} to group {test_group_name}"

    def test_remove_user_from_group(self, existing_user, test_group_name):
        """Test remove_user_from_group function."""
        # Ensure user is in group first
        groups.create_group(test_group_name)
        groups.add_user_to_group(existing_user, test_group_name)
        result = groups.remove_user_from_group(existing_user, test_group_name)
        assert result is True, f"Failed to remove user {existing_user} from group {test_group_name}"

    def test_delete_group(self, test_group_name):
        """Test delete_group function."""
        # Ensure group exists first
        groups.create_group(test_group_name)
        result = groups.delete_group(test_group_name)
        assert result is True, f"Failed to delete group {test_group_name}"


# User Management Tests (requires sudo)
@pytest.mark.sudo
class TestUserManagement:
    """Test user management functions (requires sudo permissions)."""

    def test_create_user(self, test_username):
        """Test create_user function."""
        result = users.create_user(test_username)
        assert result is True, f"Failed to create user {test_username}"

    def test_lock_user(self, test_username):
        """Test lock_user function."""
        # Ensure user exists first
        users.create_user(test_username)
        result = users.lock_user(test_username)
        assert result is True, f"Failed to lock user {test_username}"

    def test_delete_user(self, test_username):
        """Test delete_user function."""
        # Ensure user exists first
        users.create_user(test_username)
        result = users.delete_user(test_username)
        assert result is True, f"Failed to delete user {test_username}"


# Cleanup fixtures
@pytest.fixture(autouse=True, scope="class")
def cleanup_test_group(request, test_group_name):
    """Cleanup test group after all tests in class."""
    yield
    # Cleanup after tests
    try:
        groups.delete_group(test_group_name)
    except:
        pass


@pytest.fixture(autouse=True, scope="class")
def cleanup_test_user(request, test_username):
    """Cleanup test user after all tests in class."""
    yield
    # Cleanup after tests
    try:
        users.delete_user(test_username)
    except:
        pass


