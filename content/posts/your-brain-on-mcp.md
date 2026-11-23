---
title: "Your Brain on MCP: Who's Ready for Total Freedom?"
slug: your-brain-on-mcp
date: 2026-11-23
description: "AI agents and MCP are freeing intelligence analysts from clumsy interfaces. But the structure those screens quietly provided doesn't vanish. It moves onto the analyst, and what happens next is an open question."
---
Picture an analyst at two in the morning. A crisis broke six hours ago, and the fight over what it means began minutes later. Several narrative campaigns are now maneuvering for the same ground: One probing for a weak flank in allied opinion, another laying down cover for a move that hasn't happened yet, a third trying to pin a government in place until the window to respond has closed. His commander wants a picture of that battlespace by dawn: Who is advancing, where, with what forces, and in support of which moves on the ground. He has the data. What he doesn't have is a screen that will show it the way tonight's question demands. The filters were built for a different mission. The map won't overlay what he needs. The export takes four clicks and a prayer. So he does what analysts have always done: Pulls everything into a spreadsheet and builds the answer by hand.

Anyone who has worked with intelligence software knows that scene. Many of these interfaces are aesthetically unpleasant and organizationally clumsy. Often, they work against the people using them, because what those people need changes with every mission, every controversy, every crisis.

## A compromise from the start

This isn't because the people who design these systems are careless. An interface is a bet about which questions its users will ask. In intelligence work, the questions never hold still. A screen built for last year's problem is, by definition, a little wrong for this year's. Application designers tend to see themselves as building interfaces that bend to the needs of the analyst, when in reality it's usually the analysts who bend themselves to the constraints of the interface.

But two things were true about that arrangement. First, the struggle was shared. Thousands of analysts fighting the same handful of interfaces learned the same workarounds and could teach them to each other. Second, the tool, for all its faults, carried a workflow. Somebody decided which fields mattered, which steps came first, which view opened by default. Clumsy as they can be, interfaces have helped forge a kind of institutional memory.

## The promise

Now the interface is dissolving. The Model Context Protocol, or MCP, is an open standard, introduced in late 2024, that gives AI assistants a common way to connect to outside systems: Databases, applications, document stores. Think of it as a universal adapter: Build one connector to a system, and any compatible assistant can use it. Through MCP and AI agents, an assistant can reach directly into the systems that hold the data. The analyst asks in plain language and gets an answer, a table, or a chart, without touching the UI at all.

For the analyst at two in the morning, this is a real gift. The software finally bends to the question instead of the other way around.

## The shifting burden

The work the interface did doesn't vanish, though. It moves, and it moves onto the analyst.

We've lived a version of this at EdgeTheory. A couple of years ago, when AI tools became sophisticated enough to deliver real productivity leverage, we expected the hard part to be handing them work we had always done by hand. Instead, the hard part was realizing, early enough in the workflow, that this was a moment to invoke the tool in the first place. Habit is powerful. More than once, someone finished a task the old way and only afterward thought: I could have asked the assistant to do that. The tools were ready well before our instincts were.

But we're beyond that, and so is the intelligence analyst community. Reaching for the tool at the right time has largely become second nature. Using it well is another matter, and that burden now falls on the individual analyst. He has to frame the question precisely enough for a machine to act on it. He has to prompt, then supervise: Did the assistant search what he thinks it searched, over the period he meant, in the sources he trusts? He has to judge whether the chart it drew is honest or merely handsome. The old interface handled pieces of each of these, sometimes badly but almost always at least consistently. Now none of them is handled unless he handles it.

Underneath all of it sits a new kind of uncertainty, one the old screens largely spared him. A fixed interface told him, in effect, which questions could be asked. Now every question can be asked, and he is left to wonder. Am I asking the right questions? Am I requesting the right data? Am I framing the goals of the assessment correctly? Have I told the assistant enough about how to visualize the results, and how to convey what they mean? No error message will tell him he got any of these wrong. The answer comes back fluent and confident either way.

Instead of many users fighting the challenges of a handful of interfaces, each user now works with his own strengths and shortcomings. The result is that, just as there has been a shift of the work burden from interface to user, there's also been a similar shift of limitations: It's now far less one that's *imposed* by the application, and more one that's *exposed* by the user.

