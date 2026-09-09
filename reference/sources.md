# Sources

Everything in this repository is derived from Apple's own public material,
gathered September 10, 2026. No Apple content is reproduced here — these are
original notes and instructions written from the technical facts.

## Landing page

- [Get ready for iPhone Duo](https://developer.apple.com/iphone-duo/)

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
- [iPhone Duo](https://en.wikipedia.org/wiki/IPhone_Duo) — Wikipedia, for consolidated specs

## Related sessions referenced by the Tech Talks

- Modernize your UIKit app (WWDC26)
- What's new in SwiftUI (WWDC26)
- Support the Center Stage front camera in your iOS app (WWDC26)

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

## Documentation still pending

As of September 10, 2026 these were listed as "coming soon" or "coming later
this month" on the landing page. Check them before trusting any signature in
`api-index.md`:

- Xcode 27.1 beta
- *Designing for iPhone Duo* (Human Interface Guidelines)
- *Preparing your app for iPhone Duo*

## Keeping this current

Re-run the research when Xcode 27.1 ships. The Tech Talk pages carry a WebVTT
subtitle track in their HLS manifest, which is the most reliable way to read a
talk in full — see `scripts/fetch-transcripts.py`.
