# Bug: bugsdotjar-repairllama-calcite-d4d7ab99-TP1-CP1-0-ac67bada3f

## Summary
- Total patch files: **5**
- Unique patches: **5**
- Invalid/unparseable patch files: **0**

## Patch 1 (signature: `31134ceb01`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-calcite-d4d7ab99-TP1-CP1-0-ac67bada3f/output/patches/0.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/calcite/avatica/jdbc/JdbcMeta.java`

```diff
--- org/apache/calcite/avatica/jdbc/JdbcMeta.java
+++ org/apache/calcite/avatica/jdbc/JdbcMeta.java
@@ -227,7 +227,7 @@
     if (metaData == null) {
       return Collections.emptyList();
     }
-    final List<AvaticaParameter> params = new ArrayList<>();
+   final List<AvaticaParameter> params = new ArrayList<>(metaData.getParameterCount());
     for (int i = 1; i <= metaData.getParameterCount(); i++) {
       params.add(
           new AvaticaParameter(metaData.isSigned(i), metaData.getPrecision(i),
```

---

## Patch 2 (signature: `34fec90309`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-calcite-d4d7ab99-TP1-CP1-0-ac67bada3f/output/patches/1.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/calcite/avatica/jdbc/JdbcMeta.java`

```diff
--- org/apache/calcite/avatica/jdbc/JdbcMeta.java
+++ org/apache/calcite/avatica/jdbc/JdbcMeta.java
@@ -228,7 +228,7 @@
       return Collections.emptyList();
     }
     final List<AvaticaParameter> params = new ArrayList<>();
-    for (int i = 1; i <= metaData.getParameterCount(); i++) {
+   for (int i = 0; i < metaData.getParameterCount(); i++) {
       params.add(
           new AvaticaParameter(metaData.isSigned(i), metaData.getPrecision(i),
               metaData.getScale(i), metaData.getParameterType(i),
```

---

## Patch 3 (signature: `44692e6f43`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-calcite-d4d7ab99-TP1-CP1-0-ac67bada3f/output/patches/4.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/calcite/avatica/jdbc/JdbcMeta.java`

```diff
--- org/apache/calcite/avatica/jdbc/JdbcMeta.java
+++ org/apache/calcite/avatica/jdbc/JdbcMeta.java
@@ -739,7 +739,7 @@
       int maxRowCount) {
     try {
       final Connection conn = getConnection(ch.id);
-      final PreparedStatement statement = conn.prepareStatement(sql);
+     final PreparedStatement statement = conn.prepareStatement(sql,
          ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY);
       final int id = System.identityHashCode(statement);
       statementCache.put(id, new StatementInfo(statement));
       StatementHandle h = new StatementHandle(ch.id, id,
```

---

## Patch 4 (signature: `d06c43f6a2`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-calcite-d4d7ab99-TP1-CP1-0-ac67bada3f/output/patches/2.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/calcite/avatica/jdbc/JdbcMeta.java`

```diff
--- org/apache/calcite/avatica/jdbc/JdbcMeta.java
+++ org/apache/calcite/avatica/jdbc/JdbcMeta.java
@@ -235,7 +235,7 @@
               metaData.getParameterTypeName(i),
               metaData.getParameterClassName(i), "?" + i));
     }
-    return params;
+   return Collections.unmodifiableList(params);
   }

   protected static Signature signature(ResultSetMetaData metaData,
```

---

## Patch 5 (signature: `d1f65e381c`)

**Source patch files (duplicates):**
- `bugsdotjar-repairllama-calcite-d4d7ab99-TP1-CP1-0-ac67bada3f/output/patches/3.patch`

**Modifications (unified diff):**

**Files modified:**
- `org/apache/calcite/avatica/jdbc/JdbcMeta.java`

```diff
--- org/apache/calcite/avatica/jdbc/JdbcMeta.java
+++ org/apache/calcite/avatica/jdbc/JdbcMeta.java
@@ -738,7 +738,7 @@
   public StatementHandle prepare(ConnectionHandle ch, String sql,
       int maxRowCount) {
     try {
-      final Connection conn = getConnection(ch.id);
+     final Connection conn = ch.connection;
       final PreparedStatement statement = conn.prepareStatement(sql);
       final int id = System.identityHashCode(statement);
       statementCache.put(id, new StatementInfo(statement));
```

---

