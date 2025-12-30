# Bug: nifi_970ddf8f_2025-10-15_20-31-44

## Summary
- Total patch files: **9**
- Unique patches: **7**
- Patch files missing `<patched>` blocks: **2**

## Patch files with no `<patched>` blocks
- `nifi_970ddf8f_2025-10-15_20-31-44/output_0/patch_raw_1.md`
- `nifi_970ddf8f_2025-10-15_20-31-44/output_0/patch_raw_2.md`

---

## Patch 1 (signature: `00323d47ad`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_2/patch_raw_2.md`

**Modifications:**

### `.../search_api.py`

**Block 1:**

```python
result = search_class(class_name="SNI")
```

**Block 2:**

```python
result = search_method_in_file(file_path="path/to/file", method_name="SNI checks")
```

---

## Patch 2 (signature: `43740a8c1d`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_2/patch_raw_0.md`

**Modifications:**

### `...`

```
...
```

---

## Patch 3 (signature: `5a6585631f`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_1/patch_raw_2.md`

**Modifications:**

### `replication.py`

**Block 1:**

```python
...
```

**Block 2:**

```python
def cleanUpHeaders(self):
    # code to clean up headers
    pass
```

---

## Patch 4 (signature: `6146c26c2f`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_1/patch_raw_1.md`

**Modifications:**

### `replication.py`

```python
def cleanUpHeaders(self, headers):...
```

---

## Patch 5 (signature: `755378777a`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_2/patch_raw_1.md`

**Modifications:**

### `search.py`

**Block 1:**

```python
result = search_class()
print(result)
```

**Block 2:**

```python
result = search_method_in_file(file_path="", method_name="")
print(result)
```

---

## Patch 6 (signature: `818f93c2f0`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_1/patch_raw_0.md`

**Modifications:**

### `.../replication.py`

```python
...
```

---

## Patch 7 (signature: `caa04a1977`)

**Source patch_raw files (duplicates):**
- `nifi_970ddf8f_2025-10-15_20-31-44/output_0/patch_raw_0.md`

**Modifications:**

### `.../request_replicator.py`

```python
def clean_up_headers(self, request):
    # code to clean up headers goes here
    pass
```

---

