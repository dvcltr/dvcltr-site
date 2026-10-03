---
title: "Weekly Status: September 19–26, 2026"
date: 2026-09-26
course: "CYBR-510"
summary: "Turned security requirements for a deliberately vulnerable command-line application into a traceable test plan with scenarios, cases, priorities, and evidence expectations."
tags: ["CYBR-510", "Security Test Engineering", "Test Design", "Security Requirements", "Risk Assessment"]
draft: false
---

This phase of CYBR-510 focused on converting security requirements into a structured, repeatable test plan for a deliberately vulnerable command-line address book application.

## Completed this week

- Analyzed five requirements covering credentials, account lockout, authentication, authorization, and sensitive-data protection.
- Translated the requirements into security test scenarios and detailed test cases.
- Defined expected outcomes, prerequisites, cleanup steps, priorities, and evidence requirements.
- Built a traceability structure connecting every requirement to its scenarios and test cases.
- Planned boundary, negative, state-transition, timing, role-based, and data-isolation tests.
- Identified places where ambiguous specifications could make a security requirement difficult to test consistently.
- Designed the test workflow around disposable accounts and synthetic data to keep the lab isolated and safe.

## Project

### Security Test Design for a Command-Line Application

**Focus:** Requirements Analysis / Test Planning / Traceability

**Summary:** I developed a requirements-based security test design for a deliberately insecure address book application. The plan covered password policy, failed-login behavior, session identity, role restrictions, record ownership, local data protection, and audit evidence.

**Approach:** Each security requirement was decomposed into focused scenarios and individual test cases. The cases documented the expected result, test data, preconditions, post-test cleanup, and evidence needed to support the final assessment.

**What I learned:** A security requirement is only useful when it is specific enough to test. Ambiguous language around password strength, lockout behavior, and data protection can create uncertainty about what passing behavior should actually look like.

### Building the Evidence Chain

**Focus:** Test Traceability / Assessment Quality

**Summary:** The workbook connected requirements, scenarios, test cases, expected outcomes, execution status, evidence references, and defects. This created a structure that could support both technical review and final reporting.

**What I learned:** Traceability makes testing easier to defend. A reviewer should be able to move from a requirement to a test, then from the observed result to supporting evidence and a remediation recommendation.

## Currently learning

- Requirements-based security testing
- Boundary and negative test design
- Authentication and authorization abuse cases
- Risk-based test prioritization
- Test traceability and evidence planning
- Specification analysis

## Biggest takeaway

The biggest takeaway was that strong execution starts with precise test design. Defining the expected result, evidence, and cleanup process in advance makes the eventual findings more repeatable and credible.

## Next focus

- Execute the planned cases in isolated application copies.
- Automate repeatable command-line interactions.
- Collect evidence and classify any confirmed defects.
- Turn the results into a professional security test report.
