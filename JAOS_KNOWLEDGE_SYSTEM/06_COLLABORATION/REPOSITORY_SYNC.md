\# JAOS Repository Sync



Document ID: JKS-SYN-001



Version: 1.0.0



Status: 🟡 Living



Owner: Founder (Vinay B)



\---



\# Purpose



This document defines how JAOS changes are synchronized with the repository and GitHub.



\---



\# Current Sync Mode



Manual sync.



Automatic GitHub sync is not implemented yet.



\---



\# Manual Sync Rule



Every completed milestone must end with:



1\. Tests passed

2\. Documentation updated if required

3\. Knowledge System updated if required

4\. Git status checked

5\. Changes staged

6\. Commit created

7\. Push completed

8\. Milestone locked



\---



\# Standard Commands



```cmd

cd C:\\JARVIS

git status

git add .

git commit -m "type: message"

git push

