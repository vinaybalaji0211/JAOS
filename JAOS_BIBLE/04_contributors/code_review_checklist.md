\# JAOS Code Review Checklist



\## General



\- Does the code follow JAOS architecture?

\- Is the code readable?

\- Are names clear?

\- Is the file placed in the correct folder?

\- Does the component have one responsibility?



\---



\## Testing



\- Are unit tests included?

\- Were all related tests run?

\- Does the change break existing tests?



\---



\## Safety



\- Does this bypass permissions?

\- Does this access files, apps, or system features safely?

\- Does this introduce security risks?



\---



\## Maintainability



\- Is there unnecessary duplication?

\- Is there premature abstraction?

\- Can this be understood by another contributor?



\---



\## Approval



A change can be merged only when:



\- tests pass

\- architecture is respected

\- no critical issue remains

