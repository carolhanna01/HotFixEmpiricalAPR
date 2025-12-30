# Bug: ambari_dba3fee7_2025-11-03_16-30-23

## Summary
- Total patch files: **3**
- Unique patches: **3**
- Patch files missing `<patched>` blocks: **0**

## Patch 1 (signature: `b502ef73df`)

**Source patch_raw files (duplicates):**
- `ambari_dba3fee7_2025-11-03_16-30-23/output_0/patch_raw_2.md`

**Modifications:**

### `ambari-agent/src/main/python/ambari_agent/manifestGenerator.py`

```python
def writeNonGlobalConfigurations(outputFile, xmlConfigs):
    outputFile.write('$configuration =  {\n')

    for configName in xmlConfigs.iterkeys():
        config = xmlConfigs[configName]
        logger.info("Generating " + configName + ",configurations =>\n" + pprint.pformat(config))
        outputFile.write(configName + '=> {\n')
        coma = ''
        for configParam in config.iterkeys():
            outputFile.write(coma + '"' + configParam + '" => \'' + str(config[configParam]) + '\'')
            coma = ',\n'

        outputFile.write('\n},\n')

    outputFile.write('\n}\n')
```

---

## Patch 2 (signature: `c3b6aa3bf9`)

**Source patch_raw files (duplicates):**
- `ambari_dba3fee7_2025-11-03_16-30-23/output_0/patch_raw_1.md`

**Modifications:**

### `ambari-agent/src/main/python/ambari_agent/manifestGenerator.py`

```python
def writeNonGlobalConfigurations(outputFile, xmlConfigs):
    outputFile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outputFile.write('<configuration>\n')

    for configName in xmlConfigs.iterkeys():
        config = xmlConfigs[configName]
        logger.info("Generating " + configName + ", configurations =>\n" + pprint.pformat(config))
        outputFile.write('  <' + configName + '>\n')
        for configParam, value in config.iteritems():
            outputFile.write('    <' + configParam + '>' + value + '</' + configParam + '>\n')
        outputFile.write('  </' + configName + '>\n')

    outputFile.write('</configuration>\n')
```

---

## Patch 3 (signature: `d4b91b1a45`) CH:SYMPTOM-HIDING

**Source patch_raw files (duplicates):**
- `ambari_dba3fee7_2025-11-03_16-30-23/output_0/patch_raw_0.md`

**Modifications:**

### `ambari-agent/src/main/python/ambari_agent/manifestGenerator.py`

```python
185     outputFile.write(configName + '=> {\n')
186     coma = ''
187     services_affected = []
188     for configParam in config.iterkeys():
189       if configParam == 'services_affected':
190         services_affected = config[configParam]
191       else:
192         outputFile.write(coma + '"' + configParam + '" => \'' + config[configParam] + '\'')
193         coma = ',\n'
194     if services_affected:
195       outputFile.write(',\n  "services_affected" => \'' + ','.join(services_affected) + '\'')
```

---

