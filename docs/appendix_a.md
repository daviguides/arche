# Appendix A: On Incident Work - From Reactive to Proactive (and What We Can Automate)

Claude Code doesn’t magically self-orient in production issues.  
Just like any AI workflow, it needs:

- clear instructions (what to look for, what “healthy” means)
- strong context (where to look, how the system is wired)

For each service/project, the docs we provide are critical context:

- cluster name(s)
- namespaces
- services/pods
- known failure modes
- health expectations
- kubectl commands
- log locations and patterns

With that foundation, we can evolve incident workflows gradually.

---

## The missing piece: Yes, we *can* automate - but only the right layer

There **is** space for automation here, but it’s not a silver bullet.

The key nuance is:

- **We can automate detection and data gathering**
- **We can partially automate diagnosis and solution proposals**
- **We cannot automate judgment, prioritization, and side-effect reasoning**

If we automate without the right context, Claude Code becomes “roulette mode”:
it might find the issue by luck, but it won’t be reliable.

This is why committed context is the prerequisite for automation.

### Diagram: “What we automate” vs “What stays human”

```
AUTOMATE                         HUMAN-IN-THE-LOOP
────────                         ─────────────────
- detect anomalies                - define what matters
- gather logs/metrics             - validate causality
- summarize evidence              - evaluate side effects
- propose hypotheses              - decide trade-offs
- propose solutions               - approve execution
```

---

## Why detection is not “free automation”

Detecting incidents is like designing alerts:

You must define:
- which endpoints / signals matter
- what a healthy state looks like
- what “unhealthy” means
- what thresholds or patterns indicate risk

Without these definitions, “automated detection” is just noise.

So detection automation is always:
- explicit
- scoped
- gradually expanded per service

### Diagram: Detection as “Health Contract” + “Signal Mapping”

```
           ┌─────────────────────┐
           │  HEALTH CONTRACT     │
           │  (expected state)    │
           └─────────┬───────────┘
                     |
                     v
┌────────────────────┴────────────────────┐
│ SIGNAL MAPPING (what to observe)         │
│ - endpoints                              │
│ - metrics                                │
│ - logs                                   │
│ - probes                                 │
└────────────────────┬────────────────────┘
                     |
                     v
            ┌─────────────────┐
            │ DETECTION RULES  │
            │ thresholds/patterns
            └─────────────────┘
```

---

## A maturity ladder for AI-assisted incident work

Think of incident work evolving in stages.

### Stage 0 - Manual reactive
- humans notice an issue
- humans dig through logs
- humans guess next steps

### Stage 1 - Automated detection (proactive scanning)
- scripts/cron/health checks/alerts detect anomalies
- a ticket/notification is created
- “something is off” is identified earlier

### Stage 2 - Automated triage & data gathering
Claude Code can do the repetitive part:
- open the right runbooks
- identify which cluster/namespace/service to inspect
- run the right commands (kubectl/log queries)
- collect evidence and summarize it

But only if the repo contains the service context.

#### Diagram: Triage & Gather (what Claude can do automatically)

```
Incident detected
      |
      v
Claude Code reads:
- cluster-map.md
- debug-runbook.md
      |
      v
Runs commands:
- kubectl get pods
- kubectl logs ...
- describe ...
      |
      v
Outputs:
- evidence bundle
- short summary
- next questions (if info missing)
```

### Stage 3 - Automated diagnosis (candidate root cause)
Claude Code proposes:
- likely root cause hypotheses
- supporting evidence
- what additional data is needed to confirm

Human still leads:
- validating assumptions
- checking blind spots
- confirming causality (not correlation)

### Stage 4 - Automated prognosis & solution proposals
Claude Code proposes:
- solution options
- trade-offs and risks
- rollback strategies

Human still leads:
- selecting the best solution
- evaluating side effects
- confirming correctness and performance

### Stage 5 - Execution automation (after approval)
Once the decision is made and the plan is bounded:
- Claude Code can implement changes
- create PRs
- update docs/runbooks

---

## Diagram: Incident Handling Evolution (with automation boundaries)

```
                 (automation-heavy)                       (human-heavy)
┌───────────┐     ┌──────────────────┐     ┌──────────────┐     ┌──────────────────────┐
│ Detection │ --> │ Triage + Gather   │ --> │ Diagnosis     │ --> │ Prognosis + Solutions │
└───────────┘     └──────────────────┘     └──────────────┘     └──────────────────────┘
       |                    |                      |                      |
       v                    v                      v                      v
  alerts/cron         commands + logs        root cause candidates     options + trade-offs
       |                    |                      |                      |
       └──────────────────────────────────────────────────────────────────┘
                              Human Review + Decision (always)
```

---

## Where context fits (and why it replaces “RAG” here)

Instead of building a separate RAG system, we commit context with the code.

The repo becomes the “memory”:
- runbooks
- cluster maps
- command snippets
- known pitfalls

Claude Code can scan these files directly.

But the rule is simple:
> No context in repo → no reliable automation.

### Diagram: “Roulette Mode” vs “Oriented Mode”

```
NO SERVICE CONTEXT IN REPO                    SERVICE CONTEXT IN REPO
───────────────────────────                  ──────────────────────────
Claude Code: "I'll try..."                    Claude Code: "I know where to look."

   (guess)                                         (map)
     |                                               |
     v                                               v
 random commands / random logs                   runbook -> cluster -> namespace -> pod
     |                                               |
     v                                               v
 maybe finds something                           consistent evidence + summary
     |
     v
 brittle outcome
```

Example:
- If a service has no docs (cluster, namespaces, commands), Claude might still “try”
  but success becomes luck (roulette mode).
- If the docs exist, Claude can orient quickly and operate with speed.

### Diagram: The “Service Context Pack” (what every service should have)

```
repo/
  services/
    serice-a/
      docs/
        culster-health/
            INDEX.md
            cluster-map.md
            debug-runbook.md
            known-failure-modes.md
            commands.md
            health-contract.md

Where:
- cluster-map = where it runs
- runbook = how to debug
- health-contract = what “healthy” means
```

---

## The cumulative acceleration principle

There is no silver bullet:
- each service has unique failure modes
- side effects matter
- the system will not think beyond prompt + context

So the real acceleration is cumulative:

> Every incident fixed should leave behind context that makes the next incident faster.

Practical habit:
When you fix an incident, immediately ask:
- “What context was missing that made this hard?”
- “What should we document so next time Claude can self-orient?”
- “What should become a reusable runbook snippet?”

That’s how reactive becomes proactive, and manual becomes scalable.

### Diagram: The feedback loop (how every incident increases future automation)

```
      ┌───────────────────────┐
      │   INCIDENT HAPPENS     │
      └───────────┬───────────┘
                  |
                  v
      ┌───────────────────────┐
      │   FIX + LEARNINGS      │
      └───────────┬───────────┘
                  |
                  v
      ┌───────────────────────┐
      │   COMMIT CONTEXT       │
      │  (runbook / cluster /  │
      │   known failure mode)  │
      └───────────┬───────────┘
                  |
                  v
      ┌───────────────────────┐
      │  NEXT INCIDENT FASTER  │
      │  (more automation-safe)│
      └───────────┬───────────┘
                  |
                  └───────(loop)───────────>
```
