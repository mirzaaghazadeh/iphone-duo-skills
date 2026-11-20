---
name: iphone-duo-flutter
description: Adapt a Flutter app to iPhone Duo, Apple's first foldable iPhone — what MediaQuery gives you today, why displayFeatures does not work here, and how to bridge the iOS 27.1 reserved-region, hinge and arrangement APIs through platform channels. Use when a Flutter or Dart app needs foldable iPhone support.
---

# Flutter on iPhone Duo

Start here, because it is the thing that will waste your afternoon otherwise:

> **`MediaQuery.displayFeatures` is documented as "populated only on Android."**

Flutter's foldable abstraction was built for Android hinges. On iPhone Duo it
returns an **empty list**, no matter how folded the device is. The same goes for
the `dual_screen` package (`TwoPane`, `hingeAngleEvents`) — Android-only in
practice, and last published around three years ago.

So Flutter gives you no fold awareness on this device out of the box. What it
*does* give you is most of what actually matters. Work in two tiers.

## Tier 1 — works today, no native code

This is the bulk of a good port, and it is all pure Dart.

### Resize correctly

iPhone Duo changes your app's size constantly: opening, closing, folding,
rotating, and entering Split View. Flutter handles the mechanics, but only if
your layout is driven by constraints rather than constants.

- Use `LayoutBuilder` and its `BoxConstraints` for layout decisions.
- Use `MediaQuery.sizeOf(context)` when you need the window, not
  `MediaQuery.of(context)` — the `sizeOf`/`paddingOf` accessors rebuild only on
  the property you read, which matters when the size changes this often.
- Never cache a size in `initState` or a field. It will be stale within seconds.

### Handle asymmetric safe areas

This is the one that produces real bugs. On iPhone Duo the system puts its
controls **on one side**, so insets are routinely asymmetric — and which side
depends on the pose and on which half of a Split View you occupy.

`MediaQuery.paddingOf(context)` returns `EdgeInsets` with independent `left`,
`top`, `right`, `bottom`. Use each one. Any expression of the form
`width - padding.left * 2` is a defect on this device.

The `SafeArea` widget handles all four edges independently already, so prefer it
over hand-rolled padding. Where you need artwork to bleed underneath, put the
background outside the `SafeArea` and only the interactive foreground inside it.

### Replace breakpoints with size-class thinking

iOS reasons about this device in size classes: the outer display is **compact
width**, the inner display is **regular width**. Flutter has no size classes, so
map to width breakpoints — the Material 3 window size classes are a reasonable
proxy (compact `< 600`, medium `600–840`, expanded `≥ 840` logical pixels).

Two rules:

- Branch on the **constraints you were handed**, not on `Platform.isIOS`, a
  device model string, or `MediaQuery.orientationOf`. The inner display does not
  honor supported orientations, so orientation is not a reliable signal.
- Pick breakpoints from where *your content* stops working, then sanity-check
  that a compact/regular split falls out of it.

### Prefer adaptive containers

`NavigationRail` for wide layouts and `NavigationBar` for narrow ones is the
Flutter analogue of what iOS does natively when it moves controls to the side.
A rail on the inner display and a bar on the outer display will feel close to
right, and costs one breakpoint.

## Tier 2 — needs a platform channel

Everything genuinely iPhone Duo-specific is unavailable to Dart until you bridge
it. As of this writing no Flutter release has shipped iPhone Duo support, so
plan on writing this yourself, and check whether it has landed before you do.

What is worth bridging, in priority order:

| Native API (iOS 27.1) | Why you'd want it in Dart |
|---|---|
| `reservedRegions(kind:)` on `UIView` | Keep controls out of the fold and out of the under-display camera |
| `UIHingeInteraction` | Continuous hinge angle for effects |
| Size class from `traitCollection` | The real signal iOS uses, rather than your breakpoint guess |

### How to shape the bridge

Use a **`MethodChannel`** for one-shot queries (current reserved regions, current
size class) and an **`EventChannel`** for anything continuous — the hinge angle
is a live stream and will spam a `MethodChannel`.

On the iOS side, in the `Runner` target, register a `FlutterMethodChannel` and a
`FlutterEventChannel` on the `FlutterViewController`, then read the native APIs
from that view. The reserved-region APIs hang off `UIView`, and the
`FlutterViewController`'s view is the right one to query — that is the view your
Dart layout actually occupies.

Serialize regions as plain maps (`{left, top, width, height, kind, active}`) so
Dart gets something it can rebuild `Rect`s from. Send the region list on change
rather than polling.

