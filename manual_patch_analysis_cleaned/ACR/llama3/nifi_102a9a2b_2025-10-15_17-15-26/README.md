# Bug: nifi_102a9a2b_2025-10-15_17-15-26

## Summary
- Total patch files: **9**
- Unique patches: **8**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `4c9dfe7771`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_2/patch_raw_2.md`

**Modifications:**

### `consume_kafka.py`

**Block 1:**

```python
def encodeKafkaKeyAsAttribute(kafka_key):
    return kafka_key.encode('utf-8', errors='ignore')
```

**Block 2:**

```python
def interpretKafkaKeyAsAttribute(kafka_key):
    try:
        return kafka_key.decode('utf-8')
    except UnicodeDecodeError:
        return None
```

---

## Patch 2 (signature: `6dbc1de470`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_1/patch_raw_0.md`
- `nifi_102a9a2b_2025-10-15_17-15-26/output_1/patch_raw_1.md`

**Modifications:**

### `/path/to/ConsumeKafka.py`

```python
...
```

---

## Patch 3 (signature: `8697e3bac4`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_0/patch_raw_0.md`

**Modifications:**

### `/path/to/NiFiProcessor.java`

```java
...
```

---

## Patch 4 (signature: `89c2be4d0c`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_0/patch_raw_1.md`

**Modifications:**

### `/path/to/NiFiProcessor.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
...
```

**Block 3:**

```java
...
```

**Block 4:**

```java
...
```

**Block 5:**

```java
...
```

**Block 6:**

```java
...
```

**Block 7:**

```java
...
```

**Block 8:**

```java
...
```

**Block 9:**

```java
...
```

**Block 10:**

```java
...
```

**Block 11:**

```java
...
```

**Block 12:**

```java
...
```

**Block 13:**

```java
...
```

---

## Patch 5 (signature: `923fa10d30`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_2/patch_raw_0.md`

**Modifications:**

### `.../consuming_kafka.py`

**Block 1:**

```python
def encodeKafkaKeyAsAttribute(kafka_key):
    return kafka_key.decode('utf-8').encode('utf-16')
```

**Block 2:**

```python
def interpretKafkaKey(kafka_key):
    return kafka_key.encode('utf-16').decode('utf-8')
```

---

## Patch 6 (signature: `ae43eaccce`) CH:SYMPTOM-HIDING

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_2/patch_raw_1.md`

**Modifications:**

### `.../consuming_kafka.py`

**Block 1:**

```python
def encodeKafkaKeyAsAttribute(kafka_key):
    # Add error handling for invalid kafka keys
    if not isinstance(kafka_key, str):
        raise ValueError("Invalid kafka key")
    return kafka_key.encode('utf-8')
```

**Block 2:**

```python
def interpretKafkaKey(attribute):
    # Add error handling for invalid attributes
    if not isinstance(attribute, str):
        raise ValueError("Invalid attribute")
    return attribute.decode('utf-8')
```

---

## Patch 7 (signature: `b28dbadeb6`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_1/patch_raw_2.md`

**Modifications:**

### `/path/to/KafkaProcessor.py`

```python
...
```

---

## Patch 8 (signature: `d583432155`)

**Source patch_raw files (duplicates):**
- `nifi_102a9a2b_2025-10-15_17-15-26/output_0/patch_raw_2.md`

**Modifications:**

### `/path/to/NiFiProcessor.py`

```python
...
```

---

