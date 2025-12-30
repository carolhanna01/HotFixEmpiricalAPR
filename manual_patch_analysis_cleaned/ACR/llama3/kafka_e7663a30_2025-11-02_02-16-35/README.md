# Bug: kafka_e7663a30_2025-11-02_02-16-35

## Summary
- Total patch files: **9**
- Unique patches: **8**
- Patch files missing `<patched>` blocks: **1**

## Patch files with no `<patched>` blocks
- `kafka_e7663a30_2025-11-02_02-16-35/output_2/patch_raw_0.md`

---

## Patch 1 (signature: `4f7d8d0c57`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_2/patch_raw_1.md`

**Modifications:**

### `/path/to/file.py`

**Block 1:**

```python
def commitSync():...
```

**Block 2:**

```python
if condition: pass
```

---

## Patch 2 (signature: `611c757c37`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_1/patch_raw_1.md`

**Modifications:**

### `path/to/KafkaConsumer.py`

```python
def commitSync(self):
    try:
        # original implementation of commitSync method
    except Exception as e:
        print(f"Error committing sync: {e}")
        self.retry_commit()
    finally:
        self.commit_success = True
```

---

## Patch 3 (signature: `6576704eb9`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_1/patch_raw_0.md`

**Modifications:**

### `path/to/KafkaConsumer.py`

```python
if not self.is_connected():
    self.connect()
else:
    self.poll()
```

---

## Patch 4 (signature: `91534e60d3`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_2/patch_raw_2.md`

**Modifications:**

### `/path/to/file.py`

```python
...
```

---

## Patch 5 (signature: `afd5eeaae7`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_1/patch_raw_2.md`

**Modifications:**

### `path/to/ConsumerBounceTest.java`

```java
...
```

---

## Patch 6 (signature: `d584a138fc`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_0/patch_raw_2.md`

**Modifications:**

### `kafka/src/main/java/KafkaConsumer.java`

```java
def commitSync(self):
    if self.request_queue.empty():
        timeout = time.time() + 10  # wait for 10 seconds
        while True:
            if time.time() > timeout:
                break
            if not self.request_queue.empty():
                break
    else:
        request = self.request_queue.get()
        self.process_request(request)
```

### `kafka/src/main/java/NetworkClient.java`

```java
def poll(self):
    if self.request_queue.empty():
        timeout = time.time() + 10  # wait for 10 seconds
        while True:
            if time.time() > timeout:
                break
            if not self.request_queue.empty():
                break
    else:
        request = self.request_queue.get()
        self.send_request(request)
```

---

## Patch 7 (signature: `f575d5b390`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_0/patch_raw_0.md`

**Modifications:**

### `kafka/src/main/java/KafkaConsumer.java`

```java
def commitSync(self):
    while True:
        try:
            self.process_requests()
            if not self.requests_pending():
                break
        except TimeoutError:
            break
    return
```

### `kafka/src/main/java/NetworkClient.java`

```java
def poll(self):
    while True:
        try:
            self.send_request()
            if not self.request_sent():
                break
        except TimeoutError:
            break
    return
```

---

## Patch 8 (signature: `fe45183886`)

**Source patch_raw files (duplicates):**
- `kafka_e7663a30_2025-11-02_02-16-35/output_0/patch_raw_1.md`

**Modifications:**

### `kafka/src/main/java/KafkaConsumer.java`

```java
if (requests_pending):
```

### `kafka/src/main/java/NetworkClient.java`

```java
if (request_sent):
```

---

