---
title: "Two-Week Status: September 19–October 3, 2026"
date: 2026-10-03
course: "CYBR-510"
summary: "Designed and executed a security test campaign for a deliberately vulnerable command-line application, then turned the evidence into a traceable professional assessment."
tags: ["CYBR-510", "Security Test Engineering", "Test Automation", "Defect Analysis", "Security Requirements"]
draft: false
---

The last two weeks of CYBR-510 centered on moving from security requirements and test planning into hands-on execution, evidence collection, defect analysis, and professional reporting.

## Completed over the last two weeks

- Translated five security requirements into traceable scenarios and detailed test cases.
- Built a repeatable test workflow for a deliberately vulnerable command-line address book application.
- Executed 44 security tests in isolated copies of the application so each case began from a controlled state.
- Collected per-test evidence without using real accounts, passwords, or personal data.
- Assessed authentication, account lockout, authorization, data protection, and audit behavior.
- Used static analysis alongside dynamic testing to identify implementation and maintainability concerns.
- Produced a completed test workbook, defect register, evidence package, and professional security test report.

## Project

### Address Book Appliance Security Test Campaign

**Focus:** Security Test Design / Automation / Defect Assessment

**Summary:** I designed and executed a security test campaign against a deliberately insecure command-line application. The work connected each requirement to scenarios, test cases, evidence, observed results, and remediation guidance.

**Approach:** A Python PTY-based harness interacted with the application through its normal terminal prompts. Each test ran against a fresh synthetic fixture, which reduced test-order effects and protected the original installation data.

**What I learned:** Repeatability and isolation matter as much as the individual test steps. A finding is more defensible when the requirement, expected behavior, execution evidence, actual result, and recommendation can all be traced together.

### Security Findings and Reporting

**Focus:** Authentication / Authorization / Data Protection

**Summary:** The assessment identified weaknesses across credential policy, lockout behavior, session identity, privileged account protection, local file permissions, exported data handling, and audit integrity. I separated specification gaps from implementation defects and prioritized recommendations by severity.

**What I learned:** Security testing is not only about proving that something can fail. The report must explain why the behavior matters, whether the requirement itself is testable, and what a practical remediation should look like.

### Static and Dynamic Analysis

**Focus:** Evidence Correlation / Software Assurance

**Summary:** Dynamic test results were compared with targeted source review and static-analysis output. This helped confirm root causes and reveal additional issues that were difficult to observe through the interface alone.

**What I learned:** Black-box behavior, source-level reasoning, and static analysis provide different kinds of evidence. Combining them produces a more complete and credible assessment than relying on any one method.

## Currently learning

- Requirements-based security testing
- Test traceability and evidence management
- Authentication and authorization abuse cases
- Secure file and export handling
- Automated command-line application testing
- Defect classification and remediation writing
- Professional security assessment reporting

## Biggest takeaway

The biggest takeaway was that a strong security test deliverable is an evidence chain, not just a list of failures. Clear requirements, isolated execution, reproducible evidence, careful defect classification, and actionable recommendations turn testing into an assessment that other people can review and trust.

## Next focus

- Apply feedback from the completed security test assessment.
- Continue refining risk-based test prioritization and traceability.
- Build on the test harness and reporting workflow for future security engineering work.
