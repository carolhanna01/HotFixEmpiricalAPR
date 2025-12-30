# Bug: ambari_58dabba1_2025-10-30_16-09-28

## Summary
- Total patch files: **9**
- Unique patches: **8**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `11b36076b7`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_2/patch_raw_1.md`

**Modifications:**

### `.../smoke_tests.py`

**Block 1:**

```python
if params.run_smoke_test:
    schedule_smoke_test()
    run_smoke_test()
```

**Block 2:**

```python
def handle_smoke_test_request(request):
    if request is not None and request.valid:
        run_smoke_test()
    else:
        pass
```

---

## Patch 2 (signature: `341b012404`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_0/patch_raw_1.md`

**Modifications:**

### `...`

```
if params.run_smoke_test:
    api_call_with_body({"RequestInfo": ..., "Body": {"ServiceInfo": ...}})
```

---

## Patch 3 (signature: `5fa6b13681`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_1/patch_raw_1.md`

**Modifications:**

### `.../path/to/file.py`

```python
def run_smoke_test():...
```

---

## Patch 4 (signature: `96e40b06a8`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_2/patch_raw_2.md`

**Modifications:**

### `.../smoke_tests.py`

**Block 1:**

```python
if params.run_smoke_test:
```

**Block 2:**

```python
def run_smoke_test(request): if request.is_valid:
```

---

## Patch 5 (signature: `b34467ad47`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_1/patch_raw_0.md`

**Modifications:**

### `path/to/file.py`

```python
def run_smoke_test():...
```

---

## Patch 6 (signature: `b4bcced072`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_1/patch_raw_2.md`

**Modifications:**

### `.../path/to/file.py`

```python
def run_smoke_test(params): if params.get('run_smoke_test', False): ...
```

---

## Patch 7 (signature: `e5938d9a4d`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_0/patch_raw_0.md`
- `ambari_58dabba1_2025-10-30_16-09-28/output_0/patch_raw_2.md`

**Modifications:**

### `...`

**Block 1:**

```
...
```

**Block 2:**

```
...
```

---

## Patch 8 (signature: `ed037a23fd`)

**Source patch_raw files (duplicates):**
- `ambari_58dabba1_2025-10-30_16-09-28/output_2/patch_raw_0.md`

**Modifications:**

### `.../smoke_tests.py`

**Block 1:**

```python
if params.run_smoke_test:
```

**Block 2:**

```python
if request.is_valid():
```

---

