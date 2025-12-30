# Bug: ambari_b7075841_2025-10-31_14-36-22

## Summary
- Total patch files: **9**
- Unique patches: **5**
- Patch files missing `<patched>` blocks: **4**

## Patch files with no `<patched>` blocks
- `ambari_b7075841_2025-10-31_14-36-22/output_0/patch_raw_0.md`
- `ambari_b7075841_2025-10-31_14-36-22/output_1/patch_raw_0.md`
- `ambari_b7075841_2025-10-31_14-36-22/output_1/patch_raw_1.md`
- `ambari_b7075841_2025-10-31_14-36-22/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `10799bfa16`)

**Source patch_raw files (duplicates):**
- `ambari_b7075841_2025-10-31_14-36-22/output_2/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/HbaseUpgradeCatalog.java`

```java
def setMasterCoprocessorClasses(self, master_coprocessor_classes):...
```

---

## Patch 2 (signature: `262077d17d`)

**Source patch_raw files (duplicates):**
- `ambari_b7075841_2025-10-31_14-36-22/output_0/patch_raw_2.md`

**Modifications:**

### `config.py`

```python
if not config.DEBUG or os.environ.get('DEBUG', 'false').lower() == 'true':
```

### `models.py`

```python
def get_user_data(user_id):
```

---

## Patch 3 (signature: `9ecf457f46`)

**Source patch_raw files (duplicates):**
- `ambari_b7075841_2025-10-31_14-36-22/output_2/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/HbaseUpgradeCatalog.java`

```java
public void setMasterCoprocessorClasses(String[] masterCoprocessorClasses) {
    if (masterCoprocessorClasses != null && masterCoprocessorClasses.length > 0) {
        this.masterCoprocessorClasses = masterCoprocessorClasses;
    } else {
        throw new NullPointerException("Master coprocessor classes cannot be null or empty");
    }
}
```

---

## Patch 4 (signature: `cb022f6e27`)

**Source patch_raw files (duplicates):**
- `ambari_b7075841_2025-10-31_14-36-22/output_0/patch_raw_1.md`

**Modifications:**

### `.../myproject/models.py`

```python
if not request.user.is_authenticated:
```

### `.../myproject/views.py`

```python
from django.contrib.auth.models import AnonymousUser
```

---

## Patch 5 (signature: `e5b9592a96`)

**Source patch_raw files (duplicates):**
- `ambari_b7075841_2025-10-31_14-36-22/output_2/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/HbaseUpgradeCatalog.java`

```java
from ambari.server.upgrade.hbase import HBaseMasterCoprocessorClasses
def setMasterCoprocessorClasses(self, master_coprocessor_classes):
    self.master_coprocessor_classes = master_coprocessor_classes
```

---

