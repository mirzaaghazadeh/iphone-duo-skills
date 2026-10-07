---
name: iphone-duo-readiness
description: Audit and port an iOS app to iPhone Duo, Apple's first foldable iPhone. Use when asked to support, adapt, prepare, test, or review an app for iPhone Duo, foldable iPhone, the inner/outer display, device poses, or the fold. Entry point that routes to the layout, bars, hinge/scenes, camera, and design skills.
---

# Get an iOS app ready for iPhone Duo

iPhone Duo is Apple's first foldable iPhone: a 5.4-inch outer display and a
7.6-inch inner display sharing one aspect ratio, joined by a hinge the user can
leave at any angle. An existing iPhone app runs on it unchanged — but it will
look like an app that has not been thought about.

This skill is the entry point. Work the checklist, then hand off to the
specialist skill for whatever the app actually does.

## The one idea to hold onto

**iPhone Duo is not a new idiom. It is a wider continuum of sizes.**

Every mistake in this port comes from an app asserting something fixed: this
idiom, this orientation, this screen, this width, this symmetric inset. Every
fix is the same shape — replace the assertion with a question about the space
actually available right now.

If you find yourself writing a branch that means "if iPhone Duo", stop. Write a
branch on size class or available space instead, and it will be right on iPad,
in Split View, under iPhone mirroring, and on whatever ships next.

## Step 1 — Establish the baseline

Find out what the app is building against, because the SDK is the gate:

| Built against | Behavior on iPhone Duo |
|---|---|
| iOS 26 SDK or earlier | Runs, but doesn't adapt. Open, the app sits **centered with empty space around it**. Closed, content shows to the left of the status bar and camera. |
| iOS 27 SDK | Resizes to fill most of the inner display, but still avoids the status bar on the right edge. |
| **iOS 27.1 SDK or later** | Extends to the full display, with toolbars and tab bars vertical below the status bar. Unlocks the reserved-region and arrangement APIs. |

Check the deployment target and the SDK in the project, then say plainly which
tier the app is in. Getting to the 27.1 tier is the single highest-leverage
change; almost everything else in this skill assumes it.

One caution before you ship at the 27.1 tier: that's the point where the bars go
vertical, so confirm the content adapts to that before releasing. Jumping tiers
without checking is how an app ends up with controls overlapping its own layout.

### Let the tooling do the first pass

Xcode ships an **App Resizability** skill (renamed from the app modernization
skill; it now covers SwiftUI and iPhone Duo). In Xcode, ask the coding assistant
to *get my app ready for iPhone Duo* and it scans for the patterns in Step 2,
explaining each and proposing a fix.

Not using Xcode's assistant? Export the skill and use it in another agent:

```bash
xcrun agent skills export
```

It catches most issues but not all, so still work Step 2 by hand afterwards.

### Then look at it running

Three tools, in increasing fidelity:

- **The iOS resizable simulator** in Device Hub — fastest way to find layouts
  that break under arbitrary sizes.
- **iPhone Mirroring on macOS 27** — resize the window to extremes in both
  directions. Good for catching cached-size bugs.
- **The iPhone Duo simulator in Xcode 27.1** — the only one that gives you the
  real thing. Drive open, close, rotate and fold, and try Split View by dragging
  the app to one side with the home indicator.

Bugs here are visual and pose-dependent. You will not find them by reading code.

## Step 2 — Hunt the fixed assumptions

Grep the codebase for these. Each one is a real defect on this device:

**Orientation branches.** Grep for `UIDevice.current.orientation`,
`statusBarOrientation`, and `interfaceOrientation` — including
`windowScene.effectiveGeometry.interfaceOrientation`. The inner display *does
not honor supported interface orientations*, and orientation no longer tells you
what shape your app is. To learn whether you're wider than tall, compare width
and height of the space you actually have: `view.bounds` in a view controller,
`superview.bounds` in a view, or the `GeometryReader` size in SwiftUI.

**`UIScreen.main`.** Ambiguous on a two-display device and slated for
deprecation. Each use has a specific replacement:

| Instead of | Use |
|---|---|
| `UIScreen.main.bounds` | `view.bounds` / `window.bounds`; `GeometryReader` or `onGeometryChange` in SwiftUI |
| `UIScreen.main.scale` | `traitCollection.displayScale`, or `@Environment(\.displayScale)` |
| `UIWindow(frame: UIScreen.main.bounds)` | `UIWindow(windowScene:)` |
| A stored `UIScreen` | `view.window?.windowScene?.screen`, read on demand |

**Size read once, then cached.** This one hides well. Reading size at launch —
or in `viewIsAppearing` — isn't enough, because a fold resizes your app
*mid-session*. Do size-dependent layout in `layoutSubviews` /
`viewDidLayoutSubviews`, and use `viewWillTransition(to:with:)` for work that
must run on the change itself.

**"Regular width means iPad."** The trap most likely to produce a visibly wrong
screen. Plenty of apps show an iPad-only layout when `horizontalSizeClass ==
.regular`, and assume iPhone is always compact. The inner display is regular
width, so that iPad layout now runs on a phone. Check both directions: branches
that fire on regular, and branches that assume compact. Related: delete any
comparison against a specific device size, like `bounds.height == 844` or a table
of known iPhone dimensions — none of them match this device.

