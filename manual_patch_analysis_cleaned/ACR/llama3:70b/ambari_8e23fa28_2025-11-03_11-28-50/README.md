# Bug: ambari_8e23fa28_2025-11-03_11-28-50

## Summary
- Total patch files: **3**
- Unique patches: **1**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `6edccc1461`)

**Source patch_raw files (duplicates):**
- `ambari_8e23fa28_2025-11-03_11-28-50/output_0/patch_raw_0.md`
- `ambari_8e23fa28_2025-11-03_11-28-50/output_0/patch_raw_1.md`
- `ambari_8e23fa28_2025-11-03_11-28-50/output_0/patch_raw_2.md`

**Modifications:**

### `ambari-common/src/main/python/resource_management/libraries/functions/install_jdbc_driver.py`

```python
38     Logger.info("Setting yarn.nodemanager.aux-services.spark2_shuffle.classpath property")
39     os.environ['yarn.nodemanager.aux-services.spark2_shuffle.classpath'] = dest_path
```

---

