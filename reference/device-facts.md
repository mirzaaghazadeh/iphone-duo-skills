# iPhone Duo — device facts

Reference sheet for agents. Every number here comes from Apple's announcement or
the developer Tech Talks (see `sources.md`). Use it to sanity-check layout
assumptions; do **not** hardcode any of it into a layout.

## Identity

| | |
|---|---|
| Product | iPhone Duo — Apple's first foldable iPhone |
| Announced | September 9, 2026 |
| Pre-order | October 16, 2026 |
| Availability | October 23, 2026 |
| Price | From $1,999 (256 GB) up to $3,199 (2 TB) |
| Storage | 256 GB / 512 GB / 1 TB / 2 TB |
| OS | iOS 27 (ships with 27.x) |
| Form factor | Book-style inward fold, grade 5 titanium, precision hinge |
| Colors | Night Sky, Star White |
| Durability | Ceramic Shield 2 front, Ceramic Shield back, IP68 |

## Displays

| | Inner | Outer |
|---|---|---|
| Size | 7.6-inch (7.58 in diagonal as a rectangle) | 5.4-inch (5.36 in diagonal as a rectangle) |
| Panel | Super Retina XDR, foldable OLED | Super Retina XDR |
| Finish | Nano-texture, anti-glare | Standard |
| Notes | Under-display FaceTime camera | ~90% of the screen area of iPhone 18 Pro |

Both displays share the **same aspect ratio**, so the experience stays
continuous as the device opens and closes. Both are wider and shorter than a
traditional iPhone display — which is why system controls move to the side.

Peak outdoor brightness 3000 nits, ProMotion, Always On.

## Silicon and system

- **A20 Pro** — 6-core CPU (2 performance + 4 efficiency), 7-core GPU,
  dual 16-core Neural Engine, 12 GB RAM
- Custom vapor chamber, dual-battery architecture (5,400 mAh total)
- **N1** networking chip: Wi-Fi 7, Bluetooth 6, Thread
- **C2** cellular modem, mmWave in the US, eSIM-only worldwide
- USB-C 3.2 Gen 2, NFC, satellite connectivity
- Battery: up to 31 h video (inner display), up to 44 h (outer display)

## Cameras

**Rear:** 48 MP Fusion Main (with integrated optical-quality 2x telephoto,
sensor-shift OIS, zero shutter lag) + 48 MP Fusion Ultra Wide (macro).
4K120 Dolby Vision; Cinematic effects after capture up to 60 fps.

**Front — two of them, a first for iPhone.** Both are square sensors with an
ultra-wide field of view:

| | Inner front camera | Outer front camera |
|---|---|---|
| Placement | Under the inner display (first under-display camera on iPhone) | Outer display |
| Max video | 1080p @ 60 fps | 4K @ 120 fps |

A **virtual front camera** device sits in front of both and switches
automatically; it exposes only the intersection of their capabilities
(1080p / 60 fps, no depth). See `../skills/iphone-duo-camera/SKILL.md`.

## System UI behavior

- The Dynamic Island is redesigned to run **vertically** along the side of both
  displays, and expands vertically as Live Activities arrive.
- Lock Screen controls, the Home Screen Dock, and app navigation and controls
  appear **on the side** rather than top and bottom.
- **Split View** — two apps side by side on iPhone for the first time, as a
  50/50 split, created with the home gesture by dragging an app to one side.
- Picture-in-Picture can be pinned to the top of the screen; the app below
  resizes vertically to fit.
- StandBy works on either display, even off charger.

## Poses

Reason about poses, not about "portrait vs landscape". These five are the ones
Apple's HIG prose and the Tech Talks name explicitly:

1. **Closed** — outer display only, compact and one-handed.
2. **Open flat** — inner display, full canvas.
3. **Partially folded (book)** — the inner display curves through the center,
   dividing it into two usable regions.
4. **Tabletop / laptop** — seated on a surface, inner display facing the user;
   top region for viewing, bottom region for touch.
5. **Tent / standing on edge** — hands-free viewing.

> **Unresolved:** the HIG's poses illustration is captioned as showing *six*
> device poses, and the five above are all the surrounding prose names. A sixth
> is unaccounted for — plausibly a flipped/reversed configuration, since the
> camera guidance describes the device being flipped while open so the rear
> cameras face the user. Treat this list as the confirmed five rather than a
> complete set, and resolve it against the illustration when possible.

## Size classes

| Configuration | Horizontal | Vertical |
|---|---|---|
| Outer display, portrait | compact | regular |
| Outer display, landscape | compact | compact |
| Inner display (any orientation) | regular | regular |

The outer display behaves like any other iPhone. **The inner display does not
honor your supported interface orientations** — it rotates regardless. Never
branch layout on interface orientation or user interface idiom; branch on size
class and available space.