Guard everything: the hinge is `nil` on every non-folding device, and these APIs
do not exist below iOS 27.1. Your bridge must degrade to "no regions, no hinge"
rather than throw, because the same Flutter binary runs on every iPhone.

### Then use it like Tier 1

Once regions arrive in Dart, feed them into the same constraint-driven layout you
already built. A division region (the fold) tells you where to *not* put
interactive widgets; an occlusion region (the camera) tells you what to avoid
covering. `Stack` with `Positioned`, or a custom `MultiChildLayoutDelegate`, is
usually the cleanest way to displace a specific control around a region.

## What to do, in order

1. Make the app resize cleanly under `LayoutBuilder`. Most bugs die here.
2. Audit every use of `MediaQuery.padding` for symmetric-inset math.
3. Replace orientation and platform checks with constraint-based branching.
4. Add a rail/bar split so the inner display isn't just a stretched phone layout.
5. Only then, if the app genuinely needs fold awareness, write the channel.

Steps 1–4 get a Flutter app most of the way to feeling right on iPhone Duo, and
they improve it on tablets and desktop at the same time. Step 5 is the only part
that is iPhone Duo-specific, and it is the only part that can't be tested without
the Xcode 27.1 simulator.

For what the native APIs actually do and why, read
`../iphone-duo-adaptive-layout/SKILL.md` and
`../iphone-duo-readiness/SKILL.md` — the design reasoning transfers directly even
though the code doesn't.

## What the simulator showed

Everything above is from Apple's documentation. This section is from running a
Flutter 3.50 app in the iPhone Duo simulator (Xcode 27.1, iOS 27.1 runtime,
built against the iOS 27.1 SDK, UIScene lifecycle). The app's iPhone
orientations are portrait only. Treat it as one app's observations, not a
specification, and re-check on your own versions.

### `MediaQuery` sees the side column as a plain right inset

On the outer display `MediaQuery.sizeOf` was 466×678 and both `padding` and
`viewPadding` were `EdgeInsets.fromLTRB(0, 0, 84, 34)`. That 84 pt runs the full
height of the window, but the status bar and camera only fill the top of the
column: below them the column is where iPhone Duo puts bar buttons. An inset is a
rectangle edge, so it can't say where the status area ends. If you draw your own
side controls in that column, you need the native layout guide (below).

On the inner display, `UIView.safeAreaInsets` was also right 84 / bottom 34.

### The island grows, and Flutter is not told

A Live Activity from another app grows the island down the status column. Nothing
Flutter can see changes, and the change happens while your app stays in the
foreground:

| Outer display, folded | No Live Activity | Another app's Live Activity |
|---|---|---|
| `MediaQuery.padding` / `viewPadding` | right 84, bottom 34 | unchanged |
| `UIView.safeAreaInsets` | right 84, bottom 34 | unchanged |
| `reservedRegions(kind: .occlusion)`, status-column region | `{382, 0, 84×170}` | `{382, 0, 84×250}` |
| `layoutGuide(for: .bar(onEdge: .right, extent: 48)).layoutFrame` | `{394, 170, 48×474}` | `{394, 250, 48×394}` |

The camera itself is a separate occlusion region, `{399.7, 29.3, 37×37}`, and
did not move. The guide's bottom (170 + 474 = 644) stops at the home-indicator
inset.

Side controls placed at a fixed `y` end up under the grown island. Bridge the
bar guide, which is the API made for placing a vertical bar, and lay your
controls out inside it.

### Bridging the bar guide

A layout guide has no change callback and `layoutFrame` isn't observable. Pin a
hidden view to the guide with Auto Layout: UIKit moving that view is the signal.
`updateConstraints()` on the view that reads the guide also ran again on every
change in our tests.

