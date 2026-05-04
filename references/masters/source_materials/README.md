# Master Source Materials

This directory preserves full source materials used to build compact master-lens cards.

`buffett/`, `munger/`, and `ai_hedge_fund/` are Git submodules, not copied folders.

## Structure

```text
source_materials/
  README.md
  buffett/
    -> git@github.com:agi-now/buffett-skills.git
  munger/
    -> git@github.com:alchaincyf/munger-skill.git
  ai_hedge_fund/
    -> git@github.com:virattt/ai-hedge-fund.git
```

## Usage Rule

Use `references/masters/*.md` as the default execution cards for normal analysis.

Load files under this directory only when:

- the user asks for full source material,
- a master-lens detail is missing from the compact card,
- the task is learning-oriented rather than normal company analysis,
- an audit needs to trace a compact rule back to source material.

Relevant `ai_hedge_fund` source files currently include:

- `ai_hedge_fund/src/agents/ben_graham.py`
- `ai_hedge_fund/src/agents/aswath_damodaran.py`
- `ai_hedge_fund/src/agents/phil_fisher.py`

No equally direct source-material submodule has been added yet for Howard Marks, Greenwald, Greenblatt, Klarman, or Mauboussin / Rappaport.

## Token Discipline

Do not load all source materials by default. Select only the relevant source file.

## Install / Clone Notes

After cloning this repository, initialize source-material submodules with:

```bash
git submodule update --init --recursive
```

To refresh them later:

```bash
git submodule update --remote references/masters/source_materials/buffett
git submodule update --remote references/masters/source_materials/munger
git submodule update --remote references/masters/source_materials/ai_hedge_fund
```
