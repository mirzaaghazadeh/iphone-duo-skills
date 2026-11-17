---
name: iphone-duo-react-native
description: Adapt a React Native or Expo app to iPhone Duo, Apple's first foldable iPhone — asymmetric safe area insets, resize handling, and how to expose the iOS 27.1 reserved-region and hinge APIs through a native module. Use when a React Native, Expo or JS-based iOS app needs foldable iPhone support.
---

# React Native on iPhone Duo

React Native has **no fold or hinge API**. There is no `useDisplayFeatures`, no
hinge event, nothing that tells JavaScript the device is folded. As of this
writing no React Native or Expo release has shipped iPhone Duo support.

The good news is that the two things that break most often — resizing and safe
areas — are already solvable with libraries you probably have installed. Work in
two tiers.

## Tier 1 — works today, no native code

### Safe area insets, handled per edge

This is where React Native apps break on iPhone Duo, and it is worth being blunt
about why: **the safe area is asymmetric here.** iOS moves its controls to one
side of the display, so `left` and `right` insets differ — and which side depends
on the pose and on which half of a Split View your app occupies.

Use `useSafeAreaInsets()` from
[`react-native-safe-area-context`](https://github.com/AppAndFlow/react-native-safe-area-context).
It returns `{ top, right, bottom, left }` as independent numbers, and it updates
when the insets change.

```js
const insets = useSafeAreaInsets();
// each edge, independently
paddingLeft: insets.left,
paddingRight: insets.right,
```

Three things to avoid:

- **`SafeAreaView` from `react-native` core** — deprecated, and it only ever
  handled the notch case properly. Use the context library's hook or its
  `SafeAreaView`.
- **Symmetric math** — anything shaped like `width - insets.left * 2` is wrong
  the moment the insets differ, which on this device is most of the time.
- **Reading insets once** — they change while the app is running, so read them
  through the hook on every render rather than caching.

If you're on React Native 0.81+ with edge-to-edge enabled, your content already
extends under the system UI, which makes correct inset handling load-bearing
rather than cosmetic.

### Resize on every render

The window changes size constantly on iPhone Duo: opening, closing, folding,
rotating, entering Split View.

Use `useWindowDimensions()`. It is a hook, so it re-renders on change — unlike
`Dimensions.get('window')`, which returns a snapshot that silently goes stale.
If you have `Dimensions.get(...)` at module scope or in a constant, that is a
bug on this device.

For component-level sizing, `onLayout` gives you the actual measured box, which
is more reliable than deriving from window dimensions.

### Branch on width, not on device

iOS thinks in size classes: the outer display is **compact width**, the inner is
**regular width**. React Native has no equivalent, so use width breakpoints from
`useWindowDimensions()`.

Do not branch on `Platform.OS`, a device model from `react-native-device-info`,
or orientation. The inner display does not honor supported orientations, so
orientation tells you less than you think.

### Give the inner display a real layout

A phone layout stretched to 7.6 inches looks unfinished. The cheap win is a
two-column or master-detail layout above your wide breakpoint — and if you use
React Navigation, a drawer or rail-style navigator on wide and tabs on narrow.

## Tier 2 — needs a native module

Anything genuinely iPhone Duo-specific requires bridging from Swift. Worth it in
this order:

| Native API (iOS 27.1) | Why expose it to JS |
|---|---|
| `reservedRegions(kind:)` on `UIView` | Keep touch targets out of the fold and clear of the under-display camera |
| `UIHingeInteraction` | Continuous hinge angle, for effects |
| `traitCollection` size class | The signal iOS actually uses, instead of your breakpoint guess |

### Shape of the module

Write a **TurboModule** (New Architecture) or a legacy native module, with a
`NativeEventEmitter` for anything continuous. The hinge angle is a live stream —
push it as events; do not let JS poll it.

Query the reserved regions from the view your React content is mounted in, since
those APIs hang off `UIView` and regions are reported relative to a view. Emit
regions as plain objects (`{ x, y, width, height, kind, active }`) so JS can lay
out against them directly.

Guard hard. The same JS bundle runs on every iPhone, so the module must return
"no regions, no hinge" on non-folding devices and on anything below iOS 27.1
rather than throwing. Availability-check in Swift; never assume.

If you are in **Expo**, this means a config plugin plus a local native module —
it will not work in Expo Go, so you need a development build.

### Then feed it into Tier 1

Once regions reach JS, they are just numbers in your existing layout. An absolute
`View` positioned around a division region keeps a control out of the fold; a
`marginRight` derived from an occlusion region keeps content off the camera.

## What the simulator showed

Everything above is from Apple's documentation. This section is from running a
React Native 0.88 / Expo 58 app in the iPhone Duo simulator (Xcode 27.2, built
against the iOS 27.2 SDK) with `react-native-safe-area-context` 5.10 and
`react-native-screens` 4.30. Treat it as one app's observations, not a
specification, and re-check on your own versions.

### A header you draw yourself is under the status bar

With `headerShown: false` and a custom header, nothing moves your buttons into
the system's vertical bar. On both displays the status bar and Dynamic Island sit
over the trailing ~84 pt of the window, on top of whatever you put in that
corner. `useSafeAreaInsets()` reported `{ top: 0, right: 84, bottom: 34, left: 0 }`
on the outer display in portrait, so padding only for `insets.top` — the usual
iPhone habit — leaves the trailing controls covered.

Inset the content by `insets.left` and `insets.right` and let the background
run to the edges:

```js
const insets = useSafeAreaInsets();
<View style={{ flex: 1, backgroundColor, paddingTop: insets.top }}>
  <View style={{ flex: 1, marginLeft: insets.left, marginRight: insets.right }}>
    {/* header and content */}
  </View>
</View>
```

Once you do, "the width I can draw in" is no longer the window's. Anything
sized from `useWindowDimensions().width` — a swipe threshold expressed as a
fraction of the width, a strip that spaces its items across the screen, a
toast's `maxWidth` — should use `width - insets.left - insets.right` instead.
Pass it down through context so each component asks for its pane's width.

### Presented screens report no side insets

A screen presented with `presentation: 'modal'` or `'formSheet'` does not get
the side inset from its own safe area: `SafeAreaView` from
`react-native-safe-area-context` with `edges={['left', 'right']}` added no
padding inside one, while the content sat under the status bar on the outer
display.

The root insets from `useSafeAreaInsets()` are still correct for the *window*,
but applying them blindly is wrong too. On the inner display a sheet floats in
the middle of the screen (and slides to one side of the fold when the device is
partially folded), nowhere near the reserved strip; padding it by 84 pt takes
width it could have used.

Measure where the presented screen is and pad only its overlap:

```js
function ClearOfSides({ style, children }) {
  const { width: windowWidth } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const ref = useRef(null);
  const [frame, setFrame] = useState(null);
  const measure = useCallback(() => {
    ref.current?.measureInWindow((x, _y, width) => {
      if (width) setFrame((was) => (was?.x === x && was?.width === width ? was : { x, width }));
    });
  }, []);
  const x = frame?.x ?? 0;
  const width = frame?.width ?? windowWidth;
  return (
    <View
      ref={ref}
      onLayout={measure}
      style={[style, {
        paddingLeft: Math.max(0, insets.left - x),
        paddingRight: Math.max(0, x + width - (windowWidth - insets.right)),
      }]}>
      {children}
    </View>
  );
}
```

`onLayout` fires again when the device opens or closes, so the padding follows
the pose. With React Navigation 7 or Expo Router, the navigator's `screenLayout`
prop applies this to every pushed screen in one place.

### Folding while a text input is focused

Opening or closing the device re-wraps text. A `ScrollView` that had scrolled a
focused `TextInput` above the keyboard on the narrow display keeps that offset
on the wide one, where the same content is several lines shorter — the offset
can end up past the end of the content, and the screen looks empty until the
user drags it.

When the scroll view's *width* changes, wait for the rows to report their new
heights, then scroll the focused input back into view. `onLayout` on the
container gives you the width change; a short delay (350 ms covered the
transition here) is enough before calling `scrollTo`.

The keyboard itself stayed up across the fold with focus and selection intact,
and a `KeyboardStickyView` accessory
(`react-native-keyboard-controller`) followed it to the new display without any
changes.

### Two panes without a native module

For a two-pane layout on the inner display, split at the middle of the *window*,
not the middle of the safe width:

```js
const first = windowWidth / 2 - insets.left;            // leading pane
const second = windowWidth - insets.left - insets.right - first;  // trailing pane
```

The fold is at the centre of the inner display, so when the app fills it this
puts the gap between the panes on the fold with no bridge to the reserved-region
API. The panes come out unequal (about 475 pt and 391 pt in landscape, the
narrower one beside the status bar), and each should lay out against its own
width.

This is a heuristic, not fold detection: it is right when the app has the whole
inner display, and merely harmless in Split View, where the window is one half
and has no fold in it. If a control has to avoid the fold in every
configuration, that still needs Tier 2.

### A simulator quirk worth knowing

After changing the simulator's pose, the software keyboard can be hidden while
its frame is still reported, so a keyboard accessory floats in the middle of the
screen over nothing. Turning the on-screen keyboard back on (I/O → Keyboard →
Toggle Software Keyboard) clears it. It is not an app bug; do not chase it.

## What to do, in order

1. Swap any `Dimensions.get()` for `useWindowDimensions()`.
2. Swap core `SafeAreaView` for `useSafeAreaInsets()`, and audit every inset
   expression for symmetric math. If you draw your own header, inset it by
   `left` and `right`, and check modals and sheets separately — they need their
   own handling (see *What the simulator showed*).
3. Replace platform/orientation branching with width breakpoints.
4. Add a wide-layout path so the inner display earns its size.
5. Only then write the native module, and only if fold awareness genuinely
   improves the app.

Steps 1–4 are plain React Native work that pays off on tablets and foldable
Android too. Step 5 is the only iPhone Duo-specific part, and it needs the
Xcode 27.1 simulator to test.

The reasoning behind the native APIs is in
`../iphone-duo-adaptive-layout/SKILL.md` and `../iphone-duo-readiness/SKILL.md`.
The design guidance in `../iphone-duo-design-review/SKILL.md` is framework-neutral
and applies to a React Native app unchanged.
