\# JAOS Tool Platform Migration Plan



\## Decision



The canonical Tool Platform is:



```text

jaos/tools/

```



The legacy Tool Platform is:



```text

executive\_brain/tools/

```



\## Migration Map



| Legacy | Canonical | Status |

|---|---|---|

| executive\_brain/tools/core | jaos/tools | Migrating |

| executive\_brain/tools/file | jaos/tools/filesystem | Migrated |

| executive\_brain/tools/browser | jaos/tools/browser | Pending |

| executive\_brain/tools/windows | jaos/tools/windows | Pending |

| executive\_brain/tools/development | jaos/tools/development | Pending |



\## Safety Note



Legacy delete tools may delete directly.



Canonical delete tools must pass through:



```text

ToolPermissionManager

ToolApprovalManager

ToolAuditLogger

ToolExecutionEngine

```



\## Rule



```text

Do not extend legacy Tool Platform.

Only migrate useful behavior into jaos/tools/.

```

