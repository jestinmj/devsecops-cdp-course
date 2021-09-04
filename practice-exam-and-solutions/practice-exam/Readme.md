CDP Exam Practice
================================================================


A Practice exam
----------------------------------------------------------------

Thank you for taking the DevSecOps Professional Practice Exam.

Please read and understand the information presented here carefully as it contains important information to attempt and pass the mock exam.

No Guarantee.
----------------------------------------------------------------

Passing this practice exam doesn’t guarantee or suggest that you are ready for the certification exam. This is added purely for testing your confidence before taking the exam.

Best way to approach this exam
--------------------------------

Here are a few pointers to keep in mind while taking this practice test

1. Do not refer your notes or videos while taking this practice exam
2. You can use google or the security tool’s documentation during the practice exam
3. Document everything as if its a real exam

All rights reserved to Hysn Technologies Inc and its affiliates.
--------------------------------

No part of this publication/exam may be reproduced, copied, transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without the prior written permission of Hysn Technologies Inc.

In short, you are not allowed to discuss and/or share the examination questions/answers with anyone without our permission.


Exam Details
--------------------------------

You have 2 hours to solve 2 challenges in order to achieve 40 points to pass, out of a total score of 50. You need to satisfy all the requirements mentioned in a challenge to gain complete points.

Please take notes of enough details so anyone can reproduce the steps to solve these exam challenges.

Each challenge solution should at least include:

- Step by step instructions
- Files used (like .gitlab-ci.yml, roles, playbook.yml, etc.)
- Screenshots
- Output/Results (in a machine-readable format like JSON, XML).

> You do not need to share the exam solutions with our staff as you can self evaluate these in the next exercise.

Lab architecture and Tools
--------------------------------
The practice exam labs are similar to the course labs but we do introduce differences in the exam so please pay attention to the commands and the environment.

Various machines in the lab
--------------------------------
We have numerous machines in the practice exam lab. Each of these machines serve a purpose.

- DevSecOps Box :	This machine acts as a developer/security engineer machine and contains many DevSecOps tools in it
- Gitlab :	This machine contains a source code management system (SCM), CI/CD system and many other tools
- Gitlab runner: 	This machine acts as a slave machine in master/slave systems architecture and executes commands given by  Gitlab master
- Production :	This machine acts as the production machine
- Vulnerability Management: 	This machine hosts vulnerability management software to manage the vulnerabilities found as part of the day to day security scans

Machines in the lab and their domain names
--------------------------------
- DevSecOps-Box: 	devsecops-box-XqiHnDZ0
- Git server: 	gitlab-ce-XqiHnDZ0
- CI/CD: 	gitlab-ce-XqiHnDZ0
- Prod: 	prod-XqiHnDZ0
- Vulnerability Management: 	dojo-XqiHnDZ0


Access Deployed Web Services and ports
--------------------------------

Defect Dojo Upload Script
--------------------------------

If you wish, you can download a simple Defect Dojo upload script using the following command.

```
curl https://gitlab.practical-devsecops.training/-/snippets/3/raw -o upload-results.py
```

Challenges
--------------------------------

You need to solve two challenges in two hours.

Challenge 1 (25 points)
--------------------------------
1. Implement SCA, SAST, DAST for the django.nv project
2. Please embed these tests in CI/CD pipeline
3. Ensure all the best practices covered in the course videos, labs and slack discussion are being implemented

Challenge 2 (25 points)
--------------------------------

1. Harden the production machine
2. Ensure it stays compliant with linux-baseline Inspec Profile
3. Embed these tests as part of CI/CD pipeline

> Good luck with the practice exam
