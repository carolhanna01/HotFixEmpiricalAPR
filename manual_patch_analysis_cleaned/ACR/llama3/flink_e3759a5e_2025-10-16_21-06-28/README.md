# Bug: flink_e3759a5e_2025-10-16_21-06-28

## Summary
- Total patch files: **9**
- Unique patches: **6**
- Patch files missing `<patched>` blocks: **2**

## Patch files with no `<patched>` blocks
- `flink_e3759a5e_2025-10-16_21-06-28/output_1/patch_raw_1.md`
- `flink_e3759a5e_2025-10-16_21-06-28/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `0911218ce9`)

**Source patch_raw files (duplicates):**
- `flink_e3759a5e_2025-10-16_21-06-28/output_2/patch_raw_1.md`

**Modifications:**

### `.../cep_operator.py`

```python
...
```

---

## Patch 2 (signature: `39185550ac`)

**Source patch_raw files (duplicates):**
- `flink_e3759a5e_2025-10-16_21-06-28/output_0/patch_raw_2.md`

**Modifications:**

### `...`

```
...
```

### `/path/to/file.py`

**Block 1:**

```python
if event_type == 'CEP' and not is_watermark:
```

**Block 2:**

```python
if event_type == 'CEP' and not is_watermark:
```

**Block 3:**

```python
if event_type == 'CEP' and not is_watermark:
```

---

## Patch 3 (signature: `43740a8c1d`)

**Source patch_raw files (duplicates):**
- `flink_e3759a5e_2025-10-16_21-06-28/output_1/patch_raw_0.md`

**Modifications:**

### `...`

```
...
```

---

## Patch 4 (signature: `bd946600e2`)

**Source patch_raw files (duplicates):**
- `flink_e3759a5e_2025-10-16_21-06-28/output_0/patch_raw_0.md`
- `flink_e3759a5e_2025-10-16_21-06-28/output_0/patch_raw_1.md`

**Modifications:**

### `.../stream_operator.py`

```python
...
```

---

## Patch 5 (signature: `ce95145b36`)

**Source patch_raw files (duplicates):**
- `flink_e3759a5e_2025-10-16_21-06-28/output_2/patch_raw_2.md`

**Modifications:**

### `.../cep_operator.py`

```python
if self.watermark != None:
```

---

## Patch 6 (signature: `f1c971c259`)

**Source patch_raw files (duplicates):**
- `flink_e3759a5e_2025-10-16_21-06-28/output_2/patch_raw_0.md`

**Modifications:**

### `.../cep_operator.py`

```python
if watermark_time > event_time:
    forward_watermark()
else:
    process_event()
```

---

