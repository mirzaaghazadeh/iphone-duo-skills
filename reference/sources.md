# Sources

Everything in this repository is derived from Apple's own public material,
gathered September 10, 2026. No Apple content is reproduced here — these are
original notes and instructions written from the technical facts.

## Landing page

- [Get ready for iPhone Duo](https://developer.apple.com/iphone-duo/)

## Human Interface Guidelines

- [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
  — published September 9, 2026. Covers device anatomy and poses, dynamic
  layouts, the three reserved regions, split views, arrangement views, and
  vertical controls. It is also the source that confirms several toolbar API
  names, and the only source so far for the **games** guidance.

## Tech Talks

| ID | Title | Covered by |
|---|---|---|
| [111466](https://developer.apple.com/videos/play/tech-talks/111466/) | Design for iPhone Duo | `iphone-duo-design-review` |
| [111461](https://developer.apple.com/videos/play/tech-talks/111461/) | Prepare your app for iPhone Duo | `iphone-duo-readiness` |
| [111462](https://developer.apple.com/videos/play/tech-talks/111462/) | Raise the bar with iPhone Duo | `iphone-duo-vertical-bars` |
| [111463](https://developer.apple.com/videos/play/tech-talks/111463/) | Strike a pose with adaptive layouts on iPhone Duo | `iphone-duo-adaptive-layout` |
| [111464](https://developer.apple.com/videos/play/tech-talks/111464/) | Leverage multiple displays and scenes on iPhone Duo | `iphone-duo-hinge-and-scenes` |
| [111465](https://developer.apple.com/videos/play/tech-talks/111465/) | Build a great camera experience for iPhone Duo | `iphone-duo-camera` |

## Announcement and specs

- [Apple unveils iPhone Duo](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/) — Apple Newsroom, September 9, 2026
- [iPhone Duo — Technical Specifications](https://www.apple.com/iphone-duo/specs/) —
  display resolutions and ppi, dimensions, weight, Touch ID. Checked September 27, 2026.
- [iPhone Duo](https://en.wikipedia.org/wiki/IPhone_Duo) — Wikipedia, for consolidated specs

## Related sessions referenced by the Tech Talks

- Modernize your UIKit app (WWDC26)
- What's new in SwiftUI (WWDC26)
- Support the Center Stage front camera in your iOS app (WWDC26)

## Dual-screen patterns

For `iphone-duo-dual-pane-patterns`. Prior art from other foldable platforms,
which agrees with Apple's guidance on every point it overlaps:

- [Introduction to dual-screen devices](https://learn.microsoft.com/en-us/dual-screen/introduction) —
  Microsoft Surface Duo: extended canvas, list-detail, two page, dual view,
  companion pane.
- [Postures and orientation](https://developer.android.com/design/ui/mobile/guides/layout-and-content/postures-and-orientation)
  and [Make your app fold aware](https://developer.android.com/develop/adaptive-apps/guides/foldables/make-your-app-fold-aware) — Android.
- [Designing for foldables](https://developer.samsung.com/one-ui/largescreen-and-foldable/designing_for_foldable.html)
  and [Adapt your app for Flex Mode](https://developer.samsung.com/sdp/blog/en-us/2021/01/11/adapt-your-app-for-galaxy-flex-mode) — Samsung.
- [App Review Guidelines 3.1.2](https://developer.apple.com/app-store/review/guidelines/)
  and [`SubscriptionStoreView`](https://developer.apple.com/documentation/storekit/subscriptionstoreview) — for the paywall section.

## Community design resources

- [iPhone Duo Adaptive Design Starter Kit](https://www.figma.com/community/file/1681029753837117390/iphone-duo-adaptive-design-starter-kit)
  — Noah Elhadedy, Figma Community, v1.0, September 2026. Unofficial. Its safe
  areas, logical sizes, 84 pt vertical bar and 20 pt margins are aligned with the
  iPhone Duo templates in Apple's iOS and iPadOS 27 design resource (checked
  23 September 2026); every value carries an Official / Derived / Recommended /
  Assumption badge, and the dual-pane skill keeps that distinction. Column
  counts, pane gaps, the 27 pt fold band and the 600 pt text measure are the
  kit's own recommendations.

## Cross-platform

For the Flutter and React Native skills. Neither framework had iPhone Duo
support at the time of writing — these are the sources establishing what each
does and does not provide:

- [`DisplayFeature`](https://api.flutter.dev/flutter/dart-ui/DisplayFeature-class.html) —
  Flutter API docs, which state the property is **populated only on Android**.
  Exposes `bounds`, `type` (`hinge` / `fold` / `cutout`) and `state`
  (`postureFlat` / `postureHalfOpened` / `unknown`).
- [`dual_screen`](https://pub.dev/packages/dual_screen) — `TwoPane`,
  `hingeAngleEvents`, `hasHingeAngleSensor`. Last published around three years
  ago; Android-only in practice.
- [`react-native-safe-area-context`](https://github.com/AppAndFlow/react-native-safe-area-context) —
  `useSafeAreaInsets()`, the per-edge inset hook the React Native skill builds on.
- [Supporting safe areas](https://reactnavigation.org/docs/handling-safe-area/) —
  React Navigation, on preferring the hook over the deprecated core
  `SafeAreaView`.

## API reference

Re-checked **September 25, 2026**. Apple's symbol documentation is now live, and
`api-index.md` has been verified against it. The pages used:

- [`ReservedRegion`](https://developer.apple.com/documentation/swiftui/reservedregion)
  (SwiftUI) and [`UIViewReservedRegion`](https://developer.apple.com/documentation/uikit/uiviewreservedregion),
  plus [`reservedRegions(kind:options:)`](https://developer.apple.com/documentation/uikit/uiview/reservedregions(kind:options:))
- [`ArrangementView`](https://developer.apple.com/documentation/swiftui/arrangementview)
  and [`UIArrangementViewController`](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller)
- [`AVCaptureDeviceDirectionCoordinator`](https://developer.apple.com/documentation/avkit/avcapturedevicedirectioncoordinator),
  [`AVCaptureDeviceDirectionMap`](https://developer.apple.com/documentation/avkit/avcapturedevicedirectionmap),
  [`AVCaptureDeviceDescriptor`](https://developer.apple.com/documentation/avkit/avcapturedevicedescriptor)
- [`UIHingeInteraction`](https://developer.apple.com/documentation/uikit/uihingeinteraction),
  [`UIHinge`](https://developer.apple.com/documentation/uikit/uihinge) and
  [`UIHinge.Status`](https://developer.apple.com/documentation/uikit/uihinge/status-swift.enum)
- [`onHingeChange(isEnabled:_:)`](https://developer.apple.com/documentation/swiftui/view/onhingechange(isenabled:_:)),
  [`DeviceHingeContext`](https://developer.apple.com/documentation/swiftui/devicehingecontext),
  [`DeviceHinge`](https://developer.apple.com/documentation/swiftui/devicehinge) and
  [`DeviceHinge.Status`](https://developer.apple.com/documentation/swiftui/devicehinge/status-swift.struct)
- [`reservedRegions(kind:options:layoutDirectionBehavior:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:))
- [`ToolbarItemVisibilityPriority`](https://developer.apple.com/documentation/swiftui/toolbaritemvisibilitypriority),
  [`ToolbarOverflowMenu`](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu),
  [`toolbarVerticalEdge`](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge)
- [`CameraCaptureAccessory`](https://developer.apple.com/documentation/swiftui/cameracaptureaccessory)

That pass produced three corrections — the direction coordinator's change
handler, the `animated:` parameters on the UIKit arrangement mutators, and the
meaning of `toolbarVerticalEdge`. They are marked ⚠ in `api-index.md`.

## Prepare guide

- [Prepare — iPhone Duo](https://developer.apple.com/iphone-duo/prepare/) —
  published early October 2026, and the article that had been pending. A
  three-step developer checklist: run the App Resizability skill, fix a named set
  of patterns, then test resizing. Also the source for the `xcrun agent skills
  export` command, the SDK-tier behaviour descriptions, and the App Store
  guidance (screenshots, the Connect preview tool, featuring nominations).

Checked October 7, 2026: this page is live at `/iphone-duo/prepare/` rather than
under `documentation/`, which is why earlier probes for
`documentation/uikit/preparing-your-app-for-iphone-duo` returned 404 — they still
do.

## Keeping this current

Re-run the research when Xcode 27.1 ships. The Tech Talk pages carry a WebVTT
subtitle track in their HLS manifest, which is the most reliable way to read a
talk in full — see `scripts/fetch-transcripts.py`.
