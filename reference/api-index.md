# iPhone Duo — API index

Every API named across Apple's six iPhone Duo Tech Talks, grouped by job, with
the framework and the minimum SDK. Use this as a lookup table; the skills in
`../skills/` explain when and why to reach for each one.

> **Verified against the published API reference on 25 September 2026, and
> again on 23 October 2026** after Apple expanded the reserved-region and
> arrangement pages into full articles. The signatures below are taken from the
> reference rather than from the Tech Talk sessions. Where the two disagree, or
> where the reference corrected an earlier reading, the line is marked ⚠.

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
| Query regions (iOS 27.1) | `reservedRegions(kind:options:layoutDirectionBehavior:)` on a `GeometryProxy`, from `GeometryReader` or `onGeometryChange` | `reservedRegions(kind:options:)` on `UIView` |

The UIKit signature, verbatim:

```swift
@MainActor func reservedRegions(
    kind: UIView.ReservedRegion.Kind,
    options: UIView.ReservedRegion.QueryOptions = []
) -> [UIView.ReservedRegion]
```

The SwiftUI signature adds a layout-direction parameter:

```swift
func reservedRegions(
    kind: ReservedRegion.Kind,
    options: ReservedRegion.QueryOptions = [],
    layoutDirectionBehavior: LayoutDirectionBehavior = .mirrors
) -> [ReservedRegion]
```

Region geometry is physical — the camera doesn't move for right-to-left
languages — so by default SwiftUI **mirrors** the frames for you, which suits a
custom `Layout`. Pass `.fixed` when you need the unmirrored frames.

Region kinds (`divisionRegionKind` / `occlusionRegionKind` in Objective-C):

- **`.division`** — splits an area into smaller areas. The fold is a division
  region. It is *active* only while the device is partially folded; fully open,
  it is inactive.
- **`.occlusion`** — covers part of an area. The inner FaceTime camera is an
  occlusion region, active only while that camera is in use; the outer camera's
  region is always active. The API also reports the Dynamic Island and window
  controls as occlusion regions.

⚠ The Tech Talk says a flat fold is inactive **with a width of zero**. Two later
Apple sources say otherwise. The October reference says an inactive region
"still has a frame, so you can leave room for it", naming folding as the case,
and an engineer in Group Lab Day 3 describes querying the inactive fold ahead of
time so a 50/50 layout already clears it and nothing moves when the device
folds. Treat the talk's line as superseded, but check the inactive frame in the
simulator before relying on its size.

By default the query returns **only active regions**. Option `.includeInactive`
adds the ones that exist but are not currently active — useful for stable
high-level decisions (for example, always preferring an even column count on a
device that *has* a fold).

Each region carries `frame`, `isActive` (`active` in Objective-C), `kind`, an
`id`/`identifier`, and **`margins`** (`EdgeInsets` / `UIEdgeInsets`). ⚠ Per the
reference, `frame` **already includes** the margins — they are the part of the
frame kept clear for interactive content. Avoiding `frame` is enough; don't add
`margins` on top. Inset `frame` by `margins` to get the bare hardware area,
which is what full-bleed media may run up to. The margins property is not
mentioned in the Tech Talks.

⚠ The September reference said the query returned every intersecting region
*regardless* of whether it was active. The October revision says, on both the
type and the method pages, that the default returns only active regions — which
matches the Tech Talks. Filtering on `isActive` is still the right habit once you
pass `.includeInactive`.

Coordinates, from the October reference:

- `frame` is in the **queried view's own coordinate space**, in points, with
  `(0, 0)` at its top-leading corner. Only regions that overlap the view come
  back, and a partial overlap can produce a negative origin or a frame that runs
  past the view's size.
- In a custom `Layout`, the `bounds` handed to
  `placeSubviews(in:proposal:subviews:cache:)` don't always start at `(0, 0)`.
  Do the arithmetic from zero and add `bounds.origin` only when placing.
- Query in the view that positions the content, so the frames and the content
  share coordinates.
- UIKit tracks the regions you read in `updateConstraints()` and calls it again
  when they change — the natural place to read them.
- `ReservedRegion` is `Identifiable`; its `ReservedRegion.ID` is stable across
  queries, so it can drive a `ForEach` or tell an old region from a new one.

Scrolling containers — lists, tables, scroll views, collection views — do **not**
split their content around a division. A row can run across the fold; if that
hurts, read the division and lay the row out yourself.

Safe areas and layout margins on iPhone Duo are frequently **asymmetric**. Never
assume opposite insets are equal.