Intelligence analysis is a curious hybrid of standardized tradecraft and individual judgment. On one side sit the disciplines the profession has spent decades codifying: Sourcing standards, structured analytic techniques, calibrated confidence language, the habit of separating what is known from what is assessed. On the other sits something no manual fully captures: The analyst's instinct for which detail matters, which pattern is real, which silence means something. The best analysis has always needed both. The old interfaces, for all their faults, lent structural support to the standardized half; they enforced a little of the tradecraft whether the analyst wanted it or not. Agents lean the other way. They give the individual half more room than it has ever had, along with everything that comes with it: The intuition and the blind spots, the creativity and the biases, the hard-won expertise and the unexamined habits.

## Two futures

Where this leads isn't settled, and I want to resist the reflex, common in my business, to assume the worst. It's entirely possible that freedom from the screen opens a new age of intelligence analysis. Freed from interfaces that dictated what could be asked, a gifted analyst can follow a hunch across sources no product manager anticipated, test three framings of a problem before breakfast, and see it in a shape no dashboard was ever built to show. Multiply that across a workforce, and the quality of insight could rise sharply.

It's also possible that we build a Tower of Babel. Thousands of analysts, each working through an assistant in his own way, may produce not one picture of the battlespace but a fly's eye of a million facets. Each facet reflects its analyst's strengths, weaknesses, and biases: What data he knew to ask for, how he framed the assessment, how he chose to visualize and convey it. Each may be sharp on its own. Together they may not add up to anything a commander can act on. The facets can go wrong in familiar ways:

- **The vague question.** "What's going on with Iran?" returns something fluent, plausible, and useless.
- **The unchecked answer.** Assistants are confident and supervision is tedious. Under deadline, it can get skipped.
- **The private method.** Two analysts ask the same data the same question in different ways, get different answers, and neither may know the other exists.
- **The missing trail.** A fixed workflow leaves a record of what was done. A conversation is much harder to audit.

Both futures are plausible, and they may well arrive at the same time, in the same organization. Which one dominates will depend less on the models than on whether the structure analysts used to get from their screens shows up somewhere else.

And if the second future does arrive, if a meaningful share of analysts struggle to supply the structure their screens used to supply for them, what then? Who notices, and who fixes it? Their supervisors may be the first to see the symptoms: Assessments that don't line up, methods no one can reconstruct, confidence that outruns the evidence. The customers of that analysis, the commanders, policymakers, and executives who act on it, may notice next, and usually at a worse moment. Training programs, oversight offices, and the vendors who build the tools all have a stake as well, and each could respond differently: Retraining, new review requirements, stricter standards for what a tool must do before it's bought. The open question isn't whether the problem gets addressed. It's whether the remedy arrives by design, before the failures, or by reaction, after them.

## What the old screens got right by accident

Here is the irony. Some of what we hated about the old interfaces was doing us a favor. Required fields forced an analyst to name a source. Fixed workflows put collection before conclusion. Default views decided what was worth looking at first. Nobody praised these things at the time. But they were tradecraft in disguise: Structure enforced by the tool, so the analyst didn't have to supply it from scratch every time.

When the interface goes, that structure goes with it, unless someone deliberately puts it somewhere else.

## Build the discipline in

That changes the job for those of us who build these systems. If the screen is optional, the product is no longer what the analyst looks at. It's what the assistant draws on. That layer can carry tradecraft, not to fence in the gifted analyst, but to give every analyst a common floor, so the facets can be compared and combined:

- **Defined metrics with fixed meanings,** so that "trending" and "reliable" mean the same thing to every analyst and every assistant.
- **Structured workflows the assistant follows by default:** Frame the question, scope it, run it, triage the results, then decide.
- **Guardrails about what the data can't show.** A spike of a dozen items is not a surge. Sources sharing the same story is a lead, not proof of coordination.
- **Default questions** that surface what a disciplined analyst would ask, even when this analyst, tonight, doesn't.

And we should train analysts in what prompting really is underneath the jargon: Framing. A well-framed question works on any tool. A prompt trick works on one model for one season.

## Ready for the freedom?

So who's ready for total freedom? Some analysts already are, and they'll do work none of us has imagined yet. Others may find the freedom harder to use than it looks, through no fault of their own: The old screens never asked them to supply the structure themselves. The freedom is real either way. Whether it brings a new age of brilliance and insight, or a Babel of incompatible fragments, depends on one thing: whether discipline, structure, and tradecraft remain the foundation of intelligence work, long after the screens that once enforced them are gone.
