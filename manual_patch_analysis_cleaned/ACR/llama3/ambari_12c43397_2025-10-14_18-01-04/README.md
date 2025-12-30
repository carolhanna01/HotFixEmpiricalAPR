# Bug: ambari_12c43397_2025-10-14_18-01-04

## Summary
- Total patch files: **9**
- Unique patches: **4**
- Patch files missing `<patched>` blocks: **5**

## Patch files with no `<patched>` blocks
- `ambari_12c43397_2025-10-14_18-01-04/output_0/patch_raw_1.md`
- `ambari_12c43397_2025-10-14_18-01-04/output_0/patch_raw_2.md`
- `ambari_12c43397_2025-10-14_18-01-04/output_1/patch_raw_0.md`
- `ambari_12c43397_2025-10-14_18-01-04/output_1/patch_raw_1.md`
- `ambari_12c43397_2025-10-14_18-01-04/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `1ac2ce2253`)

**Source patch_raw files (duplicates):**
- `ambari_12c43397_2025-10-14_18-01-04/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/logging/LoggingRequestHelperImpl.java`

```java
try:
    # original code here
except Exception as e:
    print(f"Error occurred while making request to LogSearch service: {e}")
    logging.error(f"Error occurred while making request to LogSearch service: {e}")
finally:
    # original code here
```

---

## Patch 2 (signature: `3d3836c02c`)

**Source patch_raw files (duplicates):**
- `ambari_12c43397_2025-10-14_18-01-04/output_2/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/logging/LoggingSearchPropertyProvider.java`

**Block 1:**

```java
logging_search_property_provider = search_class(class_name="org.apache.ambari.server.controller.logging.LoggingSearchPropertyProvider")
```

**Block 2:**

```java
method_name = "makeRequestToLogSearchService"
```

---

## Patch 3 (signature: `3ece7ca920`)

**Source patch_raw files (duplicates):**
- `ambari_12c43397_2025-10-14_18-01-04/output_2/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/logging/LoggingSearchPropertyProvider.java`

```java
from org.apache.ambari.server.controller.logging import LoggingSearchPropertyProvider
```

---

## Patch 4 (signature: `c399d7b81f`)

**Source patch_raw files (duplicates):**
- `ambari_12c43397_2025-10-14_18-01-04/output_2/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/logging/LoggingSearchPropertyProvider.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
search_class(query='error')
```

**Block 3:**

```java
search_method_in_file(file_path, 'makeRequestToLogSearchService')
```

**Block 4:**

```java
search_code('Error occurred while making request to LogSearch service')
```

**Block 5:**

```java
get_code_around_line(100, 5)
```

---

