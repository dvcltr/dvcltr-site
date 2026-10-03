---
title: "Weekly Status: September 27–October 3, 2026"
date: 2026-10-03
course: "CYBR-510"
summary: "Executed 44 security tests against a deliberately vulnerable application and converted the evidence into a prioritized defect assessment and professional report."
tags: ["CYBR-510", "Security Test Engineering", "Test Automation", "Defect Analysis", "Security Reporting"]
draft: false
---

This week in CYBR-510 moved from test planning into hands-on execution, evidence collection, defect analysis, and professional reporting.

## Completed this week

- Built a Python PTY-based harness that interacted with the application through its normal terminal prompts.
- Executed 44 security tests against fresh, isolated copies of the application.
- Collected per-test evidence without using real accounts, passwords, or personal information.
- Assessed credential policy, lockout behavior, authentication, authorization, audit behavior, and data protection.
- Compared dynamic results with targeted source review and static-analysis output.
- Classified confirmed findings and developed practical remediation recommendations.
- Produced a completed test workbook, evidence package, defect register, and security test report.

## Project

### Address Book Appliance Security Test Campaign

**Focus:** Test Automation / Evidence Collection / Defect Assessment

**Summary:** I executed the security test design against a deliberately vulnerable command-line application. Each test ran against a fresh synthetic fixture so that test order and leftover state would not distort the results.

**Approach:** A PTY-based Python harness handled the application's interactive prompts, including masked password entry. The workflow captured sanitized evidence for every case and preserved the original installation data.

**What I learned:** Isolation and repeatability matter as much as individual test steps. Resetting the environment for each case makes failures easier to reproduce and prevents one test from hiding or causing another result.

### Security Findings and Reporting

**Focus:** Authentication / Authorization / Data Protection

**Summary:** The assessment identified weaknesses involving credential handling, failed-login controls, session identity, privileged-account protection, local file permissions, exported data, and audit integrity. I separated specification gaps from implementation defects and prioritized the recommended fixes.

**What I learned:** A useful finding explains more than the failure. It should show why the behavior matters, connect it to a requirement, identify the likely cause, and recommend a realistic corrective action.

### Static and Dynamic Analysis

**Focus:** Evidence Correlation / Software Assurance

**Summary:** Dynamic test behavior was compared with source-level reasoning and static-analysis output. Together, these evidence sources helped confirm root causes and identify concerns that were difficult to observe only through the user interface.

**What I learned:** Black-box testing, source review, and static analysis answer different questions. Combining them produces a stronger assessment than relying on any one technique by itself.

## Currently learning

- Automated command-line security testing
- Reproducible evidence collection
- Authentication and authorization testing
- Secure file and export handling
- Defect classification and prioritization
- Professional security assessment reporting

## Biggest takeaway

The biggest takeaway was that a strong security assessment is an evidence chain, not merely a list of failures. Reproducible execution, clear traceability, careful classification, and actionable recommendations make the results useful to both reviewers and developers.

## Next focus

- Apply feedback from the completed assessment.
- Continue refining risk-based prioritization and test traceability.
- Reuse the automation and reporting workflow in future security engineering work.
