---
name: skills-master-personal
description: Personal routing overrides. Layers on top of skills-master-core. Copy this file to ~/.claude/skills/skills-master/SKILL.personal.md and customize.
---

# Skills Master — Personal Overrides Template

**How this works:**
- The universal core (SKILL.md) runs first and handles 90% of tasks
- This file adds project-specific routing that overrides or extends the core
- Your rules always win over the core rules (CSS cascade model)

---

## HOW TO USE

1. Copy to `~/.claude/skills/skills-master/SKILL.personal.md`
2. Replace the example sections below with your own projects
3. Add rows to the routing tables for signals specific to your work
4. The core SKILL.md loads first — only add things the core doesn't cover

---

## PERSONAL OVERRIDES — Add Your Projects Here

### [Your Project Name]

| Signal | Skill | Agent | Model |
|--------|-------|-------|-------|
| Replace with your signal | replace-with-skill | general-purpose | sonnet |

### Multi-Platform Rule (if you work across web + mobile)

```
ANY feature touching [your app]:
  → BOTH platforms must be implemented before "done"
  → Web (apps/web) + Mobile (apps/mobile)
```

---

## EXECUTION GUARDRAILS — Add Your Own

```
[Add rules that apply automatically to your specific stack]

Example:
  Supabase touched?   → run supabase gen types after schema changes
  iOS feature?        → test on simulator before "done"
  Payment flow?       → security-auditor review before merge
```

---

## COMPLETION GATES — Extended

```
[Add domain-specific gates for your stack]

Example:
  DATABASE:
    □ Migration written and applied
    □ Types regenerated

  MOBILE:
    □ Web done
    □ Mobile done
    □ Both tested
```

---

## EXAMPLE — What A Real Personal Override Looks Like

```markdown
### MyApp — Backend (Node/Postgres)

| Signal | Skill | Agent | Model |
|--------|-------|-------|-------|
| gRPC service change | system-design → test | integration-specialist | sonnet |
| Rate limiting / quota | system-design → app-security | security-auditor | sonnet |
| Board metrics review | board-review | general-purpose | opus |

### Guardrails
  Prisma schema touched?    → run prisma generate after changes
  Redis touched?            → check TTL logic before merge
  >10 DB queries in a file? → db-expert review

### Completion Gates
  BACKEND:
    □ Migration file written (never raw ALTER)
    □ Prisma types regenerated
    □ Integration tests pass
```
