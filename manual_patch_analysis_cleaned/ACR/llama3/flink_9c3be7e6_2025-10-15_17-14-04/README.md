# Bug: flink_9c3be7e6_2025-10-15_17-14-04

## Summary
- Total patch files: **7**
- Unique patches: **5**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `225e2038f3`)

**Source patch_raw files (duplicates):**
- `flink_9c3be7e6_2025-10-15_17-14-04/output_0/patch_raw_0.md`
- `flink_9c3be7e6_2025-10-15_17-14-04/output_0/patch_raw_1.md`

**Modifications:**

### `.../kinesis_firehose_sink_builder.py`

```python
...
```

---

## Patch 2 (signature: `43740a8c1d`)

**Source patch_raw files (duplicates):**
- `flink_9c3be7e6_2025-10-15_17-14-04/output_0/patch_raw_2.md`
- `flink_9c3be7e6_2025-10-15_17-14-04/output_1/patch_raw_1.md`

**Modifications:**

### `...`

```
...
```

---

## Patch 3 (signature: `69e826698d`)

**Source patch_raw files (duplicates):**
- `flink_9c3be7e6_2025-10-15_17-14-04/output_1/patch_raw_0.md`

**Modifications:**

### `/path/to/KinesisFirehoseSinkBuilder.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
search_class(class_name="KinesisFirehoseSinkBuilder")
```

**Block 3:**

```java
search_method_in_class(method_name="overrideProtocol", class_name="KinesisFirehoseSinkBuilder")
```

**Block 4:**

```java
search_method_in_file(method_name="overrideProtocol", file_path="/path/to/actual/file/path.java")
```

---

## Patch 4 (signature: `742b5130bf`)

**Source patch_raw files (duplicates):**
- `flink_9c3be7e6_2025-10-15_17-14-04/output_1/patch_raw_2.md`

**Modifications:**

### `/path/to/search_api.py`

**Block 1:**

```python
search_method()
```

**Block 2:**

```python
search_class_in_file(file_path="/path/to/KinesisFirehoseSinkBuilder.java", class_name="KinesisFirehoseSinkBuilder")
```

---

## Patch 5 (signature: `eeb3696b76`)

**Source patch_raw files (duplicates):**
- `flink_9c3be7e6_2025-10-15_17-14-04/output_2/patch_raw_0.md`

**Modifications:**

### `table.py`

```python
if isinstance(row, dict) and 'id' in row:
```

### `window.py`

```python
try:
```

---