## Arrangements (iOS 27.1)

A layout container that sits between navigation containers and content
containers, arranging exactly two views by rule.

| Job | SwiftUI | UIKit |
|---|---|---|
| Container | `ArrangementView(primary:secondary:)` | `UIArrangementViewController`, ⚠ `setViewController(_:for:animated:)` |
| Choose style | `.arrangementViewStyle(some ArrangementViewStyle)` | ⚠ `updateArrangement(_:animated:)` with `UISplitArrangement` / `UIOverlayArrangement` |
| Constrain an axis | `.split.axes(.vertical)`, `.overlay.axes(_:)` | `.split.axes(.vertical)`, `.overlay.axes(_:)` |
| Size a split pane | `splitArrangementLayoutRatio(_:)`, `splitArrangementLayoutSize(minWidth:idealWidth:maxWidth:minHeight:idealHeight:maxHeight:)`, `splitArrangementFixedLayoutSize(horizontal:vertical:)` | `UISplitArrangement.DimensionRange` on the view properties' `width` / `height`, then `setViewProperties(_:for:)` |
| Choose an overlay view's side in landscape | `overlayArrangementEdge(_:)` | `edge` on the overlay's view properties, then `setViewProperties(_:for:)` |
| Read overlay stacking | `@Environment(\.overlayArrangementZIndex)` | `state(for:)` → `ViewState.zIndex` |
| Look up a placement | — | `viewController(for:)`, `placement(for:)` |
| Write a custom style | `ArrangementViewStyle.makeBody(configuration:)`, `ArrangementView(_:)` | — |

⚠ Both UIKit mutators take `animated: Bool = false`. The Tech Talks' calls
without it compile, they just don't animate; pass `animated: true` for an
animated transition. `setViewController(nil, for:)` empties a placement.

SwiftUI declaration: `nonisolated struct ArrangementView<Primary, Secondary>
where Primary: View, Secondary: View`, with `init(primary:secondary:)`. The
style protocol's default is `.automatic`.

- **split** — divides the bounds between primary and secondary, equally by
  default. Landscape: primary leading, secondary trailing. Portrait: primary
  on top. For main/detail relationships where neither view should be obscured.
- **overlay** — flat, the primary sits **above the secondary in z**. Folded, the
  two go side by side with the **secondary leading (or on top) and the primary
  trailing (or below)**. For clear foreground/background relationships.

Two cases show **only the primary view**: a split arrangement on a closed iPhone
Duo held in landscape, and any arrangement asked to lay out along an axis you
excluded with `axes(_:)`.

In UIKit, sizing starts from `UISplitArrangement.split.defaultViewProperties`;
a `DimensionRange` takes `minimum`, `preferred` and `maximum` as `Dimension`
values such as `.absolute(250)` or `.fractional(0.3)`. In SwiftUI, the view with
the higher `layoutPriority` gets its requested ratio or size and the other view
takes what is left.

Do **not** put an arrangement inside a scroll view, list, grid, collection view
or `NavigationSplitView` / `UISplitViewController`, and do **not** put a
`NavigationSplitView`, `TabView` or their UIKit counterparts inside one.

## Bars on the vertical axis

Opt in by rebuilding against the latest SDK **and** using container-provided
bars. Content from a hand-rolled `UIToolbar`, `UINavigationBar` or `UITabBar` is
not considered.

| Job | SwiftUI | UIKit |
|---|---|---|
| Custom back/close | `ToolbarItem` with `cancellationAction` placement | an item in `leadingItemGroups: [UIBarButtonItemGroup]` |
| Prominent action | `topBarPinnedTrailing` placement | `pinnedTrailingGroup` |
| Force an axis | `.axisBehavior(_:)` taking a `ToolbarItemAxisBehavior` | `UIBarButtonItem.axisBehavior` of type `UIBarButtonItem.AxisBehavior` |
| Detect a vertical bar | `toolbarVerticalEdge` environment value | `toolbarVerticalEdge` trait |
| Consolidate overflow | `ToolbarOverflowMenu` | `UINavigationItem.additionalOverflowItems`, a `UIDeferredMenuElement?` |
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
| Pair UI to another display | `sceneAccessory(content:)` modifier | `UISceneAccessory`, passed to `registerSceneAccessory(_:)` on a view controller |
| Outer-display camera UI | `CameraCaptureAccessory` | `UISceneAccessory.cameraCapture(sceneConfiguration:userInfo:)` |
| React to accessory availability | `onAvailabilityChange(perform:)` | `isAvailable` on the `UISceneAccessoryRegistration` — observable |
| Turn accessory content off | `CameraCaptureAccessory(isEnabled:content:)` | `isEnabled` on the registration |