```swift
// Runner: register on the implicit engine (UIScene lifecycle).
func didInitializeImplicitFlutterEngine(_ bridge: FlutterImplicitEngineBridge) {
  GeneratedPluginRegistrant.register(with: bridge.pluginRegistry)
  if let r = bridge.pluginRegistry.registrar(forPlugin: "DuoBarGuide") {
    DuoBarGuide.register(with: r)
  }
}

final class DuoBarGuide: NSObject, FlutterStreamHandler {
  private weak var registrar: FlutterPluginRegistrar?
  private var tracker: Tracker?

  static func register(with registrar: FlutterPluginRegistrar) {
    let instance = DuoBarGuide()
    instance.registrar = registrar
    FlutterEventChannel(name: "duo/bar_guide", binaryMessenger: registrar.messenger())
      .setStreamHandler(instance)
    objc_setAssociatedObject(registrar, "duoBarGuide", instance, .OBJC_ASSOCIATION_RETAIN)
  }

  // The view controller exists by the time Dart listens (after the first frame),
  // not when the plugin registers.
  func onListen(withArguments _: Any?, eventSink sink: @escaping FlutterEventSink) -> FlutterError? {
    guard #available(iOS 27.1, *), let host = registrar?.viewController?.view else {
      sink(nil)  // older iOS: no guide, keep your default layout
      return nil
    }
    let guide = host.layoutGuide(for: .bar(onEdge: .right, extent: 48))
    let t = Tracker()
    t.isHidden = true
    t.translatesAutoresizingMaskIntoConstraints = false
    host.addSubview(t)
    NSLayoutConstraint.activate([
      t.leadingAnchor.constraint(equalTo: guide.leadingAnchor),
      t.trailingAnchor.constraint(equalTo: guide.trailingAnchor),
      t.topAnchor.constraint(equalTo: guide.topAnchor),
      t.bottomAnchor.constraint(equalTo: guide.bottomAnchor),
    ])
    t.onMove = { f in sink([f.minX, f.minY, f.width, f.height]) }
    tracker = t
    return nil
  }

  func onCancel(withArguments _: Any?) -> FlutterError? {
    tracker?.removeFromSuperview()
    tracker = nil
    return nil
  }
}

private final class Tracker: UIView {
  var onMove: ((CGRect) -> Void)?
  private var last = CGRect.null
  override func layoutSubviews() {
    super.layoutSubviews()
    if frame != last { last = frame; onMove?(frame) }
  }
}
```

Frames arrive in the Flutter view's coordinates, which are the same logical
pixels `MediaQuery` uses. On the Dart side, listen once near the root and expose
the rect to the widget that draws the side controls; treat `null` as "no guide"
and keep the default layout.

Gate the feature on the guide being present rather than on the device model, and
don't read it as a proxy for "this is an iPhone Duo".

### Reproducing island growth in the simulator

- **What worked:** a throwaway SwiftUI app with a Widget Extension whose widget
  is an `ActivityConfiguration`, `NSSupportsLiveActivities` set in the app's
  Info.plist, and `Activity.request(...)` on launch. Start it, then bring your
  own app forward. To watch the change arrive while your app is on screen, have
  the scratch app call `beginBackgroundTask`, wait a few seconds and end its
  activities, and switch to your app in the meantime. Reinstalling the scratch
  app also ends its activities, so don't reinstall mid-test.
- **What didn't:** recording with `AVAudioRecorder` from the app under test (no
  growth, no microphone indicator), and `xcrun simctl status_bar … override`
  (it only changes the glyphs). Device Hub has no switch for Live Activities or
  the Dynamic Island.
- **Not measured:** a real device during a phone call or with the location
  indicator; the partially folded posture.

### Reading the window size outside the widget tree goes stale

A width read straight from the window during `build` — for example a state
manager helper like `Sint.width`, which divides the implicit view's
`physicalSize` by its pixel ratio — doesn't register a dependency. After
unfolding, a screen built while folded kept its 466 pt layout on the 951 pt inner
display (a feed stayed 436 pt wide, pinned to the left) until something else
rebuilt it. `MediaQuery.of(context).size` registers the dependency, but it
rebuilds on every `MediaQueryData` change. Size from the constraints you're given
(`LayoutBuilder`, `double.infinity`, `FractionallySizedBox`), or use
`MediaQuery.sizeOf(context)` when you really need the window. A unit test that
scans `lib/` for these reads keeps them from coming back.

### The inner display stayed landscape

With portrait-only iPhone orientations, the inner display showed the app at
951×669, landscape, in all four device orientations set with
`xcrun devicectl device orientation set`. Plan the regular-width layout as
landscape, and pick two-pane breakpoints from your panes' minimum widths rather
than from 600 pt, so a narrower window (Split View, a small tablet) gets one pane.

### Simulator tooling that saved time

- In Xcode 27, Simulator is **Device Hub**: `open -a "Device Hub"`. Fold and
  unfold with its posture buttons; there is no `simctl` or `devicectl` command
  for the posture.
- Name the display when you take a screenshot. With no `--display`,
  `xcrun simctl io <udid> screenshot` picked the outer display (`LCD`) in our
  runs even while unfolded. Pass `--display=LCD` (outer) or `--display=LCD-1`
  (inner); right after unfolding the inner display can be black for a few
  seconds.
- `xcrun devicectl device info displays --device <udid>` shows which display is
  active.
- While unfolded, Xcode's device-interaction taps still went to the outer
  display, which is off. Interact while folded, or through Device Hub.
