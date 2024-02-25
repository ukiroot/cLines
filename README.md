# vyos-tre

## Description:

vyos-tre is acronym from "VyOS Test Regression Environment"

## Block scheme:

```text
+-------------------------------------------------------+
|                   Pool of resources                   |
|   +---------+      +---------+      +---------+       |
|   | +---------+    | +---------+    | +---------+     |
|   | | +---------+  | | +---------+  | | +---------+   |
|   | | |         |  | | |         |  | | |         |   |
|   +-+ |   EUT   |  +-+ | bridges |  +-+ |linuxchan|   |
|     +-+         |    +-+         |    +-+         |   |
|       +---------+      +---------+      +---------+   |
|                                                       |
+-----------------+-------------------------------------+
                  ^                                     ^
                  | 5, 7                                |
                  |                                     |
+---------------------+   +-----------+                 |
|    Pool of tests|   |   |           |                 | 2
|   +---------+   |   |   |Transaction|                 |
|   | +---------+ |   |   |           |                 |
|   | | +---------+   |   +-----------+                 |
|   | | |         |   |   ^           ^   --------------+
|   +-+ |  Test   |   |   | 6         | 1 |             |
|     +-+         |   |   |           |   |   cLines    |
|       +---------+--------           ----+             |
|                     |       3, 4        |             |
+---------------------+<------------------+-------------+
```
