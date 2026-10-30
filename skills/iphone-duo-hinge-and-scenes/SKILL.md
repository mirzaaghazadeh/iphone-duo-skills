---
name: iphone-duo-hinge-and-scenes
description: Use the iPhone Duo hinge angle for interactions and effects, support Split View multitasking and multiple app scenes, and pair UI across both displays with scene accessories including CameraCaptureAccessory (SwiftUI) and UISceneAccessory.cameraCapture (UIKit). Use when building fold-driven effects, multi-window support, or dual-display experiences.
---

# Hinge, multitasking and scenes

Three capabilities that are unique to iPhone Duo, in rising order of ambition:
reacting to the hinge, participating in Split View, and putting your own UI on
both displays at once.

## The hinge

The system itself responds to the hinge — the wallpaper reacts to the angle with
a zoom effect as the device opens. Apps can read the same signal.

Use the `onHingeChange` modifier in SwiftUI, or `UIHingeInteraction` in UIKit.
Both give you:

- a coarse **status** — closed, partially open, fully open
- a **continuous angle**, updated live

`onHingeChange` hands your closure the previous and current hinge context.
`UIHingeInteraction` hands its handler the interaction and an `Update` instead,
and also fires when the view moves between hierarchies.

Watch the types — they differ between frameworks:

- SwiftUI's angle is an `Angle`; **UIKit's is a `CGFloat` in radians**.
- SwiftUI's `DeviceHinge.Status` is a struct (a `switch` needs `default`);
  UIKit's `UIHinge.Status` is an enum with a fourth case, **`.unknown`**.
- The system decides the status from the angle *and* device orientation, so
  don't recompute it from thresholds. Update rate and precision are system
  policy — don't assume a frequency.

Full signatures, a reusable normaliser, and effect patterns are in
`../iphone-duo-dual-pane-patterns/SKILL.md`.

Two things to check before using the value:

1. **Is there a hinge at all?** A `nil` hinge means the app is running on a
   device without one. Same binary, most devices.
2. **Is the device in a state you care about?** Usually you only want updates
   while partially open — and you need an `else` branch that resets whatever the
   angle was driving, so the effect doesn't stick at a stale value once the user
   opens the device flat.

Then map the angle to your parameter and update state.

### What the hinge is for

**Interactions and effects.** The angle is a live, continuous input stream — it
behaves like a sensor, and it suits things that respond continuously. Driving a
pitch bend from the fold angle, the way a whammy bar works, is the right shape of
idea.

**Not layout.** Do not lay out views from the hinge angle. Layout has proper
tools that are declarative, testable and correct on devices with no hinge:
arrangements and reserved regions, in
`../iphone-duo-adaptive-layout/SKILL.md`. Reaching for the angle here produces
layout that thrashes during the fold and breaks everywhere else.

## Split View multitasking

**Every app participates.** Two apps sit side by side, created with the familiar
home gesture — drag an app to one side and drop it. There's a second layout too,
stacking video and apps together when Picture-in-Picture is pinned. Your app
handles both identically.

If the app already supports resizing on iPad or under iPhone mirroring, it is
most of the way there. The system gives you size classes and scene geometry to
make layout decisions from; the general guidance in
`../iphone-duo-readiness/SKILL.md` applies unchanged.

The detail worth testing: in Split View, vertically laid out bar content can
appear on **either** side of your app, depending on which half you occupy. Drag
the app to both sides in Device Hub and check that asymmetric safe area handling
holds up.

## Multiple scenes

iPhone Duo is the first iPhone to support **multiple simultaneous instances of an
app's UI**. If the app already supports this on iPad, it works here too.

One behavior is genuinely new, though:

**New windows cannot be created on the outer display.** That is reserved for the
inner display, and the availability changes as the user opens and closes the
device. This dynamic availability doesn't exist on iPad.

Consequences:

- **Handle errors when requesting new scenes.** A request that always succeeded
  on iPad can now fail.
- **Prefer `UIWindowSceneActivation`**, which automatically hides itself when new
  windows aren't available — so users never tap an affordance that can't work.

## Scene accessories

Scene accessories pair additional content with your app's main UI on another
display. They aren't Duo-specific — the same mechanism backs using an iPhone as a
controller for a game on an external display — but iPhone Duo gives every user
two displays to work with.

