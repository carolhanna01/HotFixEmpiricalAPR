# Bug: bugsdotjar-repairllama-flink-6b892a63-TP1-CP1-0-f9c1beb24b

## Summary
- Total patch files: **5**
- Unique patches: **5**
- Invalid/unparseable patch files: **0**

## Patch 1 (signature: `11199795cb`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-6b892a63-TP1-CP1-0-f9c1beb24b/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java`

```diff
--- org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
+++ org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
@@ -585,7 +585,7 @@
 	 * Handles a termination notification from a task monitor.
 	 */
 	public void taskTerminated(TaskMonitor.TaskTerminated message) {
-		Protos.TaskID taskID = message.taskID();
+		final Protos.TaskID taskID = message.getTaskId();
 		Protos.TaskStatus status = message.status();

 		// note: this callback occurs for failed containers and for released containers alike
```

---

## Patch 2 (signature: `59d168bd68`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-6b892a63-TP1-CP1-0-f9c1beb24b/output/patches/3.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java`

```diff
--- org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
+++ org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
@@ -593,7 +593,7 @@

 		boolean existed;
 		try {
-			existed = workerStore.removeWorker(taskID);
+			existed = workerStore.removeWorker(id);
 		} catch (Exception ex) {
 			onFatalError(new ResourceManagerException("unable to remove worker", ex));
 			return;
```

---

## Patch 3 (signature: `82228b81ce`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-6b892a63-TP1-CP1-0-f9c1beb24b/output/patches/2.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java`

```diff
--- org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
+++ org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
@@ -589,7 +589,7 @@
 		Protos.TaskStatus status = message.status();

 		// note: this callback occurs for failed containers and for released containers alike
-		final ResourceID id = extractResourceID(taskID);
+		final ResourceID id = new ResourceID(taskID.getValue());

 		boolean existed;
 		try {
```

---

## Patch 4 (signature: `921713e765`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-6b892a63-TP1-CP1-0-f9c1beb24b/output/patches/1.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java`

```diff
--- org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
+++ org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
@@ -586,7 +586,7 @@
 	 */
 	public void taskTerminated(TaskMonitor.TaskTerminated message) {
 		Protos.TaskID taskID = message.taskID();
-		Protos.TaskStatus status = message.status();
+		Protos.TaskStatus status = message.finalStatus();

 		// note: this callback occurs for failed containers and for released containers alike
 		final ResourceID id = extractResourceID(taskID);
```

---

## Patch 5 (signature: `fb2be108de`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-6b892a63-TP1-CP1-0-f9c1beb24b/output/patches/4.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java`

```diff
--- org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
+++ org/apache/flink/mesos/runtime/clusterframework/MesosResourceManager.java
@@ -597,7 +597,7 @@
 		} catch (Exception ex) {
 			onFatalError(new ResourceManagerException("unable to remove worker", ex));
 			return;
-		}
+		} catch (Exception ex) {
			onFatalError(new ResourceManagerException("unable to remove worker", ex));
			return;
		}

 		if (!existed) {
 			LOG.info("Received a termination notice for an unrecognized worker: {}", id);
```

---

