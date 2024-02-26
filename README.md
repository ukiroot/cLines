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
    -n4 \                      # Run tests in 4 parallel threads
    -m "$SUITE_NAME" # Run tests which marked '@pytest.mark.preparation_resources'
```
### Run 'preparation_resources' suite