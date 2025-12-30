# Bug: flink_95b9adbe_2025-10-15_17-14-04

## Summary
- Total patch files: **9**
- Unique patches: **9**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `199d592dec`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_2/patch_raw_2.md`

**Modifications:**

### `/path/to/your/file.py`

**Block 1:**

```python
import re
class StreamExecutionEnvironment:
    def __init__(self):
        pass

def source(self, data):
    # your code here
    pass

def continuousSource(self, data):
    # your code here
    pass
```

**Block 2:**

```python
class StreamExecutionEnvironment:
    def __init__(self):
        pass

def source(self, data):
    # your code here
    pass

def continuousSource(self, data):
    # your code here
    pass
```

---

## Patch 2 (signature: `32eac986e5`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_1/patch_raw_1.md`

**Modifications:**

### `flink-python/pyflink/datastream/stream_execution_environment.py`

```python
class StreamExecutionEnvironment(object):
    def __init__(self):
        # ... existing code ...
        self.source_api = None
        self.continuous_source_api = None

    def set_source(self, source_api):
        self.source_api = source_api

    def set_continuous_source(self, continuous_source_api):
        self.continuous_source_api = continuous_source_api
```

---

## Patch 3 (signature: `4e43551be5`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_1/patch_raw_2.md`

**Modifications:**

### `flink-python/pyflink/datastream/stream_execution_environment.py`

**Block 1:**

```python
class StreamExecutionEnvironment(object):
```

**Block 2:**

```python
def execute(self):
```

---

## Patch 4 (signature: `64ce05d021`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_1/patch_raw_0.md`

**Modifications:**

### `flink-python/pyflink/datastream/stream_execution_environment.py`

```python
def source(self):
    # method implementation
```

---

## Patch 5 (signature: `a838b4e9c1`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_2/patch_raw_0.md`

**Modifications:**

### `.../search.py`

**Block 1:**

```python
def search_class(class_name: str): return [cls for cls in classes if 'StreamExecutionEnvironment' in str(cls)]
```

**Block 2:**

```python
def search_method_in_file(method_name: str, file_path: str): return [method for method in methods if method.name == method_name and method.file_path == file_path]
```

### `.../get_code_around_line.py`

```python
def get_code_around_line(file_path: str, line_number: int, window_size: int): return code_snippet = [line for line in open(file_path).readlines() if line_number - 1 <= len(code_snippet) and line_number + window_size > 0]
```

---

## Patch 6 (signature: `b3d1130432`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_0/patch_raw_1.md`

**Modifications:**

### `.../util.py`

```python
...
```

---

## Patch 7 (signature: `e2a247d680`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_2/patch_raw_1.md`

**Modifications:**

### `.../StreamExecutionEnvironment.py`

```python
...
```

---

## Patch 8 (signature: `ecea8ce55c`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_0/patch_raw_0.md`

**Modifications:**

### `util.py`

```python
def process_data(self, input_data):...
```

### `main.py`

```python
def run_app():...
```

---

## Patch 9 (signature: `fdbd5cdab3`)

**Source patch_raw files (duplicates):**
- `flink_95b9adbe_2025-10-15_17-14-04/output_0/patch_raw_2.md`

**Modifications:**

### `util.py`

```python
def process_data(self, data):...
```

---

