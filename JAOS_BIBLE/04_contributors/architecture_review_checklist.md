\# JAOS Architecture Review Checklist



\## Purpose



This checklist is used before approving major changes.



\---



\## Questions



1\. Does this change fit the JAOS layered architecture?

2\. Does it belong in Alpha, Beta, or a future version?

3\. Does it create unnecessary complexity?

4\. Does it duplicate an existing component?

5\. Does it violate the rule: Executive Brain thinks, Kernel executes?

6\. Does it bypass the Permission Gateway?

7\. Does it introduce circular dependencies?

8\. Does it need a new Architecture Decision Record?

9\. Does it affect existing tests?

10\. Can it scale to future versions?



\---



\## Decision



Approve only if the change improves JAOS without weakening the architecture.

