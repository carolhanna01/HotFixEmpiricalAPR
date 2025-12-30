# Bug: ambari_8782442d_2025-10-31_11-49-55

## Summary
- Total patch files: **9**
- Unique patches: **6**
- Patch files missing `<patched>` blocks: **2**

## Patch files with no `<patched>` blocks
- `ambari_8782442d_2025-10-31_11-49-55/output_1/patch_raw_0.md`
- `ambari_8782442d_2025-10-31_11-49-55/output_2/patch_raw_2.md`

---

## Patch 1 (signature: `0d0b532aee`)

**Source patch_raw files (duplicates):**
- `ambari_8782442d_2025-10-31_11-49-55/output_2/patch_raw_0.md`

**Modifications:**

### `.../requests.py`

```python
...
    def filter_requests(requests):
        return [request for request in requests if request.status == 'IN_PROGRESS']
...
```

---

## Patch 2 (signature: `43740a8c1d`)

**Source patch_raw files (duplicates):**
- `ambari_8782442d_2025-10-31_11-49-55/output_1/patch_raw_1.md`
- `ambari_8782442d_2025-10-31_11-49-55/output_2/patch_raw_1.md`

**Modifications:**

### `...`

```
...
```

---

## Patch 3 (signature: `4cc75a176f`)

**Source patch_raw files (duplicates):**
- `ambari_8782442d_2025-10-31_11-49-55/output_0/patch_raw_1.md`

**Modifications:**

### `/path/to/file.py`

```python
def handle_request(request):
    if request.status == 'IN_PROGRESS':
        # return only last 20 IN_PROGRESS requests
        in_progress_requests = [req for req in requests if req.status == 'IN_PROGRESS']
        return in_progress_requests[-20:]
    else:
        # return only last 20 requests regardless of status
        all_requests = [req for req in requests]
        return all_requests[-20:]
```

---

## Patch 4 (signature: `a62f1f2265`)

**Source patch_raw files (duplicates):**
- `ambari_8782442d_2025-10-31_11-49-55/output_0/patch_raw_2.md`

**Modifications:**

### `/path/to/file.py`

```python
...
    def handle_request(self):
        # Modified code to return only the last 20 requests
        in_progress_requests = self.get_in_progress_requests()
        return in_progress_requests[-20:]
...
```

---

## Patch 5 (signature: `d88f0cd32b`) CH:SYMPTOM-HIDER

**Source patch_raw files (duplicates):**
- `ambari_8782442d_2025-10-31_11-49-55/output_1/patch_raw_2.md`

**Modifications:**

### `api.py`

```python
requests = Request.query.order_by(Request.created_at.desc()).limit(20).all()
```

---

## Patch 6 (signature: `f9ea816909`)

**Source patch_raw files (duplicates):**
- `ambari_8782442d_2025-10-31_11-49-55/output_0/patch_raw_0.md`

**Modifications:**

### `/path/to/file.py`

```python
def handle_request(request):
    if request.status == 'IN_PROGRESS':
        return [request]
    else:
        return []
```

---

