---
name: skill-router
description: INVOKE BEFORE EVERY NON-TRIVIAL TASK — before writing code, before using any tool, before answering. Do not skip. Produces the required Skill + Agent + Model for the task. Routing engine for 2,700+ skills.
---

# Skill Router — Universal Router

**Output always:** `Skill + Agent + Model`

---

## THE 3-QUESTION TRIAGE (run now, takes 5 seconds)

```
Q1: Is something BROKEN / WRONG / FAILING?
    Error, crash, test fail, unexpected output, user correction
    YES → BROKEN PATH

Q2: Is this CREATE / BUILD / ADD something new?
    New feature, file, component, integration, page, script
    YES → BUILD PATH

Q3: Everything else (improve, ship, configure, automate, research)
    → OPERATE PATH

AMBIGUOUS? → Default to HIGHER-COMPLEXITY path
```

---

## BROKEN PATH

| Signal | Skill | Agent | Model | Thinking |
|--------|-------|-------|-------|----------|
| Error / crash / exception | `superpowers:systematic-debugging` | general-purpose | sonnet | think |
| Test failing | `test-runner` → `superpowers:systematic-debugging` | test-runner | sonnet | none |
| TypeScript errors | `typescript-expert` | general-purpose | sonnet | none |
| Performance regression | `perf` → `superpowers:systematic-debugging` | optimizer | sonnet | think |
| Security issue found | `security` | security-auditor | sonnet | think-hard |
| Deploy / build failed | `superpowers:systematic-debugging` | general-purpose | sonnet | think |
| User says "no" / "wrong" | STOP → `superpowers:systematic-debugging` | general-purpose | sonnet | think |
| Production incident | `superpowers:systematic-debugging` | general-purpose | **opus** | **ultrathink** |

---

## BUILD PATH

**Multi-file / new feature:** `brainstorming` → `writing-plans` → domain skill
**Single file / trivial add:** go directly to domain skill

| What | Skill | Agent | Model | Thinking |
|------|-------|-------|-------|----------|
| UI component / page | `frontend-design:frontend-design` | feature-dev:code-architect | sonnet | none |
| API endpoint | `system-design` | feature-dev:code-architect | sonnet | think |
| Database schema | `db-expert` | db-expert | sonnet | think |
| Auth / permissions | `brainstorming` → `security` | security-auditor | opus | **ultrathink** |
| AI feature / agent | `langgraph` → `rag-engineer` | feature-dev:code-architect | sonnet | think-hard |
| 3rd-party integration | composio skill for that app | integration-specialist | sonnet | none |
| Mobile screen | `mobile-developer` → `frontend-design:frontend-design` | feature-dev:code-architect | sonnet | none |
| CLI / automation script | `system-design` | general-purpose | sonnet | think |
| Skill / Claude skill file | `superpowers:writing-skills` | general-purpose | sonnet | think |

---

## OPERATE PATH

| Signal | Skill | Agent | Model | Thinking |
|--------|-------|-------|-------|----------|
| Refactor / clean up | `refactor` | code-simplifier:code-simplifier | sonnet | none |
| Add tests / coverage | `superpowers:test-driven-development` | test-runner | sonnet | none |
| Performance optimize | `perf` | optimizer | sonnet | think |
| Write docs | `docs` | general-purpose | sonnet | none |
| Code review | `superpowers:requesting-code-review` | superpowers:code-reviewer | sonnet | think-hard |
| Got review feedback | `superpowers:receiving-code-review` | general-purpose | sonnet | think |
| Deploy | `superpowers:verification-before-completion` → `vercel:deploy` | general-purpose | sonnet | none |
| Merge / PR / push | `superpowers:finishing-a-development-branch` | general-purpose | sonnet | none |
| DB migration | `db-expert` | db-expert | sonnet | think |
| 2+ independent tasks | `superpowers:dispatching-parallel-agents` | general-purpose | sonnet | none |
| Resume previous work | `superpowers:executing-plans` | general-purpose | sonnet | none |
| Research / docs lookup | context7 → `brainstorming` | general-purpose | sonnet | none |
| Architecture / scope decision | `brainstorming` → `system-design` | general-purpose | opus | **ultrathink** |

