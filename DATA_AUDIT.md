\# JAOS Data Audit



\## Overall Status



Status:

🟡 Active / Runtime Data Store



Priority:

HIGH



\## Purpose



The data directory stores JAOS runtime state including backups, behavior,

decisions, goals, action history, memory, profile, provider memory,

reasoning traces, recovery checkpoints, and snapshots.



\## Current Data Areas



| Folder | Role | Status |

|---|---|---|

| backups/ | Action history backups | Active |

| behavior/ | Behavior patterns | Active |

| cache/ | Runtime cache | Local runtime |

| decisions/ | Decision records | Active |

| diagnostics/ | Diagnostics output | Local runtime |

| goals/ | Goal records | Active |

| history/ | Action history | Active |

| memory/ | Long-term memory | Active |

| profile/ | User profile | Active |

| providers/ | Provider performance memory | Active |

| reasoning/ | Reasoning traces | Active |

| recovery/ | Crash checkpoints | Active |

| snapshots/ | System snapshots | Active |



\## Findings



Data contains real runtime outputs from earlier JAOS work.



This folder should not be deleted.



Some files may become local-only later depending on privacy, reproducibility,

and Git policy.



\## Final Decision



Keep data/.



Later define a Git tracking policy for runtime data, personal data, cache,

snapshots, backups, and generated diagnostics.

