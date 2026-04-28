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
| DB migration | `db-expert` | db-expert | sonnet |
| 2+ independent tasks | `superpowers:dispatching-parallel-agents` | general-purpose | sonnet |
| Resume previous work | `superpowers:executing-plans` | general-purpose | sonnet |
| Research / docs lookup | context7 → `brainstorming` | general-purpose | sonnet |

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

**After triage, BEFORE computing the chain from the routing tables**, check
`SKILL.personal.md` for a `chains:` block. If the user has saved a named chain
that matches the current task signature, use it.

```
Step 1 — Read SKILL.personal.md (already loaded as override layer)
Step 2 — Look for a `chains:` block. Each entry has:
           name:    short label
           when:    keyword/phrase signals that should activate this chain
           chain:   the dispatch sequence using → and + operators
Step 3 — If any `when:` signal matches the current task → use that chain.
Step 4 — Otherwise → compute fresh from the routing tables below.
```

**Always announce when a named chain wins.** The transparency rule does not
change just because the chain came from storage:

```
Using your saved chain `ship-feature`:
  writing-plans → dispatching-parallel-agents → frontend-design + db-expert
```

The chain in storage IS the chain that fires — no special syntax, no
re-interpretation. If a saved chain is wrong, the user edits one file. No
slash command, no tooling.

Full design rationale + schema: see [`references/named-chains.md`](./references/named-chains.md).

---

## CATALOG CHECK — Always Run After Triage (Key Differentiator)

**After routing to a skill from the tables above, check for a more specific match:**

```
keyword = core noun from the task (e.g., "kubernetes", "stripe", "threejs", "langchain")

Step 1 — LOCAL CATALOG (fast, run first):
  ls ~/.agent/skills/ | grep -iE '<keyword>'      ← 1,400+ Antigravity skills
  ls ~/.claude/skills/ | grep -iE '<keyword>'     ← your installed custom skills
  ls ~/.composio-skills/composio-skills/ | grep -iE '<keyword>'  ← 940+ integrations

  If a more specific match exists → USE IT instead of the generic routing table entry.
  Example: task is "add Stripe webhooks" → table says "integration-specialist"
           but ls finds "stripe-automation" → use stripe-automation instead.

Step 2 — ONLINE CATALOG (run if Step 1 has no match):
  WebSearch: site:github.com "SKILL.md" claude <keyword>
  → If a repo with SKILL.md exists:
    git clone --depth 1 <url> ~/.claude/skills/<skill-name>/
    Then invoke the newly installed skill.

Step 3 — GENERATE (last resort):
  superpowers:writing-skills → write a custom skill for this task
```

**When to skip the catalog check:**
- The routing table already gives you a highly specific skill (e.g., `systematic-debugging`)
- Single-line fix or trivial command
- The keyword is too generic to produce useful results (e.g., "code", "file", "text")

Curated repo list + full validation gates: see [`references/catalog-check.md`](./references/catalog-check.md) and [`references/known-skill-repos.md`](./references/known-skill-repos.md).

---

## PERSONAL OVERRIDES

Add project-specific routing on top of this file:

```bash
curl -sL https://raw.githubusercontent.com/hussi9/skill-router/main/SKILL.personal.md \
  > ~/.claude/skills/skill-router/SKILL.personal.md
```

Edit `SKILL.personal.md` with your project signals. Your rules win over the core (CSS cascade model).

---

## DISPATCH PROTOCOL — How to Actually Run a Chain

This is what makes the **Model** column enforced and not advisory.

**Rule: every chain step that needs a model different from the parent session
runs as a subagent via the `Agent` tool**, with `model` and `subagent_type`
set explicitly from the routing triple.

```
For each step in the announced chain:

  IF step.model == parent_session_model AND step is not parallel-fan-out:
      → invoke Skill(<skill>) in-session  (cheaper, same context)

  ELSE:
      → Agent(
          subagent_type=<agent from triple>,
          model=<model from triple>,
          description="<step skill name>",
          prompt="""
            Use Skill: <skill from triple>
            Task: <relevant slice of the user's request>
            Context: <files / decisions the step needs>
          """
        )

  Wait for the step to return before launching the next sequential step.
  Parallel steps (operator `+`) launch together via a single message with
  multiple Agent tool calls.
```

**Why this matters:**

- The parent session can't hot-swap models mid-turn. The only way to enforce
  a different model on a step is to run that step in a subagent with `model`
  set on the `Agent` call.
- Subagents cost tokens for context-passing, but you save dramatically when
  a `haiku`-tier step would otherwise run on `opus`. For a 5-step chain with
  mixed complexity, this typically nets a 30-50% cost reduction.
- The parent session does light orchestration only. Heavy work happens at the
  right model.

**Logging the dispatch (for observability + statusline):**

After announcing the chain, append one JSON line to
`~/.claude/skill_router_log.jsonl` so the statusline can show progress:

```bash
echo '{"ts":"<ISO8601>","type":"chain-start","name":"<chain-name-or-computed>","steps":["step1","step2","step3"],"models":["sonnet","sonnet","opus"]}' \
  >> ~/.claude/skill_router_log.jsonl
```

After each step completes, append:
```bash
echo '{"ts":"<ISO8601>","type":"chain-step","name":"<chain-name>","step":2,"of":3,"skill":"<skill>","model":"<model>"}' \
  >> ~/.claude/skill_router_log.jsonl
```

The statusline reads this file to surface live chain progress — see
[`statusline.sh`](./statusline.sh).

---

## RED FLAGS — Signs You're About to Skip This

```
"This is simple"          → Simple things take 5s to route. Skip routing = hours wasted.
"I know what to do"       → Then routing confirms it. 5s cost, 0 downside.
"No match in table"       → Run Catalog Check above before giving up.
"Ambiguous task"          → Default to higher-complexity path (BUILD).
"I already know the skill" → Still run catalog check — a better one may exist.
```
