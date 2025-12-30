# Bug: ambari_4104f2f9_2025-10-15_16-56-08

## Summary
- Total patch files: **4**
- Unique patches: **4**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `0650331092`)

**Source patch_raw files (duplicates):**
- `ambari_4104f2f9_2025-10-15_16-56-08/output_0/patch_raw_1.md`

**Modifications:**

### `/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java`

```java
search_method_in_file(method_name="handle_request", class_name="ViewThrottleFilter", file_path="/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java")
```

### `/ambari-server/src/main/java/org/apache/ambari/server/configuration/Configuration.java`

```java
search_method_in_file(method_name="get_config", class_name="Configuration", file_path="/ambari-server/src/main/java/org/apache/ambari/server/configuration/Configuration.java")
```

---

## Patch 2 (signature: `7abd117138`)

**Source patch_raw files (duplicates):**
- `ambari_4104f2f9_2025-10-15_16-56-08/output_0/patch_raw_2.md`

**Modifications:**

### `/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java`

**Block 1:**

```java
search_class(class_name="ViewThrottleFilter")
```

**Block 2:**

```java
search_method_in_file(method_name="handleRequest", class_name="ViewThrottleFilter", file_path="/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java")
```

**Block 3:**

```java
get_code_around_line(file_path="/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java", line_number=10, window_size=5)
```

### `/ambari-server/src/main/java/org/apache/ambari/server/configuration/Configuration.java`

**Block 1:**

```java
search_method_in_file(method_name="getConfig", class_name="Configuration", file_path="/ambari-server/src/main/java/org/apache/ambari/server/configuration/Configuration.java")
```

**Block 2:**

```java
get_code_around_line(file_path="/ambari-server/src/main/java/org/apache/ambari/server/configuration/Configuration.java", line_number=20, window_size=5)
```

---

## Patch 3 (signature: `7c59ad5217`)

**Source patch_raw files (duplicates):**
- `ambari_4104f2f9_2025-10-15_16-56-08/output_0/patch_raw_0.md`

**Modifications:**

### `/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java`

**Block 1:**

```java
search_class(class_name="org.apache.ambari.server.view.ViewThrottleFilter")
```

**Block 2:**

```java
search_method_in_file(method_name="handleRequest", class_name="org.apache.ambari.server.view.ViewThrottleFilter", file_path="/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java")
```

### `/ambari-server/src/main/java/org/apache/ambari/server/configuration/Configuration.java`

**Block 1:**

```java
search_file(file_path="/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java")
```

**Block 2:**

```java
get_code_around_line(file_path="/ambari-server/src/main/java/org/apache/ambari/server/view/ViewThrottleFilter.java", line_number=10, window_size=5)
```

---

## Patch 4 (signature: `8b901f7bc1`)

**Source patch_raw files (duplicates):**
- `ambari_4104f2f9_2025-10-15_16-56-08/output_1/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/ViewThrottleFilter.java`

```java
...
```

---

