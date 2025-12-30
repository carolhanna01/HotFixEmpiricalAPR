# Bug: jackrabbit_6fb52bbc_2025-10-17_04-49-10

## Summary
- Total patch files: **9**
- Unique patches: **6**
- Patch files missing `<patched>` blocks: **3**

## Patch files with no `<patched>` blocks
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_1/patch_raw_0.md`
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_1/patch_raw_1.md`
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `0c81b905d4`)

**Source patch_raw files (duplicates):**
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_0/patch_raw_0.md`

**Modifications:**

### `.../ChangeLogRecord.py`

**Block 1:**

```python
def __init__(self): self = None
```

**Block 2:**

```python
except Exception as e:
```

---

## Patch 2 (signature: `198cbabbd7`)

**Source patch_raw files (duplicates):**
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_0/patch_raw_2.md`

**Modifications:**

### `.../ChangeLogRecord.py`

```python
class ChangeLogRecord:
    def __init__(self):
        self.record = None

    def get_record(self):
        if self.record is None:
            self.record = {}  # initialize the record here
        return self.record
```

---

## Patch 3 (signature: `1a6e265100`)

**Source patch_raw files (duplicates):**
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_2/patch_raw_2.md`

**Modifications:**

### `/path/to/jackrabbit/core.py`

```python
...
```

### `/path/to/jira/plugin.py`

```python
...
```

### `/path/to/jackrabbit/utils.py`

```python
...
```

---

## Patch 4 (signature: `51e9274f32`)

**Source patch_raw files (duplicates):**
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_0/patch_raw_1.md`

**Modifications:**

### `.../ChangeLogRecord.py`

```python
if change_log_record is not None:
```

---

## Patch 5 (signature: `fb74a92c86`)

**Source patch_raw files (duplicates):**
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_2/patch_raw_0.md`

**Modifications:**

### `.../models.py`

```python
class ChangeLogRecord:
```

### `.../views.py`

```python
def get_changes(request)::
```

---

## Patch 6 (signature: `ffc6a9a3fe`)

**Source patch_raw files (duplicates):**
- `jackrabbit_6fb52bbc_2025-10-17_04-49-10/output_2/patch_raw_1.md`

**Modifications:**

### `.../jira-development-integration-plugin.py`

```python
...
```

---

