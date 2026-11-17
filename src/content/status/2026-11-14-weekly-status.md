---
title: "Weekly Status: November 8–14, 2026"
date: 2026-11-14
course: "CYBR-512"
summary: "Wrapped up CYBR-510 and replayed penetration-test attacks against a Snort-monitored lab to study how real intrusions appear as alerts."
tags: ["CYBR-512", "CYBR-510", "Snort", "Intrusion Detection", "Alert Analysis"]
draft: false
---

This week closed out CYBR-510, Security Test Engineering, and put the new Snort lab to work in CYBR-512.

## Completed this week

- Finished CYBR-510, completing another course in the program.
- Worked through the Snort intrusion detection assignment, replaying lab attacks with the IDS watching; it was finalized at the start of the following week.
- Continued Module 2 coursework on intrusion detection systems.

## Project

### Detecting intrusions with Snort

**Focus:** Alert analysis / Signal vs. noise

**Summary:** Re-ran much of the CYBR-510 penetration-test exercise from the Kali attacker against the Metasploitable 2 target, this time with the Snort sensor monitoring the same isolated network. The goal was to examine the alerts each attack generated and connect them back to the activity that caused them.

**What I learned:** Intrusion analysis is largely about finding the true positives among the false positives. Knowing exactly which attacks were launched made it much easier to judge which alerts mattered.

## Currently learning

- Reading and interpreting Snort alerts
- Separating true positives from false positives
- Mapping attacker activity to sensor evidence

## Biggest takeaway

Running the same attacks from both sides of the sensor shows how much context an analyst needs. An alert is a starting point for investigation, not a conclusion.

## Next focus

- Install and try out a SIEM for centralized log analysis.
- Practice threat hunting with SIEM data.
- Continue the course's incident-handling lab modules.
