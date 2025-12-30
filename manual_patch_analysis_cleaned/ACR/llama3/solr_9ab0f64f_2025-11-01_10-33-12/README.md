# Bug: solr_9ab0f64f_2025-11-01_10-33-12

## Summary
- Total patch files: **9**
- Unique patches: **8**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `0ab29d4c0a`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_1/patch_raw_0.md`
- `solr_9ab0f64f_2025-11-01_10-33-12/output_1/patch_raw_1.md`

**Modifications:**

### `data_processing.py`

```python
def setInfoStream(self, info_stream):
    if info_stream:
        self.info_stream = info_stream
    else:
        raise ValueError("Invalid info stream")
```

---

## Patch 2 (signature: `3d35344d8b`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_2/patch_raw_0.md`

**Modifications:**

### `index_writer.py`

```python
def setInfoStream(self):
```

---

## Patch 3 (signature: `44176bac24`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_1/patch_raw_2.md`

**Modifications:**

### `data_processing.py`

```python
def setInfoStream(self, info_stream):
    if info_stream is None:
        raise ValueError("Invalid info stream")
    self.info_stream = info_stream
```

---

## Patch 4 (signature: `81b2495f8d`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_2/patch_raw_1.md`

**Modifications:**

### `index_writer.py`

```python
if not self.infoStream and not self.assertEnabled:
```

---

## Patch 5 (signature: `850af049d2`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_0/patch_raw_1.md`

**Modifications:**

### `dev-tools/scripts/addVersion.py`

```python
def add_version(version):...
```

### `dev-tools/scripts/scriptutil.py`

```python
def script_util():...
```

---

## Patch 6 (signature: `885bac1b1c`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_0/patch_raw_0.md`

**Modifications:**

### `dev-tools/scripts/addVersion.py`

```python
...
```

### `dev-tools/scripts/scriptutil.py`

```python
...
```

---

## Patch 7 (signature: `b19dde0152`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_0/patch_raw_2.md`

**Modifications:**

### `dev-tools/scripts/addVersion.py`

```python
def add_version(file_path):
    version = get_version()
    if file_path.endswith('.txt'):
        with open(file_path, 'w') as f:
            f.write(f'Version: {version}\n')
    else:
        print(f"Unsupported file type: {file_path}")
```

### `dev-tools/scripts/scriptutil.py`

```python
def script_util():
    if sys.argv[1].endswith('.txt'):
        with open(sys.argv[1], 'w') as f:
            f.write(f'Version: {get_version()}\n')
    else:
        print(f"Unsupported file type: {sys.argv[1]}")
```

---

## Patch 8 (signature: `ef0ede6778`)

**Source patch_raw files (duplicates):**
- `solr_9ab0f64f_2025-11-01_10-33-12/output_2/patch_raw_2.md`

**Modifications:**

### `index_writer.py`

```python
def setInfoStream(self, stream):
```

---

