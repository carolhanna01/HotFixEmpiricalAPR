# Bug: kafka_d62a42df_2025-10-31_18-40-21

## Summary
- Total patch files: **9**
- Unique patches: **8**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `018975c093`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_0/patch_raw_0.md`

**Modifications:**

### `Kafka.java`

```java
public void re_scan() {
    if (mismatch_found()) {
        re_scan_at_divergence_point();
    }
}
```

### `shadowing.java`

```java
public void shadowing() {
    if (prefix_acl_found()) {
        handle_prefix_acl();
    }
}
```

---

## Patch 2 (signature: `1906eeef45`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_1/patch_raw_0.md`

**Modifications:**

### `release.py`

```python
603            'rc_tag': rc_tag,
604            'artifacts_dir': artifacts_dir
605            }
606 cmd("Creating source archive", "git archive --format tar.gz --prefix kafka-%(release_version)s-src/ -o %(artifacts_dir)s/kafka-%(release_version)s-src.tgz %(rc_tag)s" % params)
607
608 cmd("Building artifacts", "build-artifacts.sh")
609
```

---

## Patch 3 (signature: `48fc3e7f7d`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_1/patch_raw_1.md`
- `kafka_d62a42df_2025-10-31_18-40-21/output_2/patch_raw_0.md`

**Modifications:**

### `release.py`

```python
...
```

---

## Patch 4 (signature: `4eb2bd4f83`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_0/patch_raw_2.md`

**Modifications:**

### `Kafka.java`

```java
public void re_scan() {
    if (mismatch_found()) {
        re_scan_at_divergence_point();
    }
}
```

### `...`

```
public void shadowing() {
    if (prefix_acl_found()) {
        prevent_shadowing();
    }
}
```

---

## Patch 5 (signature: `5ddcc6a60b`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_2/patch_raw_1.md`

**Modifications:**

### `release.py`

```python
if condition: ... None if None else ...
```

---

## Patch 6 (signature: `9154854bcd`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_0/patch_raw_1.md`

**Modifications:**

### `Kafka.java`

```java
public void re_scan() {
    if (mismatch_found()) {
        re_scan_at_divergence_point();
    }
}
```

### `shadowing.py`

```python
def shadowing(prefix_acl):
    if prefix_acl.startswith("prefix_"):
        return "prefix_" + prefix_acl[7:]
    else:
        return prefix_acl
}
```

---

## Patch 7 (signature: `ccb2bb357c`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_2/patch_raw_2.md`

**Modifications:**

### `.../release.py`

```python
if not prefix_acl:
```

---

## Patch 8 (signature: `f752816585`)

**Source patch_raw files (duplicates):**
- `kafka_d62a42df_2025-10-31_18-40-21/output_1/patch_raw_2.md`

**Modifications:**

### `release.py`

```python

```

---

