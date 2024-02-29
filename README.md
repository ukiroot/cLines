# vyos-tre

## Description:

vyos-tre is acronym from "VyOS Test Regression Environment"

## Block scheme:

```text
+-------------------------------------------------------+
|                   Test Environment                    |
|   +---------+      +---------+      +---------+       |
|   | +---------+    | +---------+    | +---------+     |
|   | | +---------+  | | +---------+  | | +---------+   |
|   | | |    VM   |  | | |  Linux  |  | | |   VM    |   |
|   +-+ |   EUTs  |  +-+ | bridges |  +-+ |  linux  |   |
|     +-+         |    +-interfaces|    +-+ clients |   |
|       +---------+      +---------+      +---------+   |
|                                                       |
+-----------------+-------------------------------------+
                  ^                                     |
                  | 2                                   |
                  |                                     |
+---------------------+   +-----------+                 |
|    Pool of tests|   |   |           |                 |
|   +---------+   |   |   |Transaction|                 |
|   | +---------+ |   |   |           |                 |
|   | | +---------+   |   +-----------+                 |
|   | | |         |   |   ^                             |
|   +-+ |  Test   |   |   | 1, 3                        |
|     +-+         |   |   |                             |
|       +---------+--------                             |
|                     |                                 |
+---------------------+----------------------------------

1 - test starts reserve transaction
2 - test reserves required resources
3 - test finishes reserve transaction
```

## Usage

### Test suites

1. `preparation_resources` - deploy EUTs, check linuxchan state, create bridge interfaces
2. `end_to_end_routing_smoke` - simple short test for check functionality of tests system

### Run 'preparation_resources' suite
```
pytest \
    -v \
    -s \
    -l \
    -n4 \                           # Run tests in 4 parallel threads
    -m "preparation_resources"      # Run tests which marked '@pytest.mark.preparation_resources'
```
### Run 'end_to_end' suite
```
pytest \
    -v \
    -s \
    -l \
    -n4 \
    --dist=loadfile --dist=each \    # Each pytest (python) process execute tests consequentially from a source file
                                \    # it's guarantee same context of static (global) variables in test scenario in source file
    -m "end_to_end"
```