The system controls availability dynamically. Accessories are enabled by default
and can be toggled at any time, so **observe availability rather than assuming
it**: use the `onAvailabilityChange(perform:)` modifier in SwiftUI, or read
`isAvailable` on the `UISceneAccessoryRegistration` in UIKit — it's observable
in `updateProperties()` and `layoutSubviews()`. Reflect the current state in
your UI (disabling a toggle button when the accessory can't be shown, for
instance).

### CameraCaptureAccessory

For camera apps, a camera capture accessory puts UI on the **outer** display —
which faces the same way as the camera — while the capture interface stays on
the **inner** one. The person in front of the lens gets something to look at: a
script to read, a countdown before recording starts, how much of them the camera
sees, or something to entertain a child.

The system decides when and where to present it. Your app passes no display,
capture session or camera; the system finds the active capture session itself.
Presentation needs the app **full screen on the inner display**, **in the
foreground**, with an **active capture session**. Treat the content as an
enhancement: the capture interface must work when nothing appears, and keep
every essential control there. The outer display accepts touch, which suits one
small capture task — tapping a preview to focus — not a second interface.

**Register the accessory on the same view as your camera UI.** Scoped that way,
it appears and disappears with the camera view, with no lifecycle code. The two
frameworks differ more than the names suggest — UIKit has **no
`CameraCaptureAccessory` type**:

```swift
// SwiftUI
CameraPreview()
    .sceneAccessory {
        CameraCaptureAccessory(isEnabled: $isScriptEnabled) {
            ScriptView(model: script)   // captures the model you already use
        }
        .onAvailabilityChange { showsScriptControls = $0 }
    }
```

```swift
// UIKit, in the camera view controller's viewDidLoad()
let configuration = UISceneConfiguration()
configuration.delegateClass = ScriptSceneDelegate.self
let accessory = UISceneAccessory.cameraCapture(sceneConfiguration: configuration,
                                               userInfo: script)
registration = registerSceneAccessory(accessory)   // hold it strongly

// Turning it off, and hiding controls (in updateProperties())
registration?.isEnabled = isScriptEnabled
scriptControls.isHidden = !(registration?.isAvailable ?? false)
```

In UIKit the scene delegate gets the model back from
`connectionOptions.sceneAccessoryUserInfo`. Keep your own strong reference to
it — `userInfo` identifies the object to the scene, it doesn't store it. The
system gives that scene the role `.windowCameraCaptureAccessory`; there's no
scene-manifest entry to add, and one would have no effect.

**Share state rather than sending messages.** Give the accessory the model the
capture interface already reads. A control the subject taps on the outer display
then changes what the person holding the device sees, with nothing in between.

**Turn it off rather than unregistering.** A toolbar toggle bound to `isEnabled`
is the natural control; disable or hide it while the accessory is unavailable.
Unregister only when the app stops offering the content. Availability changes
for reasons outside the app: the system presents only the **top-most**
registration of a kind, so navigating to a view that registers its own makes the
previous one unavailable until you go back, and content goes away when capture
stops, the app leaves the foreground, or the device folds closed. Accessories of
different kinds never compete — slides on an external display and capture
content on the outer display can run at once.

Simulator has no camera. Build the accessory from ordinary views so previews can
check its layout, then test presentation on a device.

Camera specifics — which physical camera is streaming, and which way it is
actually facing once two displays are involved — are in
`../iphone-duo-camera/SKILL.md`. That question gets genuinely subtle, and the
direction coordinator exists to answer it.

## Checklist

1. Support resizing first. Split View correctness follows from it.
2. Test the app on both sides of a Split View, in every pose.
3. If the app supports multiple windows, handle scene-request failure and adopt
   `UIWindowSceneActivation`.
4. Consider whether a hinge-driven effect genuinely improves the app — then guard
   for `nil` hinge and reset state when the device leaves the range you care
   about.
5. For camera apps, evaluate whether a camera capture accessory on the outer
   display would help the person in front of the lens — `CameraCaptureAccessory`
   in SwiftUI, `UISceneAccessory.cameraCapture` in UIKit — and test it on a
   device.
