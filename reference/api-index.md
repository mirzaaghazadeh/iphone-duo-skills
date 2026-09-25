# iPhone Duo — API index

Every API named across Apple's six iPhone Duo Tech Talks, grouped by job, with
the framework and the minimum SDK. Use this as a lookup table; the skills in
`../skills/` explain when and why to reach for each one.

> **Verified against the published API reference on 25 September 2026.**
> Apple's developer documentation for these symbols is now live, so the
> signatures below are taken from it rather than from the Tech Talk sessions.
> Three corrections came out of that pass and are marked ⚠ below.
>
> Still missing: the *Preparing your app for iPhone Duo* article is not yet
> published.

## SDK gates

| Built against | What your app gets on iPhone Duo |
|---|---|
| Pre-iOS 27 | Runs fine. Closed: uses the space left of the status bar and camera. Open: familiar size and aspect ratio. |
| iOS 27 SDK | Extends to the left of the status bar area on the inner display. Existing resizing work pays off. |
| **iOS 27.1 SDK** | Full-screen: content reaches the screen edge, and standard navigation/toolbar buttons lay out **vertically** under the status bar. Unlocks reserved regions and arrangements. |

Tooling: **Xcode 27.1** → iPhone Duo simulator in **Device Hub**, with controls
to open, close, rotate and fold. The **App Resizability** skill in Xcode 27.1
(formerly the app modernization skill) now covers SwiftUI and iPhone Duo.

## Size classes, screens, shape

| Job | SwiftUI | UIKit |
|---|---|---|
| Read size class | `@Environment(\.horizontalSizeClass)`, `@Environment(\.verticalSizeClass)` | `traitCollection.horizontalSizeClass` / `.verticalSizeClass` |
| Screen scale | environment / trait | `traitCollection.displayScale` |
| Get a screen at all | prefer not to | `window?.windowScene?.screen` |
| Match screen corners (iOS 26) | `ConcentricRectangle` | `UICornerConfiguration` |

**Avoid `UIScreen.main`.** It is ambiguous on a two-display device and is slated
for deprecation. Prefer environment values, trait collection, or scene bounds.

`UIRequiresFullScreen` is still honored, but the app still resizes when the
device opens and closes, including in Split View.

## Safe areas and reserved regions

| Job | SwiftUI | UIKit |
|---|---|---|
| Keep foreground in safe area | default behavior | `view.safeAreaInsets`, or the safe area layout guide |
| Let background bleed | `.ignoresSafeArea()` | `view.bounds` |
| Custom UI outside the safe area (iOS 27.1) | `ReservedRegion` | `UIViewReservedRegion` |
| Query regions (iOS 27.1) | `reservedRegions(kind:options:)` on a `GeometryProxy`, from `GeometryReader` or `onGeometryChange` | `reservedRegions(kind:options:)` on `UIView` |

The UIKit signature, verbatim:

```swift
@MainActor func reservedRegions(
    kind: UIView.ReservedRegion.Kind,
    options: UIView.ReservedRegion.QueryOptions = []
) -> [UIView.ReservedRegion]
```

Region kinds (`divisionRegionKind` / `occlusionRegionKind` in Objective-C):

- **`.division`** — splits an area into smaller areas. The fold is a division
  region. It is *active* only while the device is folded; when flat it is
  inactive with zero width.
- **`.occlusion`** — covers part of an area. The inner FaceTime camera is an
  occlusion region, active only while that camera is active.

Option `.includeInactive` returns regions that exist but are not currently
active — useful for stable high-level decisions (for example, always preferring
an even column count on a device that *has* a fold).

Each region carries `frame`, `isActive` (`active` in Objective-C), `kind`, an
`id`/`identifier`, and **`margins`** — the insets the system suggests leaving
around the region. ⚠ The margins property is not mentioned in the Tech Talks;
prefer it over laying content flush against `frame`.

Safe areas and layout margins on iPhone Duo are frequently **asymmetric**. Never
assume opposite insets are equal.

## Arrangements (iOS 27.1)

A layout container that sits between navigation containers and content
containers, arranging exactly two views by rule.

| Job | SwiftUI | UIKit |
|---|---|---|
| Container | `ArrangementView(primary:secondary:)` | `UIArrangementViewController`, ⚠ `setViewController(_:for:animated:)` |
| Choose style | `.arrangementViewStyle(some ArrangementViewStyle)` | ⚠ `updateArrangement(_:animated:)` with `UISplitArrangement` / `UIOverlayArrangement` |
| Constrain split axis | `.split.axes(.horizontal)` | `.axes(.horizontal)` on the arrangement |
| Read overlay stacking | `@Environment(\.overlayArrangementZIndex)` | `state(for:)` → `ViewState.zIndex` |
| Look up a placement | — | `viewController(for:)`, `placement(for:)` |

⚠ Both UIKit mutators take an `animated:` parameter. The Tech Talks show them
without it.

SwiftUI declaration: `struct ArrangementView<Primary, Secondary> where Primary:
View, Secondary: View`, with `init(primary:secondary:)`.

- **split** — divides the bounds between primary and secondary. Splits
  horizontally when wider than tall, vertically when taller than wide. For
  main/detail relationships where neither view should be obscured.
- **overlay** — prefers stacking content above/below, moving to side-by-side
  when folded. For clear foreground/background relationships.

Do **not** put navigation containers (e.g. `NavigationSplitView`) inside an
arrangement, and do **not** put an arrangement inside `List` or `ScrollView`.

## Bars on the vertical axis

Opt in by rebuilding against the latest SDK **and** using container-provided
bars. Content from a hand-rolled `UIToolbar`, `UINavigationBar` or `UITabBar` is
not considered.

