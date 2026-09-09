# iPhone Duo Skills

Agent skills for building iOS apps on **iPhone Duo** — Apple's first foldable
iPhone, announced September 9, 2026.

Apple's developer material for iPhone Duo currently lives in six Tech Talk
videos; the written documentation and HIG pages were still marked "coming soon"
at the time this was written. These skills distill that material into structured
guidance an agent can act on, plus reference sheets for device facts and the full
API surface.

## Install

```bash
npx skills add mirzaaghazadeh/iphone-duo-skills
```

Installs all six. The CLI detects your agent — Claude Code, Cursor, Copilot,
Gemini and others — and puts them where that agent looks.

Useful flags:

```bash
# just one skill
npx skills add mirzaaghazadeh/iphone-duo-skills --skill iphone-duo-readiness

# user-level instead of project-level
npx skills add mirzaaghazadeh/iphone-duo-skills --global

# see what's in here without installing
npx skills add mirzaaghazadeh/iphone-duo-skills --list
```

To try a skill without installing it at all:

```bash
npx skills use mirzaaghazadeh/iphone-duo-skills@iphone-duo-readiness
```

<details>
<summary>Manual install</summary>

```bash
git clone https://github.com/mirzaaghazadeh/iphone-duo-skills.git
cp -r iphone-duo-skills/skills/* ~/.claude/skills/
```

Or project-level, into `.claude/skills/` in a repo.

</details>

Each skill is a self-contained `SKILL.md` with YAML frontmatter, so it also works
anywhere that reads plain Markdown instructions. Restart the session and the
skills appear; invoke one by name or just describe the task.

## The skills

| Skill | Use it when |
|---|---|
| **iphone-duo-readiness** | Entry point. Auditing or porting an existing app — SDK tiers, fixed-assumption hunting, safe areas, routing to the rest. |
| **iphone-duo-adaptive-layout** | Content lands in the fold. Reserved regions, division vs occlusion, displacement patterns, `ArrangementView`. |
| **iphone-duo-vertical-bars** | Toolbars and tab bars. The vertical axis, symbol vs text, `AxisBehavior`, overflow and visibility priority. |
| **iphone-duo-hinge-and-scenes** | Hinge-driven effects, Split View, multiple scenes, dual-display UI via scene accessories. |
| **iphone-duo-camera** | Capture apps. Virtual front camera vs individual cameras, direction coordinator, mirroring, preview. |
| **iphone-duo-design-review** | Design critique rather than code — poses, side controls, asymmetry, fold avoidance, sheets. |

## Reference

- [`reference/device-facts.md`](reference/device-facts.md) — displays, silicon,
  cameras, poses, and the size-class table
- [`reference/api-index.md`](reference/api-index.md) — every announced API by
  job, with framework and minimum SDK
- [`reference/sources.md`](reference/sources.md) — every source, linked

## What actually matters on this device

If you read nothing else:

**iPhone Duo is not a new idiom — it's a wider continuum of sizes.** Every bug in
a foldable port comes from an app asserting something fixed (this idiom, this
orientation, this screen, this width, this symmetric inset), and every fix
replaces that assertion with a question about the space available right now.

Three concrete consequences:

1. **The inner display ignores your supported interface orientations.** Branch on
   size class, never on orientation or idiom.
2. **`UIScreen.main` is ambiguous here** and slated for deprecation. Use the
   environment, the trait collection, or the scene's bounds.
3. **Safe areas are asymmetric.** Any math shaped like
   `width - safeAreaInsets.left * 2` is a defect.

And the highest-leverage single change: **build against the iOS 27.1 SDK.**
It's the gate for edge-to-edge content, vertical bars, reserved regions and
arrangements.

## Accuracy

Every technical claim traces to Apple's Tech Talks or Newsroom announcement.
Nothing is invented — but these APIs were announced while Xcode 27.1 was still
rolling out, so treat the names as the *shape* of the API and confirm exact
signatures against the SDK headers before relying on a build.

`scripts/fetch-transcripts.py` re-fetches the Tech Talk transcripts from the
WebVTT subtitle track in each video's HLS manifest, which is how this repo was
researched. Re-run it when Xcode 27.1 ships and the pending documentation lands.

## License

MIT — see [LICENSE](LICENSE).

Not affiliated with or endorsed by Apple. "iPhone" and "iPhone Duo" are
trademarks of Apple Inc.
