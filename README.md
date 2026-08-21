# parcelLab Returns Portal: Engineering Manager Challenge

## The situation

You have joined parcelLab as Engineering Manager for the returns team. The team owns
customer-facing portals where shoppers find an order, check which items are eligible for
return, and submit a request.

The portal is live but incomplete. Backend work is unfinished, tests are failing, and
part of the return flow is broken. You have a small team and need to decide what to
prioritize.

The challenge has three parts. Complete them in order and manage your time across them.

> **Time limit: 4 hours total.** Stop when the time is up and submit your current work.
> A well-reasoned partial solution is preferable to a rushed complete one. Suggested
> split: Part 1 ≈ 90 min · Part 2 ≈ 30 min · Part 3 ≈ 60 min · write-ups ≈ 15 min.

> Please do not fork or publish this repository. Work locally and submit as a private
> repo share or a zip file.

You may use AI tools. If you do, keep a brief record in `AI_LOG.md` of how you used
them.

## Getting started

**Stack:** Python 3.13+, Django, DRF, pytest, ruff, mypy (strict). PyYAML is available.

```bash
uv sync

pytest              # you'll see some failures — that's intentional
python manage.py runserver
```

Open <http://localhost:8000/returns/> and try order `RMA-1001` with email
`alex@example.com` or zip `10115`.

### Project layout

```
portal/
  data/orders_raw.json      # raw order payloads from upstream
  services/mapper.py        # maps raw payload → domain model (incomplete)
  services/eligibility.py   # return eligibility evaluator (stubbed on main)
  templates/returns/*       # Django + HTMX UI
  tests/*                   # pytest suite (some tests intentionally failing)
```

## Your team

- **Thomas:** senior engineer, 6 years at parcelLab, with deep domain knowledge. Thomas
  started a four-week sabbatical on Friday and is unreachable.
- **Andrej:** senior engineer, joined 8 months ago, with strong backend and
  infrastructure experience. Andrej spends half his time with the carrier integrations
  team.
- **Julia:** mid-level engineer, joined 1.5 years ago. Julia is reliable, eager to grow,
  and has not yet led a project alone.

---

## Part 1 · Ship something (~90 min)

Choose one item from the backlog below and implement it. Select the work where your
direct contribution is most useful. In `DECISIONS.md`, explain your choice, why you did
not choose the other items, and how you would assign the remaining work.

> BR-002 is not an option. Thomas implemented it before leaving; you will review that
> work in Part 2.

### BR-001 · Complete the mapper gaps

The mapper does not populate several item-level fields required by the eligibility
engine.

Missing fields on each article: `is_digital`, `is_final_sale`, `category`.

Look at `orders_raw.json` and the test fixtures to understand the different payload
shapes you need to handle.

### BR-003 · Fix and extend the test suite

Several tests are failing. Some depend on BR-001 or BR-002; others may have separate
causes. Fix the suite and add any tests needed to cover your changes.

### BR-004 · Category-specific return windows

Add configurable return windows by category, such as 14 days for electronics and 30 days
for apparel. Use the order-level window when a category has no specific setting.

### SEC-001 · Security audit

A security researcher claims that the portal allows unauthorized access to customer
order data (see Part 3). Audit the codebase, identify the issue, write a test that
demonstrates it, and fix it.

### FR-001 · Show returnable items only

Add a "Show returnable only" toggle to the articles list using HTMX, without a full page
reload.

### FR-002 · Fix the return submission flow

The "Continue" button on the articles page does nothing. Implement the missing flow:
article selection → confirmation → success.

---

## Part 2 · Review Thomas's PR (~30 min)

Before leaving, Thomas pushed the return eligibility engine (BR-002) on branch
**`feature/BR-002-eligibility-engine`** with this note:

> _"Eligibility engine done, all eligibility tests green. Built it config-driven so
> enterprise customers can get custom rules without code changes. Fine to merge without
> me. — T"_

The PR is also available on GitHub:
<https://github.com/parcellab-dev-bot/em-challenge/pulls>

Review the branch and record the result in `REVIEW.md`:

- List your findings and distinguish merge blockers from non-blocking feedback.
- Choose a merge decision: merge, merge with follow-ups, or request changes. State what
  should happen to the branch while Thomas is away.
- Address the review to Thomas, who will read it on return. Use an appropriate tone for
  an experienced engineer with longstanding ownership of the codebase.

```bash
git diff em-challenge...feature/BR-002-eligibility-engine   # the full change
git log em-challenge..feature/BR-002-eligibility-engine     # Thomas's commits
```

> **Optional:** To review inline, push both branches to your own repository and open a
> PR there. Submit either `REVIEW.md` or a link to that PR.

---

## Part 3 · Monday morning memo (~60 min)

At 9:00 on your first Monday, you receive these messages:

**From: mailer@relay-anon.net — Subject: Vulnerability in your returns portal**

> I have identified a vulnerability in your returns portal that allows access to any
> customer's order data — names, home addresses, emails, purchase history. Works today,
> on production. I am giving you the chance to fix this before it becomes public. My fee
> for the full technical details is €15,000. You have two weeks. Payment instructions
> follow on confirmation.

**From: Dani (VP Sales) — Subject: NordThreads demo — 2 weeks!!**

> Team — huge news, NordThreads (potentially our biggest returns customer ever) agreed
> to a live demo in two weeks. They specifically want to see a customer completing a
> return end-to-end in the portal. I told them no problem 🙂
>
> Also — they asked whether their team could configure their own return rules per
> market themselves (they run 14 country organizations with different return
> policies). I said that's basically what our platform does 🙂 Can you confirm both?

Available engineering capacity is Andrej at 50%, Julia at 100%, and you. Thomas is
unreachable. Write `PLAN.md` containing:

1. A two-week plan covering priorities, sequence, ownership (including your work),
   excluded work, and accepted risks. Limit this to one page.
2. **Beyond the demo:** NordThreads' rules question is a product decision, not a
   scheduling one. In 5–10 lines: what should the rules capability become, what would
   you commit to now, and what would you refuse to build even for our biggest
   customer? Take a position; don't list options.
3. A reply to Dani. She is non-technical and has already committed to the demo. Decide
   what she needs to know, whether to mention the security report, and how you answer
   the rules question she has already half-promised.

A reply to the researcher is optional. If included, limit it to 2–3 sentences on how the
company should handle the report.

---

## What to submit

- Your Part 1 implementation: working, type-safe code in small, readable commits
- `REVIEW.md`: your review of Thomas's PR
- `PLAN.md`: the two-week plan, your position on the rules capability, and the reply
  to Dani
- `DECISIONS.md`: your choice, delegation decisions, and rationale
- `AI_LOG.md`: your AI tool record, if applicable, and a short answer to this question:
  What review standard would you apply to AI-generated code on your team?

---

© parcelLab
