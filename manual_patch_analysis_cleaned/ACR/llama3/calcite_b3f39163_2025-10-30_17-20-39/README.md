# Bug: calcite_b3f39163_2025-10-30_17-20-39

## Summary
- Total patch files: **9**
- Unique patches: **7**
- Patch files missing `<patched>` blocks: **2**

## Patch files with no `<patched>` blocks
- `calcite_b3f39163_2025-10-30_17-20-39/output_0/patch_raw_1.md`
- `calcite_b3f39163_2025-10-30_17-20-39/output_2/patch_raw_1.md`

---

## Patch 1 (signature: `150d223385`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_0/patch_raw_2.md`

**Modifications:**

### `.../auth.py`

```python
def authenticateUser(user_id):
    # Check if the user has the required role
    if not hasRole(user_id, 'admin'):
        return False

    # Recursively check for nested roles
    for role in getRoles(user_id):
        if hasRole(role, 'admin'):
            return True

    return False
```

### `.../role.py`

```python
def hasRole(user_id, role):
    # Check if the user has the specified role
    if getRole(user_id) == role:
        return True

    # Recursively check for nested roles
    for parent_role in getParentRoles(role):
        if hasRole(user_id, parent_role):
            return True

    return False
```

---

## Patch 2 (signature: `2e139de533`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_1/patch_raw_2.md`

**Modifications:**

### `/path/to/Jetty/ConstraintSecurityHandler.java`

```java
def isUserInRole(self, role):
```

---

## Patch 3 (signature: `47951d76a5`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_2/patch_raw_2.md`

**Modifications:**

### `...`

**Block 1:**

```
...
```

**Block 2:**

```
def isUserInRole(user, role):
    return any(r == role for r in user.getRoles())
```

---

## Patch 4 (signature: `77f5eb616e`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_1/patch_raw_0.md`

**Modifications:**

### `/path/to/Jetty/ConstraintSecurityHandler.java`

```java
if (realm.equalsIgnoreCase("default")) {
    return true;
}
```

---

## Patch 5 (signature: `c0c89dbadc`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_0/patch_raw_0.md`

**Modifications:**

### `.../user_authentication.py`

```python
def authenticateUser(username, password):
```

---

## Patch 6 (signature: `c69c01d188`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_2/patch_raw_0.md`

**Modifications:**

### `...`

```
...
```

### `security_handler.py`

```python
def isUserInRole(role): return True if role in [user_roles] else False
```

---

## Patch 7 (signature: `e3fb6cd8f6`)

**Source patch_raw files (duplicates):**
- `calcite_b3f39163_2025-10-30_17-20-39/output_1/patch_raw_1.md`

**Modifications:**

### `/path/to/Jetty/ConstraintSecurityHandler.java`

```java
def isUserInRole(self, role):
    if self._isSPNEGOAuthenticated():
        return True
    else:
        return False
```

---

