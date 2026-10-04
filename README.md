# 🕷️ sysadmin-automation-toolkit — Abo_Omar Engineering

A collection of production-ready automation scripts for web scraping, data cleaning, and server alerting — built to be dropped into real environments and scheduled without modification.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
  - [Web Scraping](#web-scraping)
  - [Data Cleaning](#data-cleaning)
  - [Server Alerting](#server-alerting)
  - [Bash Scripts](#bash-scripts)
- [Scheduling with Cron](#-scheduling-with-cron)
- [Environment Variables](#-environment-variables)
- [Security Notes](#-security-notes)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 Overview

This repository contains 12 standalone automation scripts organized into four categories:

| Category | Scripts | Purpose |
| :--- | :--- | :--- |
| **Scrapers** | 3 | Extract data from public APIs and websites |
| **Data Cleaners** | 3 | Sanitize, normalize, and deduplicate datasets |
| **Alerters** | 3 | Monitor servers and push alerts to Telegram/Slack |
| **Bash Utilities** | 3 | Backup, log rotation, and health checks |

Every script is:
- **Self-contained**: no hidden dependencies between scripts.
- **Idempotent**: safe to run repeatedly.
- **Configurable**: via CLI args or environment variables.
- **Observable**: logs to stdout/stderr with timestamps.
- **Rate-limit aware**: respects target servers with delays.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                 sysadmin-automation-toolkit                 │
└─────────────────────────────────────────────────────────────┘

   DATA SOURCES                    PIPELINE                    SINKS
   ────────────                    ────────                    ─────

   ┌──────────┐                ┌──────────────┐           ┌──────────┐
   │ Hacker   │───┐            │              │           │  JSON    │
   │ News API │   │            │   Scrapers   │──────────▶│  Files   │
   └──────────┘   │            │              │           └──────────┘
                  │            └──────┬───────┘
   ┌──────────┐   │                   │                   ┌──────────┐
   │   BBC    │───┼───────────────────┤                   │   CSV    │
   │   HTML   │   │                   │                   │  Files   │
   └──────────┘   │                   │                   └──────────┘
                  │            ┌──────▼───────┐
   ┌──────────┐   │            │              │           ┌──────────┐
   │ RemoteOK │───┘            │   Cleaners   │──────────▶│  Ready   │
   │   API    │                │              │           │  Data    │
   └──────────┘                └──────────────┘           └──────────┘

   ┌──────────┐                ┌──────────────┐           ┌──────────┐
   │  Server  │                │              │           │ Telegram │
   │ Metrics  │───────────────▶│   Monitor    │──────────▶│   Bot    │
   └──────────┘                │              │           └──────────┘
                               └──────┬───────┘
                                      │                   ┌──────────┐
                                      └──────────────────▶│  Slack   │
                                                          │ Webhook  │
                                                          └──────────┘