---

## WHEN NO SKILL IS NEEDED

Single-line fix · reading code · one factual question · one command · under 3 trivial steps

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

## COMPLEXITY RULE

```
1 domain  → 1 skill
2+ domains → announce chain, run in order

"This touches [N] domains. Chain: [skill1] → [skill2] → ...
Invoking step 1 now."
```

Operators in the chain:
- `→` sequential (B depends on A)
- `+` parallel (steps don't share state)

Full chain syntax + standard shapes: see [`references/multi-domain-chaining.md`](./references/multi-domain-chaining.md).

---

## NAMED CHAIN LOOKUP — Run Before Computing Fresh

After triage, BEFORE computing fresh, check `SKILL.personal.md` for a
`chains:` block. If any `when:` substring matches the user's prompt
(case-insensitive, first match wins), use the saved chain instead.

When a saved chain wins, announce it with provenance:
```
Using your saved chain `<name>`: <step1> → <step2> + <step3>
```

Schema, match algorithm, per-step model resolution: [`references/named-chains.md`](./references/named-chains.md).

---

## CATALOG CHECK — Run After Routing-Table Lookup (Key Differentiator)

If the table returned a generic skill (e.g. `integration-specialist`),
search local + remote catalogs for a more specific match. If found, use
the specialist instead.

```
1. Local: ls ~/.agent/skills/, ~/.claude/skills/, ~/.composio-skills/  | grep -iE '<keyword>'
2. Remote: site:github.com "SKILL.md" claude <keyword>  (4 curated repos in ref doc)
3. Generate: superpowers:writing-skills (last resort)
```

Skip when: routing-table answer is already specialist · single-line fix ·
keyword is too generic ("code", "file", "text").

Full validation gates + curated repos: [`references/catalog-check.md`](./references/catalog-check.md), [`references/known-skill-repos.md`](./references/known-skill-repos.md).

---

## PERSONAL OVERRIDES

Add project-specific routing on top of this file:

```bash
curl -sL https://raw.githubusercontent.com/hussi9/skill-router/main/SKILL.personal.md \
  > ~/.claude/skills/skill-router/SKILL.personal.md
```

Edit `SKILL.personal.md` with your project signals. Your rules win over the core (CSS cascade model).

---

## THINKING DEPTH — Pre-pend the Right Keyword

Pre-pend the routing row's `Thinking` value as the literal first word of the
dispatch prompt:

| Value | Pre-pend |
|-------|----------|
| `none` | (nothing) |
| `think` | `think.` |
| `think-hard` | `think hard.` |
| `ultrathink` | `ultrathink.` |

Do not paraphrase. If a community `ultrathink` / `think-hard` skill is
installed, invoke that skill INSTEAD of the bare keyword.

Full rules + community alternatives: [`references/thinking-depth.md`](./references/thinking-depth.md).

---

## DISPATCH PROTOCOL — How Each Step Actually Runs

This is what makes the **Model** column enforced, not advisory.

```
For each step in the announced chain:
  IF step.model == parent_model AND not parallel-fan-out:
      → Skill(<skill>) in-session   (cheaper, same context)
  ELSE:
      → Agent(subagent_type=<agent>, model=<model>,
              prompt="<thinking-keyword>. Use Skill: <skill>. Task: <slice>. Context: <files>")
  Sequential `→`: wait. Parallel `+`: one message, multiple Agent calls.
```

After dispatching, write log lines to `~/.claude/skill_router_log.jsonl`
(`chain-start`, `chain-step`, `thinking-active`, `chain-end`) for the
statusline + the `scripts/audit-dispatch.py` compliance auditor.

Full event schema, common skip patterns, and verification: [`references/dispatch-protocol.md`](./references/dispatch-protocol.md).

---

## RED FLAGS — Signs You're About to Skip This

```
"This is simple"          → Simple things take 5s to route. Skip routing = hours wasted.
"I know what to do"       → Then routing confirms it. 5s cost, 0 downside.
"No match in table"       → Run Catalog Check above before giving up.
"Ambiguous task"          → Default to higher-complexity path (BUILD).
"I already know the skill" → Still run catalog check — a better one may exist.
```
