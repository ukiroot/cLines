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
