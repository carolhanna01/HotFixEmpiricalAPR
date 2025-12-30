# Bug: bugsdotjar-repairllama-flink-1836e08f-TP1-CP1-1-5738b79f94

## Summary
- Total patch files: **5**
- Unique patches: **4**
- Invalid/unparseable patch files: **1**

## Invalid / unparseable patch files
- `bugsdotjar-repairllama-flink-1836e08f-TP1-CP1-1-5738b79f94/output/patches/1.patch` — empty diff

---

## Patch 1 (signature: `13e6580022`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-1836e08f-TP1-CP1-1-5738b79f94/output/patches/3.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/api/graph/StreamConfig.java`

```diff
--- org/apache/flink/streaming/api/graph/StreamConfig.java
+++ org/apache/flink/streaming/api/graph/StreamConfig.java
@@ -100,7 +100,7 @@
 	}

 	public Configuration getConfiguration() {
-		return config;
+		return configuration;
 	}

 	// ------------------------------------------------------------------------
```

---

## Patch 2 (signature: `559ba83e30`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-1836e08f-TP1-CP1-1-5738b79f94/output/patches/2.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/runtime/tasks/StreamTask.java`

```diff
--- org/apache/flink/streaming/runtime/tasks/StreamTask.java
+++ org/apache/flink/streaming/runtime/tasks/StreamTask.java
@@ -774,7 +774,7 @@

 						stateBackend = clazz.newInstance().createFromConfig(flinkConfig);
 					} catch (ClassNotFoundException e) {
-						throw new IllegalConfigurationException("Cannot find configured state backend: " + backendName);
+						throw new IllegalConfigurationException("Cannot find configured state backend: " + backendName, e);
 					} catch (ClassCastException e) {
 						throw new IllegalConfigurationException("The class configured under '" +
 								ConfigConstants.STATE_BACKEND + "' is not a valid state backend factory (" +
```

---

## Patch 3 (signature: `6216391251`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-1836e08f-TP1-CP1-1-5738b79f94/output/patches/4.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/runtime/tasks/StreamTask.java`

```diff
--- org/apache/flink/streaming/runtime/tasks/StreamTask.java
+++ org/apache/flink/streaming/runtime/tasks/StreamTask.java
@@ -338,7 +338,7 @@

 			// if the operators were not disposed before, do a hard dispose
 			if (!disposed) {
-				disposeAllOperators();
+				tryDisposeAllOperators();
 			}
 		}
 	}
```

---

## Patch 4 (signature: `7d6ee0c9e3`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-1836e08f-TP1-CP1-1-5738b79f94/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/runtime/tasks/StreamTask.java`

```diff
--- org/apache/flink/streaming/runtime/tasks/StreamTask.java
+++ org/apache/flink/streaming/runtime/tasks/StreamTask.java
@@ -769,7 +769,7 @@
 				default:
 					try {
 						@SuppressWarnings("rawtypes")
-						Class<? extends StateBackendFactory> clazz =
+						Class<? extends StateBackendFactory<?>> clazz =
 								Class.forName(backendName, false, getUserCodeClassLoader()).asSubclass(StateBackendFactory.class);

 						stateBackend = clazz.newInstance().createFromConfig(flinkConfig);
```

---

