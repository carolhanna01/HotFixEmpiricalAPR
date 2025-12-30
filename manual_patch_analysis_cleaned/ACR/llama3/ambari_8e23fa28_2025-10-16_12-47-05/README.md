# Bug: ambari_8e23fa28_2025-10-16_12-47-05

## Summary
- Total patch files: **9**
- Unique patches: **6**
- Patch files missing `<patched>` blocks: **3**

## Patch files with no `<patched>` blocks
- `ambari_8e23fa28_2025-10-16_12-47-05/output_0/patch_raw_2.md`
- `ambari_8e23fa28_2025-10-16_12-47-05/output_2/patch_raw_1.md`
- `ambari_8e23fa28_2025-10-16_12-47-05/output_2/patch_raw_2.md`

---

## Patch 1 (signature: `04641a7799`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-10-16_12-47-05/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/agent/AuxServices.java`

```java
...
```

### `ambari-server/src/main/java/org/apache/ambari/server/cluster/Cluster.java`

```java
...
```

---

## Patch 2 (signature: `69a52b1664`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-10-16_12-47-05/output_2/patch_raw_0.md`

**Modifications:**

### `/path/to/SparkContext.py`

```python
def start(self):...
```

---

## Patch 3 (signature: `7ac59b56d2`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-10-16_12-47-05/output_1/patch_raw_2.md`

**Modifications:**

### `contrib/management-packs/odpi-ambari-mpack/src/main/resources/stacks/ODPi/2.0/services/YARN/package/scripts/resourcemanager.py`

```python
...
```

### `contrib/management-packs/odpi-ambari-mpack/src/main/resources/stacks/ODPi/2.0/services/YARN/package/scripts/application_timeline_server.py`

```python
...
```

---

## Patch 4 (signature: `a26e22693a`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-10-16_12-47-05/output_1/patch_raw_1.md`

**Modifications:**

### `contrib/management-packs/odpi-ambari-mpack/src/main/resources/stacks/ODPi/2.0/services/YARN/package/scripts/resourcemanager.py`

```python
def validate_yarn_service_configurations(self, yarn_site_xml):
```

### `contrib/management-packs/odpi-ambari-mpack/src/main/resources/stacks/ODPi/2.0/services/YARN/package/scripts/application_timeline_server.py`

```python
def validate_yarn_service_configurations(self, yarn_site_xml):
```

### `contrib/management-packs/odpi-ambari-mpack/src/main/resources/stacks/ODPi/2.0/services/YARN/package/scripts/nodemanager.py`

```python
def validate_yarn_service_configurations(self, yarn_site_xml):
```

---

## Patch 5 (signature: `a31bc9ca52`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-10-16_12-47-05/output_1/patch_raw_0.md`

**Modifications:**

### `contrib/management-packs/odpi-ambari-mpack/src/main/resources/stacks/ODPi/2.0/services/YARN/package/scripts/resourcemanager.py`

**Block 1:**

```python
...
```

**Block 2:**

```python
import requests
requests.get('https://api.example.com/search', params={'q': 'search term'})
```

---

## Patch 6 (signature: `a954b2e0d1`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-10-16_12-47-05/output_0/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/agent/ExecutionCommand.java`

```java
self.search_class("AmbariCustomCommandExecutionHelperTest")
```

---