SwiftUI, verbatim:

```swift
nonisolated func onHingeChange(
    isEnabled: Bool = true,
    _ action: @escaping (DeviceHingeContext, DeviceHingeContext) -> Void
) -> some View
```

The closure gets the previous and current `DeviceHingeContext`. Its `hinge` is a
`DeviceHinge?` — `nil` means the device has no hinge. `DeviceHinge` exposes
`angle: Angle` and `status: DeviceHinge.Status`. ⚠ `DeviceHinge.Status` is a
**struct** with static members `.closed`, `.partiallyOpen`, `.fullyOpen`
(Equatable and Hashable), not an enum — a `switch` over it needs `default`.

In UIKit the shape is different from the SwiftUI modifier and worth reading
directly. `UIHingeInteraction` takes an update handler with **two arguments, the
interaction and an `Update`** — not a previous/current pair — and has an
`isEnabled` flag:

```swift
init(updateHandler: (UIHingeInteraction, UIHingeInteraction.Update) -> Void)
```

`Update.hinge` is a `UIHinge?`, `nil` when the interaction leaves a hierarchy
that provides hinge updates. The handler fires on hinge changes **and** when the
interaction moves between hierarchies. `UIHinge` exposes `angle: CGFloat` —
⚠ **in radians** — and `status: UIHinge.Status`, an `Int`-backed enum with
⚠ **four** cases: `.closed`, `.partiallyOpen`, `.fullyOpen` and `.unknown`.
All of these types are iOS 27.1.

What the reference says about the values:

- The status is determined by the system from the angle **and device
  orientation** — don't recompute it from angle thresholds.
- The rate and granularity of angle updates are system policy and can change —
  don't depend on a frequency or precision.
- If closed / partially open / fully open is all you need, prefer `status`.
- The angle range is not documented; don't assume flat is exactly 180°.

Use the hinge for **interactions and effects**. Use arrangements and reserved
regions for **layout**.

New windows cannot be created while on the outer display — that is reserved for
the inner display. Handle scene-request failures, and prefer
`UIWindowSceneActivation`, which hides itself when new windows are unavailable.

### Scene accessories

⚠ UIKit has **no `CameraCaptureAccessory`** — this table used to list it in both
columns. UIKit builds the accessory from a scene configuration and registers it
on the view controller that shows the capture interface:

```swift
let configuration = UISceneConfiguration()
configuration.delegateClass = ScriptSceneDelegate.self

let accessory = UISceneAccessory.cameraCapture(sceneConfiguration: configuration,
                                               userInfo: script)
registration = registerSceneAccessory(accessory)   // keep a strong reference
```

The scene delegate reads `userInfo` back from
`connectionOptions.sceneAccessoryUserInfo`, an `Any?`. The system gives the
accessory's scene the role `UISceneSession.Role.windowCameraCaptureAccessory` —
apps never set it, and a scene-manifest entry for it has no effect.

| Symbol | Availability |
|---|---|
| `sceneAccessory(content:)`, `SceneAccessoryContent`, `onAvailabilityChange(perform:)` | iOS 27.0 |
| `UISceneAccessory`, `UISceneAccessoryRegistration`, `registerSceneAccessory(_:)`, `unregisterSceneAccessory(_:)`, `sceneAccessoryUserInfo` | iOS 27.0 |
| `CameraCaptureAccessory`, `UISceneAccessory.cameraCapture(sceneConfiguration:)` and `(sceneConfiguration:userInfo:)`, `windowCameraCaptureAccessory` | **iOS 27.1** |

What the reference and *Registering a camera capture accessory on iPhone Duo*
say:

- `isEnabled` is your app's choice; `isAvailable` is the system's, and one
  doesn't reflect the other. Turn content off with `isEnabled` (or the SwiftUI
  binding) rather than unregistering; call `unregisterSceneAccessory(_:)` only
  when the app stops offering the content.
- `isAvailable` is observable in `updateProperties()` and `layoutSubviews()`.
- The system presents the **top-most** registration of a kind. Navigating to a
  view that registers its own makes the previous one unavailable; going back
  restores it. Accessories of different kinds never compete.
- Content goes away when capture stops, the app leaves the foreground, or the
  device folds closed. It is on by default.
- Simulator has no camera. Check the content's layout in previews, then test
  presentation on a device.

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
