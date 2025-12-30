# Bug: nifi_f85ae68f_2025-10-17_07-25-12

## Summary
- Total patch files: **6**
- Unique patches: **5**
- Patch files missing `<patched>` blocks: **1**

## Patch files with no `<patched>` blocks
- `nifi_f85ae68f_2025-10-17_07-25-12/output_1/patch_raw_2.md`

---

## Patch 1 (signature: `25f083367a`)

**Source patch_raw files (duplicates):**
- `nifi_f85ae68f_2025-10-17_07-25-12/output_0/patch_raw_2.md`

**Modifications:**

### `.../SFTPServer.py`

**Block 1:**

```python
...
```

**Block 2:**

```python
class SFTPServer:
```

---

## Patch 2 (signature: `576ea2936b`)

**Source patch_raw files (duplicates):**
- `nifi_f85ae68f_2025-10-17_07-25-12/output_0/patch_raw_0.md`

**Modifications:**

### `.../server.py`

```python
...
```

---

## Patch 3 (signature: `5efe2b16ca`)

**Source patch_raw files (duplicates):**
- `nifi_f85ae68f_2025-10-17_07-25-12/output_0/patch_raw_1.md`

**Modifications:**

### `.../main.py`

```python
from ... import SFTPServer
```

---

## Patch 4 (signature: `993b1ee9bf`)

**Source patch_raw files (duplicates):**
- `nifi_f85ae68f_2025-10-17_07-25-12/output_1/patch_raw_1.md`

**Modifications:**

### `FetchSFTP.java`

```java
try:
    # original code here
except Exception as e:
    # handle exception here
finally:
    sshClient.close()
```

### `SFTPTransfer.java`

```java
try:
    # original code here
except Exception as e:
    # handle exception here
finally:
    keepAliveThread.join()
    if not keepAliveThread.is_alive():
        # close the connection here
```

---

## Patch 5 (signature: `e15d7415ff`)

**Source patch_raw files (duplicates):**
- `nifi_f85ae68f_2025-10-17_07-25-12/output_1/patch_raw_0.md`

**Modifications:**

### `FetchSFTP.java`

```java
try:
    # original code here
except Exception as e:
    print(f"Error: {e}")
    sshClient.close()
finally:
    if sshClient:
        sshClient.close()
```

### `SFTPTransfer.java`

```java
try:
    # original code here
except Exception as e:
    print(f"Error: {e}")
    sftp.close()
finally:
    if sftp:
        sftp.close()
```

---

