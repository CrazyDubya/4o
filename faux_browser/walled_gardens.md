# Walled Garden Strategy

This document outlines how different user profiles map to curated sets of websites. The goal is to keep browsing safe and focused while still allowing flexibility when additional content is needed.

## Domain Categories

- **Allowed Domains** – Pages that are always accessible once mirrored locally.
- **Soft-Allow Domains** – Sites that may be appropriate but require approval before use. The server will deny them by default and log the attempt.
- **Blocked Domains** – Pages that should never be served to the user. They are removed from the repository and attempts are logged.

## Profile Examples

- **Child Profile**
  - `allowed_domains`: educational and entertainment sites vetted for minors.
  - `soft_allow_domains`: school resources that might contain forums or user-generated content.
- **Researcher Profile**
  - `allowed_domains`: reference material and documentation sites.
  - `soft_allow_domains`: wider news sources that may contain unpredictable content.

By combining these lists the caretaker can craft a garden that fits each user's needs. The fetcher sanitizes all pages before they enter the repository, and the offline server enforces the profile when serving content.
