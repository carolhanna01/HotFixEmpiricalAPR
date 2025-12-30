# Bug: ambari_27a22897_2025-11-04_07-34-18

## Summary
- Total patch files: **3**
- Unique patches: **2**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `12ad47fb56`)

**Source patch_raw files (duplicates):**
- `ambari_27a22897_2025-11-04_07-34-18/output_0/patch_raw_1.md`
- `ambari_27a22897_2025-11-04_07-34-18/output_0/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/view/ViewAmbariStreamProvider.java`

```java
URIBuilder uriBuilder = new URIBuilder();
    uriBuilder.setScheme("https");
    uriBuilder.setHost("localhost");
    uriBuilder.setPort(8443);
    URI uri = uriBuilder.build();
```

---

## Patch 2 (signature: `203f567532`)

**Source patch_raw files (duplicates):**
- `ambari_27a22897_2025-11-04_07-34-18/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/view/ViewAmbariStreamProvider.java`

```java
URIBuilder uriBuilder = new URIBuilder();
    uriBuilder.setPath("/api/v1/clusters/" + clusterName);
    uriBuilder.setParameter("fields", "Clusters/desired_configs,Clusters/cluster_state");
```

---

