# Bug: ambari_274616eb_2025-10-31_00-42-56

## Summary
- Total patch files: **9**
- Unique patches: **5**
- Patch files missing `<patched>` blocks: **3**

## Patch files with no `<patched>` blocks
- `ambari_274616eb_2025-10-31_00-42-56/output_1/patch_raw_0.md`
- `ambari_274616eb_2025-10-31_00-42-56/output_1/patch_raw_1.md`
- `ambari_274616eb_2025-10-31_00-42-56/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `00cd2d7524`)

**Source patch_raw files (duplicates):**
- `ambari_274616eb_2025-10-31_00-42-56/output_2/patch_raw_0.md`
- `ambari_274616eb_2025-10-31_00-42-56/output_2/patch_raw_2.md`

**Modifications:**

### `.../hbase_service.py`

```python
if hbase_status == 'success':
```

---

## Patch 2 (signature: `4e459ea32d`)

**Source patch_raw files (duplicates):**
- `ambari_274616eb_2025-10-31_00-42-56/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/state/stack/UpgradePackTest.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
...
```

---

## Patch 3 (signature: `5b44050318`)

**Source patch_raw files (duplicates):**
- `ambari_274616eb_2025-10-31_00-42-56/output_2/patch_raw_1.md`

**Modifications:**

### `.../hbase_service.py`

```python
if hbase_service_status == 'success':
```

---

## Patch 4 (signature: `9928a26462`)

**Source patch_raw files (duplicates):**
- `ambari_274616eb_2025-10-31_00-42-56/output_0/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/state/stack/upgrade/ServiceCheckGrouping.java`

```java
search_method_in_file(method_name=None, file_path='ambari-server/src/main/java/org/apache/ambari/server/state/stack/upgrade/ServiceCheckGrouping.java')
```

### `ambari-server/src/main/java/org/apache/ambari/server/state/stack/UpgradePackTest.java`

**Block 1:**

```java
get_code_around_line(file_path='ambari-server/src/main/java/org/apache/ambari/server/state/stack/UpgradePackTest.java', line_number=10, window_size=None)
```

**Block 2:**

```java
search_code(code_str=None, file_path='ambari-server/src/main/java/org/apache/ambari/server/state/stack/UpgradePackTest.java')
```

---

## Patch 5 (signature: `d0939965fd`)

**Source patch_raw files (duplicates):**
- `ambari_274616eb_2025-10-31_00-42-56/output_0/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/state/stack/UpgradePackTest.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
import org.apache.ambari.server.state.stack.UpgradePack;
public class UpgradePackTest {
    public void testSearch() {
        UpgradePack pack = new UpgradePack();
        // Search for classes
        List<Class<?>> classes = pack.searchClasses("ServiceCheckGrouping");
        // Search for methods
        List<Method> methods = pack.searchMethods("ambari-server/src/main/java/org/apache/ambari/server/state/stack/upgrade/ServiceCheckGrouping.java", "ServiceCheckGrouping");
        // Search for code snippets
        List<String> codeSnippets = pack.searchCodeSnippets("ambari-server/src/main/java/org/apache/ambari/server/state/stack/UpgradePackTest.java", "testSearch");
    }
}
```

---

