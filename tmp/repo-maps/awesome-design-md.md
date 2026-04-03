# Repo Map — awesome-design-md

## Path
- `C:\laragon\www\awesome-design-md`

## What it is
A curated content repository of `DESIGN.md` design-system documents inspired by public websites, meant to be copied into projects and used by AI/design agents as frontend style references.

## Mental model
This is **not** a runtime app/framework repo.
It is a **design reference library**.

## Core structure
- `README.md` — main catalog and purpose
- `CONTRIBUTING.md` — contribution rules and quality bar
- `design-md/<brand>/`
  - `DESIGN.md`
  - `preview.html`
  - `preview-dark.html`
  - `README.md`

## Standard per entry
Each design pack is expected to provide:
1. `DESIGN.md`
2. `preview.html`
3. `preview-dark.html`
4. `README.md`

## Required DESIGN.md sections
1. Visual Theme & Atmosphere
2. Color Palette & Roles
3. Typography Rules
4. Component Stylings
5. Layout Principles
6. Depth & Elevation
7. Do's and Don'ts
8. Responsive Behavior
9. Agent Prompt Guide

## Why it matters to Clio
Afu wants this repo remembered as a reusable design inspiration library for future web/frontend work.

## Best use cases
- choose a visual direction for a new web project
- borrow a design language for landing pages or dashboards
- reference typography / palette / spacing / tone when generating UI
- use as DESIGN.md-style guidance for AI-assisted frontend building

## Caveats
- content-heavy repo; consistency can drift between DESIGN.md and preview files
- not a runtime codebase
- should be treated as inspiration/reference, not source-of-truth product implementation

## Recommended workflow when using it
1. choose 1–3 reference brands
2. read their `DESIGN.md`
3. extract:
   - color logic
   - typography hierarchy
   - component tone
   - spatial mood
4. adapt, do not blindly clone
