# Bug: flink_74c45c48_2025-10-15_17-14-07

## Summary
- Total patch files: **9**
- Unique patches: **9**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `1921b3accc`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_2/patch_raw_1.md`

**Modifications:**

### `...`

**Block 1:**

```
result = search_class("KinesisFirehoseSinkBuilder")
```

**Block 2:**

```
result = search_method_in_file("KinesisFirehoseITCase.java", "protocol")
```

**Block 3:**

```
result = search_code("default protocol KinesisFirehoseSinkBuilder software.amazon.awssdk.http.Protocol")
```

---

## Patch 2 (signature: `2a04253a88`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_0/patch_raw_1.md`

**Modifications:**

### `.../kinesis_firehose_sink_builder.py`

**Block 1:**

```python
...
```

**Block 2:**

```python
...
```

---

## Patch 3 (signature: `2cdf3d1edb`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_0/patch_raw_2.md`

**Modifications:**

### `.../kinesis_firehose_sink_builder.py`

```python
self.protocol = 'https'
```

---

## Patch 4 (signature: `6628c9bf04`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_1/patch_raw_0.md`

**Modifications:**

### `kinesis-firehose-sink-builder/src/main/java/com/apache/kinesis/FirehoseSink.java`

```java
def create_firehose_client(self, protocol='https'):...
```

### `kinesis-firehose-sink-builder/src/main/java/com/apache/kinesis/KinesisFirehose.java`

```java
def get_protocol(self): return 'https'
```

---

## Patch 5 (signature: `8afe9e509a`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_1/patch_raw_1.md`

**Modifications:**

### `kinesis-firehose-sink-builder/src/main/java/com/apache/kinesis/FirehoseSink.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
public FirehoseSink createFirehoseClient() {
    // code here
    return new FirehoseSink("https", "aws-firehose.com");
}
```

---

## Patch 6 (signature: `8e1a99a229`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_2/patch_raw_0.md`

**Modifications:**

### `search.py`

**Block 1:**

```python
result = search_class("KinesisFirehoseSinkBuilder", None)
```

**Block 2:**

```python
result = search_method_in_file("KinesisFirehoseITCase.java", "protocol")
```

**Block 3:**

```python
result = search_code("default protocol KinesisFirehoseSinkBuilder software.amazon.awssdk.http.Protocol",)
```

---

## Patch 7 (signature: `c8578dc847`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_0/patch_raw_0.md`

**Modifications:**

### `.../kinesis_firehose_sink_builder.py`

```python
class KinesisFirehoseSinkBuilder:
```

---

## Patch 8 (signature: `e5576e0dea`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_2/patch_raw_2.md`

**Modifications:**

### `.../KinesisFirehoseITCase.java`

```java
...
```

### `.../software.amazon.awssdk.http.Protocol`

```
...
```

### `.../KinesisFirehoseSinkBuilder`

```
...
```

### `.../default protocol`

```
...
```

---

## Patch 9 (signature: `eff640cac5`)

**Source patch_raw files (duplicates):**
- `flink_74c45c48_2025-10-15_17-14-07/output_1/patch_raw_2.md`

**Modifications:**

### `kinesis-firehose-sink-builder/src/main/java/com/apache/kinesis/FirehoseSink.java`

```java
def createFirehoseClient(self, protocol='https'):...
```

### `kinesis-firehose-sink-builder/src/main/java/com/apache/kinesis/KinesisFirehose.java`

```java
def getProtocol(self): return 'https'
```

---

