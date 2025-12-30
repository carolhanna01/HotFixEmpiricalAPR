# Bug: ambari_9491f1fd_2025-10-30_21-17-56

## Summary
- Total patch files: **9**
- Unique patches: **5**
- Patch files missing `<patched>` blocks: **4**

## Patch files with no `<patched>` blocks
- `ambari_9491f1fd_2025-10-30_21-17-56/output_0/patch_raw_1.md`
- `ambari_9491f1fd_2025-10-30_21-17-56/output_1/patch_raw_2.md`
- `ambari_9491f1fd_2025-10-30_21-17-56/output_2/patch_raw_0.md`
- `ambari_9491f1fd_2025-10-30_21-17-56/output_2/patch_raw_2.md`

---

## Patch 1 (signature: `6d25e6851c`)

**Source patch_raw files (duplicates):**
- `ambari_9491f1fd_2025-10-30_21-17-56/output_2/patch_raw_1.md`

**Modifications:**

### `.../pom.xml`

```xml
<dependency>
    <groupId>org.apache.directory.server</groupId>
    <artifactId>apacheds-all</artifactId>
    <version>1.5.8</version>
</dependency>
```

---

## Patch 2 (signature: `9067c79f5b`)

**Source patch_raw files (duplicates):**
- `ambari_9491f1fd_2025-10-30_21-17-56/output_1/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/ldap/service/ads/DefaultLdapConfigurationService.java`

```java
...
```

---

## Patch 3 (signature: `b3d220fd6f`)

**Source patch_raw files (duplicates):**
- `ambari_9491f1fd_2025-10-30_21-17-56/output_0/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/python/ambari_server/setupActions.py`

```python
import org.apache.hadoop.hive.conf.HiveConf;
```

### `contrib/management-packs/hdf-ambari-mpack/src/main/resources/stacks/HDF/2.0/services/stack_advisor.py`

```python
import org.apache.hadoop.hive.conf.HiveConf;
```

---

## Patch 4 (signature: `cdb74db76a`)

**Source patch_raw files (duplicates):**
- `ambari_9491f1fd_2025-10-30_21-17-56/output_1/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/ldap/service/ads/DefaultLdapConfigurationService.java`

```java
...
```

### `ambari-server/pom.xml`

```xml
...
```

---

## Patch 5 (signature: `fcf1265630`)

**Source patch_raw files (duplicates):**
- `ambari_9491f1fd_2025-10-30_21-17-56/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/python/ambari_server/setupActions.py`

```python
import org.apache.hadoop.hive.conf.HiveConf;
```

### `contrib/management-packs/hdf-ambari-mpack/src/main/resources/stacks/HDF/2.0/services/stack_advisor.py`

```python
from org.apache.hadoop.hive.conf import HiveConf;
```

---

