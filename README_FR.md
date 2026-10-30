# iPhone Duo Skills

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [Türkçe](README_TR.md)

> Ce document est une traduction du [README](README.md) anglais. En cas de divergence, la version anglaise fait foi.

![iPhone Duo partiellement plié, montrant l'écran intérieur avec le Dock et les commandes disposés verticalement le long du bord droit](https://raw.githubusercontent.com/mirzaaghazadeh/iphone-duo-skills/main/assets/iphone-duo-hero.webp)

<sup>Image © Apple Inc., issue de la [page développeur iPhone Duo](https://developer.apple.com/iphone-duo/), utilisée à des fins d'identification. Ce projet n'est ni affilié à Apple ni approuvé par Apple.</sup>

Des skills d'agent IA pour développer des apps iOS sur **iPhone Duo** — le
premier iPhone pliable d'Apple, annoncé le 9 septembre 2026.

Les ressources développeur d'Apple pour l'iPhone Duo comptent désormais six
vidéos Tech Talk, la page HIG
[Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo),
la checklist [Prepare](https://developer.apple.com/iphone-duo/prepare/) et la
référence d'API. Ces deux dernières sont arrivées après le lancement de ce dépôt :
la référence d'API a corrigé trois affirmations, et le guide Prepare en a ajouté
plusieurs autres. Les deux mises à jour sont prises en compte ici.

Ces skills condensent l'ensemble en consignes structurées qu'un agent peut
appliquer directement, accompagnées de fiches de référence sur les
caractéristiques de l'appareil et l'ensemble des API.

## Installation

```bash
npx skills add mirzaaghazadeh/iphone-duo-skills
```

Installe les onze skills. La CLI détecte votre agent — Claude Code, Cursor,
Copilot, Gemini et d'autres — et les place là où cet agent va les chercher.

Options utiles :

```bash
# un seul skill
npx skills add mirzaaghazadeh/iphone-duo-skills --skill iphone-duo-readiness

# au niveau utilisateur plutôt qu'au niveau du projet
npx skills add mirzaaghazadeh/iphone-duo-skills --global

# voir le contenu sans rien installer
npx skills add mirzaaghazadeh/iphone-duo-skills --list
```

Pour essayer un skill sans l'installer du tout :

```bash
npx skills use mirzaaghazadeh/iphone-duo-skills@iphone-duo-readiness
```

<details>
<summary>Installation manuelle</summary>

```bash
git clone https://github.com/mirzaaghazadeh/iphone-duo-skills.git
cp -r iphone-duo-skills/skills/* ~/.claude/skills/
```

Ou au niveau du projet, dans le dossier `.claude/skills/` d'un dépôt.

</details>

Chaque skill est un `SKILL.md` autonome avec un frontmatter YAML : il fonctionne
donc aussi partout où des instructions en Markdown simple sont lues. Redémarrez
la session et les skills apparaissent ; appelez-en un par son nom, ou décrivez
simplement la tâche.

## Les skills

| Skill | Compatible avec | À utiliser quand |
|---|---|---|
| **iphone-duo-readiness** | SwiftUI · UIKit | Point d'entrée. Audit ou portage d'une app existante — niveaux de SDK, traque des hypothèses figées, zones de sécurité, orientation vers les autres skills. |
| **iphone-duo-adaptive-layout** | SwiftUI · UIKit | Du contenu tombe dans le pli. Régions réservées, division ou occlusion, schémas de déplacement, `ArrangementView`. |
| **iphone-duo-vertical-bars** | SwiftUI · UIKit | Barres d'outils et barres d'onglets. L'axe vertical, symbole ou texte, `AxisBehavior`, débordement et priorité de visibilité. |
| **iphone-duo-hinge-and-scenes** | SwiftUI · UIKit | Effets pilotés par la charnière, Split View, scènes multiples, interface sur les deux écrans via les accessoires de scène. |
| **iphone-duo-camera** | AVFoundation · AVKit | Apps de capture. Caméra frontale virtuelle ou caméras individuelles, coordinateur de direction, effet miroir, aperçu. |
| **iphone-duo-dual-pane-patterns** | SwiftUI · UIKit | Décider de ce qui va dans chaque volet. Dimensions en pixels et en points, zones de sécurité et jetons de mise en page, types exacts des callbacks de charnière, correspondance posture → schéma, effets pilotés par la charnière, paywalls sur deux volets, onboarding qui tient compte du pli. |
| **iphone-duo-design-review** | Tout framework | Critique de design plutôt que de code — postures, commandes latérales, asymétrie, évitement du pli, sheets. |
| **iphone-duo-games** | Unity · Unreal · Godot · SpriteKit · Metal | Le projet est un jeu. Remplir l'écran dans toutes les postures, ratio d'aspect ou letterboxing, commandes tactiles à l'écart du pli. |
| **iphone-duo-flutter** | Flutter · Dart | L'app est en Flutter. Ce que `MediaQuery` vous donne, pourquoi `displayFeatures` ne fonctionne pas ici, passerelle via les platform channels. |
| **iphone-duo-react-native** | React Native · Expo | L'app est en React Native. Insets asymétriques, gestion du redimensionnement, passerelle via un module natif. |
| **iphone-duo-capacitor** | Capacitor · Ionic · Angular · React · Vue | L'app tourne dans une web view. Pourquoi Device Posture et Viewport Segments ne l'atteignent pas, asymétrie des zones de sécurité, et comment obtenir l'état du pli côté natif. |

### Quels skills pour votre stack

**iOS natif — SwiftUI ou UIKit.** Commencez par `iphone-duo-readiness`, qui vous
oriente vers les autres. Les cinq skills centrés sur Swift citent de vraies API
iOS 27.1 que vous pouvez appeler directement ; `iphone-duo-design-review`
s'applique quel que soit votre outil.

**Flutter.** Lisez d'abord `iphone-duo-flutter`, puis `iphone-duo-design-review` —
les consignes de design sont indépendantes du framework et s'appliquent telles
quelles. Parcourez `iphone-duo-adaptive-layout` pour le *raisonnement* derrière
les régions réservées et le déplacement ; les concepts se transposent, même si
le code ne se transpose pas.

**React Native ou Expo.** Même démarche : `iphone-duo-react-native`, puis
`iphone-duo-design-review`, puis `iphone-duo-adaptive-layout` pour le contexte.

**Tout framework, si vous capturez des photos ou des vidéos.** `iphone-duo-camera`
compte quelle que soit la stack, car les deux caméras frontales et la question
« dans quelle direction cette caméra est-elle tournée ? » se jouent au niveau
d'AVFoundation. Les apps multiplateformes s'y heurtent via le plugin caméra
qu'elles utilisent, ou via leur propre passerelle.

**Jeux — Unity, Unreal, Godot, SpriteKit, Metal.** Lisez `iphone-duo-games`. Les
jeux échappent à la plupart des consignes d'interface, mais pas au
redimensionnement, et le pli est un vrai danger pour les commandes tactiles à
l'écran.

**Capacitor, Ionic ou une autre web view.** Lisez d'abord `iphone-duo-capacitor`,
puis `iphone-duo-design-review`. La subtilité : les API web standard pour cela
existent, mais dans une `WKWebView` elles restent derrière un flag expérimental
que seul Safari peut activer. L'état du pli doit donc venir du côté natif, même
si le CSS correspondant est spécifié.

**Kotlin Multiplatform, .NET MAUI et consorts.** Pas de skill dédié, mais le
schéma des skills Flutter et React Native se transpose directement : tout relève
soit *du redimensionnement et des zones de sécurité, gérables dans votre couche
existante*, soit *d'une passerelle native vers les API iOS 27.1*. Lisez le skill
multiplateforme le plus proche de votre configuration, ainsi que
`iphone-duo-design-review`.

> **Rappel de réalité multiplateforme.** Ni Flutter ni React Native ne prennent
> en charge l'iPhone Duo pour l'instant. `MediaQuery.displayFeatures` de Flutter est
> documenté comme renseigné **uniquement sur Android** ; il renvoie donc une
> liste vide ici. React Native n'a aucune API de pli. Les deux skills séparent ce
> qui fonctionne aujourd'hui de ce qui nécessite une passerelle native, pour que
> vous ne perdiez pas un après-midi à chercher une API qui n'existe pas.

## Référence

- [`reference/device-facts.md`](reference/device-facts.md) — écrans (pixels,
  ppi, points), dimensions, puce, caméras, postures et tableau des size classes
- [`reference/api-index.md`](reference/api-index.md) — chaque API annoncée,
  classée par usage, avec son framework et le SDK minimal
- [`reference/sources.md`](reference/sources.md) — toutes les sources, avec liens

## Ce qui compte vraiment sur cet appareil

Si vous ne lisez qu'une chose :

**L'iPhone Duo n'est pas un nouvel idiom — c'est un continuum de tailles plus
large.** Chaque bug d'un portage sur pliable vient d'une app qui tient quelque
chose pour fixe (cet idiom, cette orientation, cet écran, cette largeur, ces
marges symétriques), et chaque correctif remplace cette certitude par une
question sur l'espace disponible à cet instant.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/layout-model-dark.svg">
  <img alt="Trois états de l'appareil — fermé sur l'écran extérieur de 5,4 pouces (compact × regular, les barres passent sur le côté), partiellement plié avec une région de division au centre de l'écran intérieur (regular × regular, garder les cibles tactiles hors de la courbure), et ouvert à plat sur l'écran intérieur de 7,6 pouces (regular × regular, de la place pour une vue partagée). En dessous, la chaîne : posture, espace disponible, size class, ce que le système déplace." src="assets/layout-model.svg" width="900">
</picture>

<sup>Schéma réalisé par ce projet. Le comportement sous-jacent est documenté dans
les [Tech Talks iPhone Duo](https://developer.apple.com/iphone-duo/) d'Apple et
dans [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) ;
voir [`reference/sources.md`](reference/sources.md).</sup>

Trois conséquences concrètes :

1. **L'écran intérieur ignore les orientations d'interface que vous déclarez.**
   Décidez selon la size class, jamais selon l'orientation ou l'idiom.
2. **`UIScreen.main` est ambigu ici** et voué à être déprécié. Utilisez
   l'environnement, la trait collection ou les bounds de la scène.
3. **Les zones de sécurité sont asymétriques.** Tout calcul de la forme
   `width - safeAreaInsets.left * 2` est un défaut.

Et le changement le plus rentable : **compiler avec le SDK iOS 27.1.** C'est lui
qui débloque le contenu bord à bord, les barres verticales, les régions
réservées et les arrangements.

## Exactitude

Chaque affirmation technique remonte aux Tech Talks d'Apple, à la page HIG
*Designing for iPhone Duo*, à la référence d'API publiée ou au communiqué de la
Newsroom.

**Vérifié par rapport à la référence d'API d'Apple le 25 septembre 2026.** La
documentation des symboles est en ligne : les signatures de
`reference/api-index.md` en proviennent donc, et non plus des sessions Tech Talk.
Cette passe a corrigé trois erreurs :

- Le gestionnaire de changement du coordinateur de direction reçoit un
  `AVCaptureDeviceDirectionMap`, pas un `AVCaptureDeviceDescriptor` — il vous
  fournit des *tableaux* de descripteurs, tournés vers l'avant et vers l'arrière,
  parmi lesquels choisir.
- Les méthodes UIKit qui modifient un arrangement prennent un paramètre
  `animated:`. (La passe d'octobre a établi que sa valeur par défaut est
  `false` : les appels plus courts des Tech Talks compilent donc — ils ne sont
  simplement pas animés.)
- `toolbarVerticalEdge` indique le bord préféré par le système, **qu'une barre
  verticale soit visible ou non** — ce n'est pas un indicateur « les éléments
  sont-ils verticaux en ce moment ».

Une deuxième passe, le **27 septembre 2026**, a porté sur les types de charnière
et sur la requête SwiftUI des régions réservées, et a corrigé trois autres
points :

- `UIHinge.angle` (UIKit) est en **radians**, et `UIHinge.Status` a un quatrième
  cas, `.unknown`. `DeviceHinge.Status` (SwiftUI) est une struct, pas une enum.
- La requête SwiftUI `reservedRegions` prend un paramètre
  `layoutDirectionBehavior:` (par défaut `.mirrors`).
- Le `frame` d'une région réservée **inclut déjà** ses `margins` — ce ne sont
  pas des marges supplémentaires à ajouter autour.

Une troisième passe, le **23 octobre 2026**, après qu'Apple a transformé les
pages sur les régions réservées et les arrangements en articles complets, a
tranché une question et en a ouvert une autre :

- La requête de régions ne renvoie par défaut **que les régions actives**. La
  référence de septembre disait le contraire ; elle concorde désormais avec les
  Tech Talks.
- Le Tech Talk indique qu'un pli ouvert à plat est inactif et de largeur nulle ;
  la référence et le Group Lab Day 3 indiquent désormais qu'une région inactive
  conserve un frame pour lequel on peut prévoir de la place à l'avance. Les
  skills suivent les sources les plus récentes, avec une note invitant à
  vérifier ce frame dans le simulateur.
- Un arrangement split n'affiche **que sa vue principale** sur un iPhone Duo
  fermé tenu en paysage, ainsi que le long de tout axe que vous avez exclu.

Une quatrième passe, le **30 octobre 2026**, a lu *Registering a camera capture
accessory on iPhone Duo*, que le watcher de docs cherchait au mauvais chemin, et
a corrigé un point de plus :

- UIKit n'a **pas de `CameraCaptureAccessory`**. Il enregistre un
  `UISceneAccessory.cameraCapture(sceneConfiguration:userInfo:)` sur le view
  controller et reçoit en retour un `UISceneAccessoryRegistration` à observer et
  à activer ou désactiver.

Les corrections et les contradictions encore ouvertes sont signalées par ⚠ dans
l'index des API.

## Maintenance

Trois workflows gardent ce dépôt fiable, car le principal risque pour un dépôt
comme celui-ci est de se périmer sans que personne ne s'en aperçoive.

| Workflow | Exécution | Rôle |
|---|---|---|
| `validate.yml` | à chaque push et PR | Vérifie que chaque `SKILL.md` a un frontmatter valide, que `name` correspond à son dossier et est unique, que les renvois sont résolus, et que le paquet npm se construit toujours |
| `watch-apple-docs.yml` | le vendredi, 06:00 UTC | Compare 32 pages Apple — la page d'accueil, la checklist Prepare, la HIG, la référence d'API, les articles et les sessions — et ouvre (ou commente) une issue étiquetée `apple-docs` quand quelque chose change |
| `publish.yml` | à chaque release GitHub | Valide, vérifie que le tag correspond à `package.json`, puis publie sur npm avec provenance |

Les deux scripts fonctionnent aussi en local :

```bash
python3 scripts/validate-skills.py   # les mêmes vérifications que la CI
python3 scripts/check-sources.py     # rafraîchir la référence des docs Apple
```

## Licence

MIT — voir [LICENSE](LICENSE).

Ce projet n'est ni affilié à Apple ni approuvé par Apple. « iPhone » et
« iPhone Duo » sont des marques d'Apple Inc.
