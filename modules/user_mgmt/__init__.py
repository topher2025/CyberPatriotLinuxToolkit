"""
User management package.

Responsible for:
- User existence and lifecycle
- Group creation and membership
- Auditing users and groups

Does NOT handle:
- Sudo or admin privileges
- File permissions or ownership
- Password or authentication policy
"""

from modules.user_mgmt.sub_modules.users import (
    list_users,
    user_exists,
    create_user,
    lock_user,
    delete_user,
)

from modules.user_mgmt.sub_modules.groups import (
    group_exists,
    create_group,
    add_user_to_group,
    remove_user_from_group,
)

from modules.user_mgmt.sub_modules.audit import (
    audit_users,
    audit_groups,
)

__all__ = [
    # users
    "list_users",
    "user_exists",
    "create_user",
    "lock_user",
    "delete_user",
    # groups
    "group_exists",
    "create_group",
    "add_user_to_group",
    "remove_user_from_group",
    # audit
    "audit_users",
    "audit_groups",
]
