# iPhone Duo Skills

![iPhone Duo, partially folded, showing the inner display with the dock and controls running vertically down the right side](https://raw.githubusercontent.com/mirzaaghazadeh/iphone-duo-skills/main/assets/iphone-duo-hero.webp)

<sup>Image © Apple Inc., from the [iPhone Duo developer page](https://developer.apple.com/iphone-duo/), used for identification. Not affiliated with or endorsed by Apple.</sup>

Agent skills for building iOS apps on **iPhone Duo** — Apple's first foldable
iPhone, announced September 9, 2026.

Apple's developer material for iPhone Duo is six Tech Talk videos plus the
[Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
HIG page. Xcode 27.1 and the *Preparing your app for iPhone Duo* article are still
listed as coming. These skills distill what exists into structured guidance an
agent can act on, plus reference sheets for device facts and the full API surface.

## Install

```bash
npx skills add mirzaaghazadeh/iphone-duo-skills
```

Installs all nine. The CLI detects your agent — Claude Code, Cursor, Copilot,
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

| Skill | Works with | Use it when |
|---|---|---|
| **iphone-duo-readiness** | SwiftUI · UIKit | Entry point. Auditing or porting an existing app — SDK tiers, fixed-assumption hunting, safe areas, routing to the rest. |
| **iphone-duo-adaptive-layout** | SwiftUI · UIKit | Content lands in the fold. Reserved regions, division vs occlusion, displacement patterns, `ArrangementView`. |
| **iphone-duo-vertical-bars** | SwiftUI · UIKit | Toolbars and tab bars. The vertical axis, symbol vs text, `AxisBehavior`, overflow and visibility priority. |
| **iphone-duo-hinge-and-scenes** | SwiftUI · UIKit | Hinge-driven effects, Split View, multiple scenes, dual-display UI via scene accessories. |
| **iphone-duo-camera** | AVFoundation · AVKit | Capture apps. Virtual front camera vs individual cameras, direction coordinator, mirroring, preview. |
| **iphone-duo-design-review** | Any framework | Design critique rather than code — poses, side controls, asymmetry, fold avoidance, sheets. |
| **iphone-duo-games** | Unity · Unreal · Godot · SpriteKit · Metal | The project is a game. Filling the screen across poses, aspect ratio vs letterboxing, touch controls clear of the fold. |
| **iphone-duo-flutter** | Flutter · Dart | The app is Flutter. What `MediaQuery` gives you, why `displayFeatures` doesn't work here, bridging via platform channels. |
| **iphone-duo-react-native** | React Native · Expo | The app is React Native. Asymmetric insets, resize handling, bridging via a native module. |

### Which skills apply to your stack

**Native iOS — SwiftUI or UIKit.** Start with `iphone-duo-readiness`, which routes
you to the rest. The five Swift-focused skills name real iOS 27.1 APIs you can
call directly; `iphone-duo-design-review` applies whatever you build in.

**Flutter.** Read `iphone-duo-flutter` first, then `iphone-duo-design-review` —
the design guidance is framework-neutral and applies unchanged. Skim
`iphone-duo-adaptive-layout` for the *reasoning* behind reserved regions and
displacement; the concepts transfer even though the code doesn't.

**React Native or Expo.** Same shape: `iphone-duo-react-native`, then
`iphone-duo-design-review`, then `iphone-duo-adaptive-layout` for background.

**Any framework, if you capture photo or video.** `iphone-duo-camera` matters
regardless of stack, because the two front cameras and the "which way is this
camera facing" problem are AVFoundation-level facts. Cross-platform apps hit them
through whatever camera plugin they use, or through their own bridge.

**Games — Unity, Unreal, Godot, SpriteKit, Metal.** Read `iphone-duo-games`. Games
sidestep most of the UI guidance but not resizing, and the fold is a genuine
hazard for on-screen touch controls.

**Kotlin Multiplatform, .NET MAUI, Capacitor and friends.** No dedicated skill,
but the pattern from the Flutter and React Native skills carries over directly:
everything is either *resize and safe-area handling you can do in your existing
layer*, or *a native bridge to the iOS 27.1 APIs*. Read whichever cross-platform
skill is closer to your setup, plus `iphone-duo-design-review`.

> **Cross-platform reality check.** Neither Flutter nor React Native supports
> iPhone Duo yet. Flutter's `MediaQuery.displayFeatures` is documented as
> populated **only on Android**, so it returns an empty list here; React Native has
> no fold API at all. Both skills split what works today from what needs a native
> bridge, so you don't lose an afternoon hunting for an API that isn't there.

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

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/layout-model-dark.svg">
  <img alt="Three device states — closed on the 5.4-inch outer display (compact by regular, bars move to the side), partially folded with a division region down the centre of the inner display (regular by regular, keep touch targets out of the curve), and open flat on the 7.6-inch inner display (regular by regular, room for a split view). Below, the chain: pose, available space, size class, what the system moves." src="assets/layout-model.svg" width="900">
</picture>

<sup>Diagram by this project. The underlying behavior is documented across Apple's
[iPhone Duo Tech Talks](https://developer.apple.com/iphone-duo/) and
[Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo);
see [`reference/sources.md`](reference/sources.md).</sup>

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

Every technical claim traces to Apple's Tech Talks, the *Designing for iPhone Duo*
HIG page, or the Newsroom announcement. Nothing is invented — but most of these
APIs were announced while Xcode 27.1 was still rolling out, so treat the names as
the *shape* of the API and confirm exact signatures against the SDK headers before
relying on a build.

A handful of toolbar API names are now confirmed by the published HIG;
`reference/api-index.md` marks which ones.

`scripts/fetch-transcripts.py` re-fetches the Tech Talk transcripts from the
WebVTT subtitle track in each video's HLS manifest, which is how this repo was
researched. Re-run it when Xcode 27.1 ships and the pending documentation lands.

## License

MIT — see [LICENSE](LICENSE).

Not affiliated with or endorsed by Apple. "iPhone" and "iPhone Duo" are
trademarks of Apple Inc.