**Full-bleed media.** Hero images and video set to `.scaleAspectFill` or
`.aspectRatio(contentMode: .fill)` crop more aggressively on a wider display and
can lose the subject entirely. Choose fill versus fit from the current size class
or aspect ratio, or set a focal point.

**Symmetric inset math.** This is the subtle one. On iPhone Duo the safe area
and layout margins are routinely asymmetric — vertical controls sit on one side
only, and which side depends on the pose and on Split View placement. Any
arithmetic shaped like `bounds.width - safeAreaInsets.left * 2` is wrong.
Inset by the whole set instead and let each edge speak for itself.

**Hardcoded widths and breakpoints.** Fixed point values, device-width tables,
"if width > 390" style thresholds. Target the two size classes: **compact width
on the outer display, regular width on the inner display**.

**Hand-rolled bars.** A custom `UIToolbar`, `UINavigationBar` or `UITabBar` is
invisible to the system's vertical-bar layout. Its content will not participate.

## Step 3 — Adopt the standard containers

The cheapest path to a good port is letting system containers do the adapting.
These are already fully pose-aware:

- `NavigationSplitView` / `UISplitViewController` — columns collapse to a single
  stack when closed, and appear tiled or as overlays when open.
- `TabView` / `UITabBarController` — adapt across every pose, laying out
  vertically where appropriate. On the inner display you can opt into a richer
  sidebar by setting the tab bar's preferred placement to `.sidebar`.
- `NavigationStack`, `List`, `ScrollView` — adapt to reserved regions on their
  own.
- Sheets, alerts, menus, popovers and context menus — reposition themselves
  around the fold automatically.

System components carry **fold avoidance**: they nudge interactive elements out
of the curved region so buttons never land in the fold. You get that free by
using them, and you owe yourself an implementation of it if you don't.

## Step 4 — Get safe areas right

Four rules, in priority order:

1. Use container-provided bars for anything bar-shaped. They lay out *outside*
   the safe area and dodge the status bar, the Dynamic Island and the camera on
   their own. Horizontal bars contribute top/bottom insets; vertical bars
   contribute leading/trailing insets.
2. Keep interactive and legible foreground content **inside** the safe area.
   SwiftUI does this by default; in UIKit reference `safeAreaInsets` or
   constrain to the safe area layout guide.
3. Let backgrounds bleed **past** it — `.ignoresSafeArea()` in SwiftUI,
   `view.bounds` in UIKit — so artwork runs under bars and sidebars.
4. Handle every edge independently, and test in Split View on both sides.

For custom UI that needs to live outside the safe area without colliding with
system UI, iOS 27.1 adds `ReservedRegion` (SwiftUI) and `UIViewReservedRegion`
(UIKit). Reach for those rather than guessing at insets.

To match the screen's corner radius, use the iOS 26 concentricity APIs —
`ConcentricRectangle` in SwiftUI, `UICornerConfiguration` in UIKit — which were
updated for the shapes on this device.

## Step 5 — Route to the specialist

| If the app… | Use |
|---|---|
| has toolbars, tab bars, or overflow menus | `iphone-duo-vertical-bars` |
| has custom layout, split-like views, or content that lands in the fold | `iphone-duo-adaptive-layout` |
| wants hinge-driven effects, multiple windows, or dual-display UI | `iphone-duo-hinge-and-scenes` |
| captures photo or video | `iphone-duo-camera` |
| needs to decide what goes in each pane, size assets, or build a two-pane paywall / onboarding | `iphone-duo-dual-pane-patterns` |
| needs a design pass rather than a code pass | `iphone-duo-design-review` |

Device numbers live in `../../reference/device-facts.md`; every API name and its
framework is in `../../reference/api-index.md`.

## Step 6 — Shipping it

Adapting the app is most of the job, but the App Store side is easy to forget and
cheap to do:

- **Screenshots and previews.** Capture the app across orientations and poses so
  the product page shows it actually working on the device, not a phone layout
  stretched wide. Check the current screenshot specifications for the required
  sizes.
- **Preview before you publish.** App Store Connect has a preview tool for
  checking how your assets render on iPhone Duo. Worth using — an asset that
  looks right in Xcode can still read badly on the product page.
- **Featuring nomination.** App Store Connect lets you submit one, and in the
  Helpful Details section you can state that the app is optimized for iPhone Duo,
  including support for all device poses. Being early matters here: there won't be
  many optimized apps at launch, which is exactly when editorial is looking.

## Reporting back

Give the user the tier they're on, the concrete defects found with
`file:line`, and what changes tier. Be honest about what needs a running
simulator to confirm — pose-dependent layout bugs are not statically decidable,
and claiming otherwise wastes their time.

## Accuracy note

Signatures in this repo were verified against Apple's published API reference on
25 September 2026, so they are no longer guesses from the Tech Talk sessions.
Three claims were wrong and got corrected in that pass — see the ⚠ markers in
`../../reference/api-index.md`.

Apple's *Prepare* checklist has since been published and is folded in here too,
so the written guidance is now complete rather than inferred from the videos.

One caveat remains, and it matters: nothing here has been compiled or run against
a real device. Pose-dependent layout behaviour in particular needs the simulator
to confirm, so don't report it as verified on the strength of documentation
alone.
