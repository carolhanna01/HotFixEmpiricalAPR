# Bug: bugsdotjar-repairllama-flink-31837a75-TP1-CP1-1-6b4c256098

## Summary
- Total patch files: **5**
- Unique patches: **4**
- Invalid/unparseable patch files: **1**

## Invalid / unparseable patch files
- `bugsdotjar-repairllama-flink-31837a75-TP1-CP1-1-6b4c256098/output/patches/2.patch` — empty diff

---

## Patch 1 (signature: `03f2cb2380`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-31837a75-TP1-CP1-1-6b4c256098/output/patches/4.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/api/datastream/ConnectedStreams.java`

```diff
--- org/apache/flink/streaming/api/datastream/ConnectedStreams.java
+++ org/apache/flink/streaming/api/datastream/ConnectedStreams.java
@@ -199,7 +199,7 @@
 	 */
 	public <R> SingleOutputStreamOperator<R> map(CoMapFunction<IN1, IN2, R> coMapper) {

-		TypeInformation<R> outTypeInfo = TypeExtractor.getBinaryOperatorReturnType(coMapper,
+		TypeInformation<R> outTypeInfo = TypeExtractor.getCoMapReturnType(coMapper,
 				CoMapFunction.class, false, true, getType1(), getType2(),
 				Utils.getCallLocationName(), true);
```

---

## Patch 2 (signature: `268895556d`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-31837a75-TP1-CP1-1-6b4c256098/output/patches/3.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/api/graph/StreamGraphGenerator.java`

```diff
--- org/apache/flink/streaming/api/graph/StreamGraphGenerator.java
+++ org/apache/flink/streaming/api/graph/StreamGraphGenerator.java
@@ -584,7 +584,7 @@
 				if (inputGroup == null) {
 					inputGroup = inputGroupCandidate;
 				} else if (!inputGroup.equals(inputGroupCandidate)) {
-					return "default";
+					return null;
 				}
 			}
 			return inputGroup == null ? "default" : inputGroup;
```

---

## Patch 3 (signature: `48d1cbde38`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-31837a75-TP1-CP1-1-6b4c256098/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/api/operators/StreamingRuntimeContext.java`

```diff
--- org/apache/flink/streaming/api/operators/StreamingRuntimeContext.java
+++ org/apache/flink/streaming/api/operators/StreamingRuntimeContext.java
@@ -138,7 +138,7 @@

 	@Override
 	public <T> ListState<T> getListState(ListStateDescriptor<T> stateProperties) {
-		requireNonNull(stateProperties, "The state properties must not be null");
+		requireNonNull(stateProperties, "The state descriptor must not be null");
 		try {
 			stateProperties.initializeSerializerUnlessSet(getExecutionConfig());
 			return operator.getPartitionedState(stateProperties);
```

---

## Patch 4 (signature: `af3819329b`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-flink-31837a75-TP1-CP1-1-6b4c256098/output/patches/1.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/flink/streaming/api/operators/StreamingRuntimeContext.java`

```diff
--- org/apache/flink/streaming/api/operators/StreamingRuntimeContext.java
+++ org/apache/flink/streaming/api/operators/StreamingRuntimeContext.java
@@ -140,6 +140,17 @@
 	public <T> ListState<T> getListState(ListStateDescriptor<T> stateProperties) {
 		requireNonNull(stateProperties, "The state properties must not be null");
 		try {
+			stateProperties.initializeSerializer(getExecutionConfig());
+			return operator.getPartitionedState(stateProperties);
+		} catch (Exception e) {
+			throw new RuntimeException("Error while getting state", e);
+		}
+	}
+
+	@Override
+	public <T> ReducingState<T> getReducingState(ReducingStateDescriptor<T> stateProperties) {
+		requireNonNull(stateProperties, "The state properties must not be null");
+		try {
 			stateProperties.initializeSerializerUnlessSet(getExecutionConfig());
 			return operator.getPartitionedState(stateProperties);
 		} catch (Exception e) {
@@ -148,17 +159,6 @@
 	}

 	@Override
-	public <T> ReducingState<T> getReducingState(ReducingStateDescriptor<T> stateProperties) {
-		requireNonNull(stateProperties, "The state properties must not be null");
-		try {
-			stateProperties.initializeSerializerUnlessSet(getExecutionConfig());
-			return operator.getPartitionedState(stateProperties);
-		} catch (Exception e) {
-			throw new RuntimeException("Error while getting state", e);
-		}
-	}
-
-	@Override
 	@Deprecated
 	public <S> OperatorState<S> getKeyValueState(String name, Class<S> stateType, S defaultState) {
 		requireNonNull(stateType, "The state type class must not be null");
```

---

