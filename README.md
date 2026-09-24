# SpecBuddy + OpenSpec Learning

A hands-on project for learning and practicing Spec-Driven Development with OpenSpec, SpecBuddy, and OpenCode.

## Project Overview

This project uses a simple Python Mini Calculator to demonstrate the OpenSpec workflow:

`Explore → Proposal → Specs → Design → Tasks → Apply → Sync → Archive`

## Changes

### 1. add-subtract-operation

Added subtraction support to the existing CLI while preserving the default addition behavior.

```text
python calc.py 2 3
python calc.py --subtract 5 3
python calc.py -s 5 3
