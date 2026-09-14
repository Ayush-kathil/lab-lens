# Real-World Visual Triage Report

## Overview
This report documents the visual triage of the 16 candidate real-world images acquired from Wikimedia Commons. The goal is to determine the spatial value of each image based on whether it depicts a real laboratory setup with interacting components, rather than isolated equipment or diagrams.

## Criteria
- **HIGH**: Authentic laboratory setup depicting multiple interacting pieces of equipment (e.g., distillation, titration) with clear spatial relationships.
- **MEDIUM**: Plausible setup but lacking clear interaction or slightly ambiguous.
- **LOW**: Multiple pieces of equipment present, but not arranged in a functional setup (e.g., a row of empty beakers).
- **REJECTED**: Isolated equipment without context, or non-photographic images (e.g., diagrams, illustrations).
- **AMBIGUOUS**: Unclear or poor quality.

## Triage Results

### Initial Batch (rw_001 to rw_009)
*Originally gathered with isolated keyword searches.*
- **rw_001.jpg**: REJECTED - Isolated beaker.
- **rw_002.jpg**: REJECTED - Isolated beaker.
- **rw_003.jpg**: REJECTED - Isolated beaker setup (no interaction).
- **rw_004.jpg**: REJECTED - Isolated beaker.
- **rw_005.jpg**: LOW - Three isolated beakers.
- **rw_006.jpg**: LOW - Three isolated empty beakers.
- **rw_007.jpg**: REJECTED - Isolated beaker.
- **rw_008.jpg**: LOW - Collection of isolated flasks.
- **rw_009.png**: REJECTED - Isolated pipette bulb.

### Setup-Focused Batch (rw_010 to rw_016)
*Gathered specifically targeting "distillation" and "titration" setups.*
- **rw_010.jpg**: HIGH - Complex multi-flask setup on a retort stand.
- **rw_011.jpg**: HIGH - Titration setup showing a burette and stand.
- **rw_012.png**: REJECTED - Diagram of a titration setup (not a real-world photograph).
- **rw_013.jpg**: HIGH - Simple distillation setup (flask, condenser, heating mantle).
- **rw_014.jpg**: HIGH - Fractional distillation setup.
- **rw_015.png**: REJECTED - Illustration/diagram of a setup (not a real-world photograph).
- **rw_016.jpg**: HIGH - Titration setup showing a burette and a beaker below it.

## Summary
- **HIGH**: 5 images (`rw_010`, `rw_011`, `rw_013`, `rw_014`, `rw_016`)
- **MEDIUM**: 0 images
- **LOW**: 3 images (`rw_005`, `rw_006`, `rw_008`)
- **REJECTED**: 8 images

The HIGH value images will be the primary focus for human annotation using the workbench, as they provide actual spatial relationships required for spatial compliance reasoning.
