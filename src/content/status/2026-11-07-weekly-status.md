---
title: "Weekly Status: November 1–7, 2026"
date: 2026-11-07
course: "CYBR-512"
summary: "Built a three-VM intrusion detection lab with Snort monitoring traffic between an attacker and a vulnerable target."
tags: ["CYBR-512", "Snort", "Intrusion Detection", "VirtualBox", "Lab Setup"]
draft: false
---

This week in CYBR-512 was about building the lab: an isolated network where attacks can be launched and observed by an intrusion detection system.

## Completed this week

- Submitted the Snort setup assignment with a documented, screenshot-backed lab build.
- Studied Module 2 material on intrusion detection systems.

## Project

### Snort intrusion detection lab

**Focus:** Network IDS / Lab architecture

**Summary:** Set up three virtual machines on a single isolated VirtualBox NAT network: a Kali Linux attacker, a deliberately vulnerable Metasploitable 2 target, and a dedicated Linux sensor running Snort. The attacker and target VMs carried over from CYBR-510, so the new work centered on installing, configuring, and verifying the IDS.

**What I learned:** A sensor is only useful if it can actually see the traffic it is meant to inspect. Network placement and configuration matter as much as the detection rules.

## Currently learning

- Snort installation and configuration
- Network intrusion detection concepts
- Documenting a lab build as evidence

## Biggest takeaway

Detection begins with visibility. Before any alert can be trusted, the sensor's view of the network has to be verified.

## Next focus

- Use Snort to detect attacks launched in the lab.
- Begin Module 3 on Security Information and Event Management (SIEM).