| Job | SwiftUI | UIKit |
|---|---|---|
| Custom back/close | `cancellationAction` placement | leading item, `leftItemsSupplementBackButton = false` |
| Prominent action | `topBarPinnedTrailing` placement | `pinnedTrailingGroup` |
| Force an axis | `AxisBehavior` (horizontal-only / vertical) | `AxisBehavior` |
| Detect a vertical bar | `toolbarVerticalEdge` environment value | `toolbarVerticalEdge` trait |
| Consolidate overflow | `ToolbarOverflowMenu` | `UINavigationItem.additionalOverflowItems` |
| Control collapse order | `ToolbarItemVisibilityPriority` | `UIBarButtonItemVisibilityPriority` |
| Group items (instead of manual spacers) | `ToolbarItemGroup` | `UIBarButtonItemGroup` |
| Title + symbol on an item | `Label` | `UIBarButtonItem` |
| Toolbar vs tab bar compression | toolbar compression behavior | toolbar compression behavior |
| Turn vertical bars off | `toolbarVerticalBehavior` | `preferredVerticalBarBehavior` |
| Tab bar as sidebar | default tab bar placement → `.sidebar` | tab bar controller sidebar preferred placement → `.sidebar` |
| Badges (iOS 26) | badge API | badge API |

**Availability differs within this table, which matters when setting a
deployment target.** The toolbar APIs are older than the foldable-specific ones:

| Symbol | Introduced |
|---|---|
| `ToolbarItemVisibilityPriority` (`.automatic` / `.low` / `.high`, plus `init(higherThan:)` / `init(lowerThan:)`) | iOS 27.0 |
| `UIBarButtonItemVisibilityPriority` (`.standard` / `.low` / `.high`, plus `init(rawValue:)`) | iOS 27.0 |
| `ToolbarOverflowMenu` | iOS 27.0 |
| `toolbarVerticalEdge` | **iOS 27.1** |

⚠ `toolbarVerticalEdge` is a `HorizontalEdge?` reporting the system's *preferred*
edge for a vertical bar in the current context — **whether or not one is
visible**. It is not a flag for "are items vertical right now"; use it to align
your own custom bars with the system's placement.

Note the naming asymmetry: SwiftUI's default is `.automatic`, UIKit's is
`.standard`.

## Hinge and scenes

| Job | SwiftUI | UIKit |
|---|---|---|
| Observe the hinge | `onHingeChange` modifier | `UIHingeInteraction` |
| Request a new scene | — | `UIWindowSceneActivation` action |
| Pair UI to another display | `sceneAccessory` modifier | scene accessory API |
| Outer-display camera UI | `CameraCaptureAccessory` | `CameraCaptureAccessory` |
| React to accessory availability | `onAvailabilityChange` | observation tracking |

`onHingeChange` hands you the previous and current hinge context. A `nil` hinge
means the device has no hinge. You get a coarse status — closed, partially open,
fully open — plus a continuous angle.

In UIKit the shape is different from the SwiftUI modifier and worth reading
directly. `UIHingeInteraction` takes an update handler with **two arguments, the
interaction and an `Update`** — not a previous/current pair — and has an
`isEnabled` flag:

```swift
init(updateHandler: (UIHingeInteraction, UIHingeInteraction.Update) -> Void)
```

The hinge state itself is a separate `UIHinge` object exposing `angle: CGFloat`
and `status: UIHinge.Status`. Both are iOS 27.1.

Use the hinge for **interactions and effects**. Use arrangements and reserved
regions for **layout**.

New windows cannot be created while on the outer display — that is reserved for
the inner display. Handle scene-request failures, and prefer
`UIWindowSceneActivation`, which hides itself when new windows are unavailable.

## Camera (AVFoundation / AVKit)

| Job | API |
|---|---|
| Discover a front camera | `AVCaptureDevice.DiscoverySession`, position `.front`, Wide or Ultra Wide device type → resolves to the **virtual front camera** |
| Address one physical camera | built-in **outer** ultra-wide device type; built-in **inner** ultra-wide device type |
| Track which way cameras face | `AVCaptureDeviceDirectionCoordinator` (AVKit) |
| Read the current facing | `deviceDirections` on the coordinator, or the map passed to the change handler |
| Group cameras by facing | ⚠ `AVCaptureDeviceDirectionMap` (AVKit) |
| Pass a device across actors | `AVCaptureDeviceDescriptor` (AVKit) — sendable |
| Keep captures upright | `AVCaptureDeviceRotationCoordinator` |
| Fit the preview | `videoGravity` on `AVCaptureVideoPreviewLayer` |
| Use the square sensor fully | `dynamicAspectRatio` on `AVCaptureDevice` |

The direction coordinator is main-actor isolated and reports facing **relative to
the display its view is on**. Use one coordinator per view when you drive both
displays at once.

```swift
init(view: UIView,
     deviceTypes: [AVCaptureDevice.DeviceType],
     changeHandler: ((AVCaptureDeviceDirectionMap) -> Void)?)
```

⚠ The handler receives an **`AVCaptureDeviceDirectionMap`**, not a descriptor.
The map holds two arrays — `forwardFacingDeviceDescriptors` and
`backwardFacingDeviceDescriptors` — so your handler picks a descriptor rather
than being handed one. The same map is readable any time via `deviceDirections`.

An `AVCaptureDeviceDescriptor` carries `uniqueID`, `localizedName`, `deviceType`,
`mediaTypes` and `position`. Both it and the map live in **AVKit**, not
AVFoundation.

Virtual front camera trade-off: automatic switching, but only the capabilities
common to both physical cameras — 1080p, 60 fps, and **no depth**.

Related Apple articles: *Choosing a Camera by the Direction it Faces*,
*Supporting Device Rotation in Your Camera App*.
