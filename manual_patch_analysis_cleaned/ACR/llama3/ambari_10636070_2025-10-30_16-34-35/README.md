# Bug: ambari_10636070_2025-10-30_16-34-35

## Summary
- Total patch files: **9**
- Unique patches: **5**
- Patch files missing `<patched>` blocks: **2**

## Patch files with no `<patched>` blocks
- `ambari_10636070_2025-10-30_16-34-35/output_0/patch_raw_0.md`
- `ambari_10636070_2025-10-30_16-34-35/output_0/patch_raw_1.md`

---

## Patch 1 (signature: `41965d20e2`)

**Source patch_raw files (duplicates):**
- `ambari_10636070_2025-10-30_16-34-35/output_0/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/AmbariManagementControllerImpl.java`

```java
...
```

---

## Patch 2 (signature: `90c86533ea`)

**Source patch_raw files (duplicates):**
- `ambari_10636070_2025-10-30_16-34-35/output_1/patch_raw_0.md`
- `ambari_10636070_2025-10-30_16-34-35/output_1/patch_raw_1.md`
- `ambari_10636070_2025-10-30_16-34-35/output_1/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/AmbariManagementControllerImpl.java`

```java
...
```

### `ambari-server/src/test/java/org/apache/ambari/server/controller/internal/UserResourceProviderTest.java`

```java
...
```

---

## Patch 3 (signature: `c6fe165884`)

**Source patch_raw files (duplicates):**
- `ambari_10636070_2025-10-30_16-34-35/output_2/patch_raw_0.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/AmbariController.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
...
```

**Block 3:**

```java
...
```

**Block 4:**

```java
...
```

**Block 5:**

```java
...
```

**Block 6:**

```java
...
```

---

## Patch 4 (signature: `d4fc21e35c`)

**Source patch_raw files (duplicates):**
- `ambari_10636070_2025-10-30_16-34-35/output_2/patch_raw_1.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/AmbariController.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
...
```

**Block 3:**

```java
...
```

---

## Patch 5 (signature: `dc3efefc91`)

**Source patch_raw files (duplicates):**
- `ambari_10636070_2025-10-30_16-34-35/output_2/patch_raw_2.md`

**Modifications:**

### `ambari-server/src/main/java/org/apache/ambari/server/controller/AmbariController.java`

**Block 1:**

```java
...
```

**Block 2:**

```java
public class AmbariController {
    // ...
    public void handleUserResourceProperties(String userResourceProperties, AmbariServer ambariServer) {
        if (userResourceProperties != null) {
            ambariServer.setUserResourceProperties(userResourceProperties);
        }
    }
}
```

---

