# Bug: ambari_69c83419_2025-10-31_10-06-00

## Summary
- Total patch files: **9**
- Unique patches: **6**
- Patch files missing `<patched>` blocks: **3**

## Patch files with no `<patched>` blocks
- `ambari_69c83419_2025-10-31_10-06-00/output_0/patch_raw_1.md`
- `ambari_69c83419_2025-10-31_10-06-00/output_0/patch_raw_2.md`
- `ambari_69c83419_2025-10-31_10-06-00/output_1/patch_raw_0.md`

---

## Patch 1 (signature: `0a19f4bd2c`)

**Source patch_raw files (duplicates):**
- `ambari_69c83419_2025-10-31_10-06-00/output_1/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/ams/AmsService.java`

```java
...
```

### `ambari-server/src/main/java/org/apache/ambari/server/ams/ZooKeeper.java`

```java
...
```

---

## Patch 2 (signature: `562236aa31`)

**Source patch_raw files (duplicates):**
- `ambari_69c83419_2025-10-31_10-06-00/output_2/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/resources/common-services/HDFS/2.1.0.2.0/package/alerts/alert_metrics_deviation.py`

```python
def collect_metrics():...
```

### `ambari-server/src/main/resources/stacks/HDPWIN/2.1/services/stack_advisor.py`

```python
def detect_deviations():...
```

---

## Patch 3 (signature: `93033aa8f7`)

**Source patch_raw files (duplicates):**
- `ambari_69c83419_2025-10-31_10-06-00/output_1/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/ams/AmsService.java`

```java
...
```

---

## Patch 4 (signature: `977b8882d5`)

**Source patch_raw files (duplicates):**
- `ambari_69c83419_2025-10-31_10-06-00/output_2/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/resources/common-services/HDFS/2.1.0.2.0/package/alerts/alert_metrics_deviation.py`

```python
def collect_metrics(self):
    # some code here
    if self.metrics_collector:
        self.metrics_collector.collect()
    else:
        raise ValueError("Metrics collector not found")
    return
```

### `ambari-server/src/main/resources/stacks/HDPWIN/2.1/services/stack_advisor.py`

```python
def detect_deviations(self):
    # some code here
    if self.metrics_collector:
        deviations = self.metrics_collector.detect_deviations()
    else:
        raise ValueError("Metrics collector not found")
    return deviations
```

---

## Patch 5 (signature: `bf284ebe39`)

**Source patch_raw files (duplicates):**
- `ambari_69c83419_2025-10-31_10-06-00/output_2/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/resources/common-services/HDFS/2.1.0.2.0/package/alerts/alert_metrics_deviation.py`

```python
def collect_metrics():
    # Add code to correctly handle metrics collection and deviation detection
    pass
```

### `ambari-server/src/main/resources/stacks/HDPWIN/2.1/services/stack_advisor.py`

```python
def detect_deviations():
    # Add code to correctly handle deviation detection and alerting
    pass
```

### `ambari-server/src/main/resources/stacks/HDP/2.1/services/stack_advisor.py`

```python
def provide_alerts():
    # Add code to correctly handle alerting and notification
    pass
```

---

## Patch 6 (signature: `d2cc742a0b`)

**Source patch_raw files (duplicates):**
- `ambari_69c83419_2025-10-31_10-06-00/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/upgrade/UpgradeCatalog.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
...
```

---

