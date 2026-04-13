---
name: skills-master-core
description: Universal routing core for Claude Code. 3-question triage → domain routing → Skill + Agent + Model. Drop into any Claude Code setup. Works standalone or as the base for a personal override layer.
---

# Skills Master — Universal Core

> Before any non-trivial task: run this. Always produces one answer.

---

## THE 3-QUESTION TRIAGE

```
Q1: Is something BROKEN / WRONG / FAILING?
    Error, crash, test fail, unexpected output, user correction
    YES → BROKEN PATH

Q2: Is this CREATE / BUILD / ADD something new?
    New feature, file, component, integration, page, script
    YES → BUILD PATH

Q3: Everything else (improve, ship, configure, automate, research, resume)
    → OPERATE PATH

AMBIGUOUS (spans 2 paths)?
    → Default to the HIGHER-COMPLEXITY path
    "Fix AND add feature" → BUILD PATH
    "Refactor AND deploy" → BUILD PATH (treat deploy as part of it)
```

---

## BROKEN PATH

| Signal | Skill | Agent | Model |
|--------|-------|-------|-------|
| Error / crash / exception | `superpowers:systematic-debugging` | general-purpose | sonnet |
| Test failing | `test-runner` → `superpowers:systematic-debugging` | test-runner | sonnet |
| TypeScript errors | `typescript-expert` | general-purpose | sonnet |
| Performance regression | `perf` → `superpowers:systematic-debugging` | optimizer | sonnet |
| Security issue found | `security` | security-auditor | sonnet |
| Deploy / build failed | `superpowers:systematic-debugging` | general-purpose | sonnet |
| User says "no" / "wrong" | STOP → `superpowers:systematic-debugging` | general-purpose | sonnet |
| Production incident | `superpowers:systematic-debugging` | general-purpose | **opus** |

---

## BUILD PATH

**Multi-file / new feature:** `brainstorming` → `writing-plans` → domain skill
**Single file / trivial add:** go directly to domain skill

| What | Skill | Agent | Model |
|------|-------|-------|-------|
| UI component / page | `frontend-design:frontend-design` | feature-dev:code-architect | sonnet |
| API endpoint | `system-design` | feature-dev:code-architect | sonnet |
| Database schema | `db-expert` | db-expert | sonnet |
| Auth / permissions | `brainstorming` → `security` | security-auditor | opus |
| AI feature / agent | `langgraph` → `rag-engineer` | feature-dev:code-architect | sonnet |
| 3rd-party integration | composio skill for that app | integration-specialist | sonnet |
| Mobile screen | `mobile-developer` → `frontend-design:frontend-design` | feature-dev:code-architect | sonnet |
| CLI / automation script | `system-design` | general-purpose | sonnet |
| Skill / Claude skill file | `superpowers:writing-skills` | general-purpose | sonnet |

---

## OPERATE PATH

| Signal | Skill | Agent | Model |
|--------|-------|-------|-------|
| Refactor / clean up | `refactor` | code-simplifier:code-simplifier | sonnet |
| Add tests / coverage | `superpowers:test-driven-development` | test-runner | sonnet |
| Performance optimize | `perf` | optimizer | sonnet |
| Write docs | `docs` | general-purpose | sonnet |
| Code review | `superpowers:requesting-code-review` | superpowers:code-reviewer | sonnet |
| Got review feedback | `superpowers:receiving-code-review` | general-purpose | sonnet |
| Deploy | `superpowers:verification-before-completion` → `vercel:deploy` | general-purpose | sonnet |
| Merge / PR / push | `superpowers:finishing-a-development-branch` | general-purpose | sonnet |
| Env var / secret | check secrets manager → `vercel:env` | general-purpose | sonnet |
| DB migration | `db-expert` | db-expert | sonnet |
| Cron / scheduled job | `schedule` skill | general-purpose | sonnet |
| 3rd-party connect | composio skill → `connect-apps` | integration-specialist | sonnet |
| Research / docs lookup | context7 → `brainstorming` | general-purpose | sonnet |
| Resume previous work | read task list → `superpowers:executing-plans` | general-purpose | sonnet |
| Update CLAUDE.md | `claude-md-management:revise-claude-md` | general-purpose | sonnet |
| 2+ independent tasks | `superpowers:dispatching-parallel-agents` | general-purpose | sonnet |

---

## COMPLEXITY RULE

```
1 domain  → 1 skill
2+ domains → announce chain, run in order

ANNOUNCE:
"This touches [N] domains. Chain: [skill1] → [skill2] → ...
Invoking step 1 now."
```

---

## COMPLETION GATE

Before any "done" claim → `superpowers:verification-before-completion`

```
□ Code actually runs correctly
□ TypeScript passes (tsc --noEmit)
□ Tests pass
□ Original request fully met (re-read it)
```

---

## WHEN NO SKILL IS NEEDED

Single-line fix · reading code · one factual question · one command · under 3 trivial steps

---

## SKILL REGISTRY

New skills installed? Run this once per session:

```
Check: ls -lt ~/.agent/skills/ | head -5
Check: ls -lt ~/.claude/skills/ | head -5
For each new skill: read first 5 lines of SKILL.md
Does it apply to today's work? → use it
Better than an existing routing entry? → use it instead
```

Add new routing permanently:
```
claude-md-management:revise-claude-md
"Add [skill] to skills-master under [section] for signal: [trigger]"
```

---

## NO MATCH? DISCOVERY PROTOCOL

```
1. ls ~/.agent/skills/ | grep -iE '<keyword>'        ← Antigravity (860+)
2. ls ~/.claude/skills/ | grep -iE '<keyword>'       ← Composio + custom
3. WebFetch Antigravity README → npx antigravity-awesome-skills
4. WebSearch: site:github.com "SKILL.md" claude <keyword>
5. git clone --depth 1 <url> /tmp/s && cp SKILL.md → ~/.claude/skills/<name>/
6. superpowers:writing-skills → write it yourself
```
