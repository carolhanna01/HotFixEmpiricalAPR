# Bug: kafka_be846d83_2025-11-01_19-53-52

## Summary
- Total patch files: **3**
- Unique patches: **3**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `34860ea5e9`)

**Source patch_raw files (duplicates):**
- `kafka_be846d83_2025-11-01_19-53-52/output_0/patch_raw_2.md`

**Modifications:**

### `clients/src/main/java/ConfigTransformer.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
...
```

### `clients/src/main/java/ConfigTransformerTest.java`

```java
...
```

---

## Patch 2 (signature: `3993a7ab34`)

**Source patch_raw files (duplicates):**
- `kafka_be846d83_2025-11-01_19-53-52/output_0/patch_raw_0.md`

**Modifications:**

### `config_transformer.py`

**Block 1:**

```python
search_class("org.apache.kafka.common.config.ConfigTransformer")
```

**Block 2:**

```python
file_name = "ConfigTransformer.java"; method_name = "transform"; search_method_in_file(method_name=method_name, file_path=file_name)
```

**Block 3:**

```python
class_name = "org.apache.kafka.common.config.ConfigTransformer"; search_class_in_file(class_name=class_name, file_name="")
```

**Block 4:**

```python
line_number = 10; window_size = 5; get_code_around_line(file_path="", line_number=line_number, window_size=window_size)
```

---

## Patch 3 (signature: `861032380f`)

**Source patch_raw files (duplicates):**
- `kafka_be846d83_2025-11-01_19-53-52/output_0/patch_raw_1.md`

**Modifications:**

### `clients/src/main/java/ConfigTransformer.java`

**Block 1:**

```java
search_class("org.apache.kafka.common.config.ConfigTransformer")
```

**Block 2:**

```java
file_name = "ConfigTransformer.java"
method_name = "transform"
search_method_in_file(method_name=method_name, file_path=file_name)
```

### `clients/src/main/java/ConfigTransformerTest.java`

```java
file_path = "clients/src/test/java/ConfigTransformerTest.java"
line_number = 10
window_size = 5
get_code_around_line(file_path=file_path, line_number=line_number, window_size=window_size)
```

---

