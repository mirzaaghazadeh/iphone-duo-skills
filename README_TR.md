# iPhone Duo Skills

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [Türkçe](README_TR.md)

> Bu belge, İngilizce [README](README.md) dosyasının çevirisidir. İkisi arasında bir fark olursa İngilizce sürüm esas alınır.

![Kısmen katlanmış iPhone Duo; iç ekranda Dock ve kontroller sağ kenar boyunca dikey olarak sıralanmış](https://raw.githubusercontent.com/mirzaaghazadeh/iphone-duo-skills/main/assets/iphone-duo-hero.webp)

<sup>Görsel © Apple Inc., [iPhone Duo geliştirici sayfasından](https://developer.apple.com/iphone-duo/) alınmıştır ve yalnızca tanımlama amacıyla kullanılmaktadır. Bu proje Apple ile bağlantılı değildir ve Apple tarafından onaylanmamıştır.</sup>

**iPhone Duo** için iOS uygulamaları geliştirmeye yönelik agent skill'leri.
iPhone Duo, Apple'ın 9 Eylül 2026'da duyurduğu ilk katlanabilir iPhone'dur.

Apple'ın iPhone Duo için yayımladığı geliştirici materyalleri artık altı Tech
Talk videosu,
[Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
HIG sayfası, [Prepare](https://developer.apple.com/iphone-duo/prepare/) kontrol
listesi ve API referansından oluşuyor. Son ikisi bu depo başladıktan sonra
yayımlandı — API referansı üç iddiayı düzeltti, Prepare rehberi ise birkaç tane
daha ekledi. Her iki güncelleme de buraya yansıtıldı.

Bu skill'ler tüm bunları bir agent'ın doğrudan uygulayabileceği yapılandırılmış
yönergelere dönüştürür; ayrıca cihaz bilgileri ve API yüzeyinin tamamı için
başvuru sayfaları içerir.

## Kurulum

```bash
npx skills add mirzaaghazadeh/iphone-duo-skills
```

On bir skill'in tamamını kurar. CLI, kullandığınız agent'ı — Claude Code,
Cursor, Copilot, Gemini ve diğerleri — algılar ve skill'leri o agent'ın baktığı
yere yerleştirir.

Kullanışlı seçenekler:

```bash
# yalnızca tek bir skill
npx skills add mirzaaghazadeh/iphone-duo-skills --skill iphone-duo-readiness

# proje düzeyi yerine kullanıcı düzeyinde
npx skills add mirzaaghazadeh/iphone-duo-skills --global

# kurmadan içeriği görüntüle
npx skills add mirzaaghazadeh/iphone-duo-skills --list
```

Bir skill'i hiç kurmadan denemek için:

```bash
npx skills use mirzaaghazadeh/iphone-duo-skills@iphone-duo-readiness
```

<details>
<summary>Elle kurulum</summary>

```bash
git clone https://github.com/mirzaaghazadeh/iphone-duo-skills.git
cp -r iphone-duo-skills/skills/* ~/.claude/skills/
```

Ya da proje düzeyinde, bir deponun `.claude/skills/` klasörüne.

</details>

Her skill, YAML frontmatter içeren bağımsız bir `SKILL.md` dosyasıdır; bu yüzden
düz Markdown talimatlarını okuyan her ortamda da çalışır. Oturumu yeniden
başlattığınızda skill'ler görünür; birini adıyla çağırın ya da yapmak
istediğiniz işi anlatın.

## Skill'ler

| Skill | Uyumlu olduğu | Ne zaman kullanılır |
|---|---|---|
| **iphone-duo-readiness** | SwiftUI · UIKit | Başlangıç noktası. Mevcut bir uygulamayı denetlerken veya taşırken — SDK katmanları, sabit varsayımları bulup ayıklama, güvenli alanlar, diğer skill'lere yönlendirme. |
| **iphone-duo-adaptive-layout** | SwiftUI · UIKit | İçerik katlanma yerine denk geliyor. Ayrılmış bölgeler (reserved regions), bölünme ve örtme (division / occlusion), yer değiştirme desenleri, `ArrangementView`. |
| **iphone-duo-vertical-bars** | SwiftUI · UIKit | Araç çubukları ve sekme çubukları. Dikey eksen, sembol mü metin mi, `AxisBehavior`, taşma ve görünürlük önceliği. |
| **iphone-duo-hinge-and-scenes** | SwiftUI · UIKit | Menteşeye bağlı efektler, Split View, birden fazla sahne, sahne aksesuarlarıyla (scene accessories) iki ekranlı arayüz. |
| **iphone-duo-camera** | AVFoundation · AVKit | Çekim uygulamaları. Sanal ön kamera mı tekil kameralar mı, yön koordinatörü (direction coordinator), aynalama, önizleme. |
| **iphone-duo-dual-pane-patterns** | SwiftUI · UIKit | Her bölmeye ne konacağına karar verirken. Piksel/nokta boyutları, güvenli alan ve yerleşim token'ları, menteşe callback'lerinin tam türleri, duruş → desen eşleştirmesi, menteşeye bağlı efektler, iki bölmeli paywall'lar, katlanmayı hesaba katan onboarding. |
| **iphone-duo-design-review** | Her framework | Kod yerine tasarım eleştirisi — duruşlar, yan kontroller, asimetri, katlanma yerinden kaçınma, sheet'ler. |
| **iphone-duo-games** | Unity · Unreal · Godot · SpriteKit · Metal | Proje bir oyun. Her duruşta ekranı doldurmak, en-boy oranı mı letterbox mı, katlanma yerinden uzak dokunmatik kontroller. |
| **iphone-duo-flutter** | Flutter · Dart | Uygulama Flutter ile yazılmış. `MediaQuery` size neler veriyor, `displayFeatures` burada neden çalışmıyor, platform channel'lar üzerinden köprü kurmak. |
| **iphone-duo-react-native** | React Native · Expo | Uygulama React Native ile yazılmış. Asimetrik inset'ler, yeniden boyutlanmayı ele almak, native bir modül üzerinden köprü kurmak. |
| **iphone-duo-capacitor** | Capacitor · Ionic · Angular · React · Vue | Uygulama bir web view içinde çalışıyor. Device Posture ve Viewport Segments neden ona ulaşmıyor, güvenli alan asimetrisi ve katlanma durumunu native taraftan almak. |

### Hangi skill'ler sizin stack'inize uygun

**Native iOS — SwiftUI veya UIKit.** Sizi diğerlerine yönlendiren
`iphone-duo-readiness` skill'i ile başlayın. Swift odaklı beş skill, doğrudan
çağırabileceğiniz gerçek iOS 27.1 API'lerini adıyla verir;
`iphone-duo-design-review` ise ne ile geliştirirseniz geliştirin geçerlidir.

**Flutter.** Önce `iphone-duo-flutter`, ardından `iphone-duo-design-review`
skill'ini okuyun — tasarım yönergeleri framework'ten bağımsızdır ve olduğu gibi
geçerlidir. Ayrılmış bölgelerin ve yer değiştirmenin ardındaki *mantık* için
`iphone-duo-adaptive-layout` skill'ine göz atın; kod aktarılamasa da kavramlar
aktarılır.

**React Native veya Expo.** Aynı sıra: `iphone-duo-react-native`, ardından
`iphone-duo-design-review`, arka plan bilgisi için de
`iphone-duo-adaptive-layout`.

**Fotoğraf veya video çekiyorsanız, hangi framework olursa olsun.**
`iphone-duo-camera` stack'iniz ne olursa olsun önemlidir; çünkü iki ön kamera ve
"bu kamera hangi yöne bakıyor" sorunu AVFoundation düzeyindeki gerçeklerdir.
Çapraz platform uygulamalar bunlarla, kullandıkları kamera eklentisi ya da kendi
köprüleri üzerinden karşılaşır.

**Oyunlar — Unity, Unreal, Godot, SpriteKit, Metal.** `iphone-duo-games`
skill'ini okuyun. Oyunlar arayüz yönergelerinin çoğunu atlayabilir ama yeniden
boyutlanmayı atlayamaz; katlanma yeri de ekrandaki dokunmatik kontroller için
gerçek bir tehlikedir.

**Capacitor, Ionic veya başka bir web view.** Önce `iphone-duo-capacitor`,
ardından `iphone-duo-design-review` skill'ini okuyun. İşin püf noktası şu: bunun
için standart web API'leri mevcut, ancak bir `WKWebView` içinde yalnızca
Safari'nin açabildiği deneysel bir bayrağın arkasında kapalı duruyorlar. Bu
yüzden CSS tarafı tanımlı olsa bile katlanma bilgisi native taraftan gelmek
zorunda.

**Kotlin Multiplatform, .NET MAUI ve benzerleri.** Özel bir skill yok, ancak
Flutter ve React Native skill'lerindeki yaklaşım doğrudan aktarılabilir: her şey
ya *mevcut katmanınızda yapabileceğiniz yeniden boyutlanma ve güvenli alan
işleridir* ya da *iOS 27.1 API'lerine native bir köprüdür*. Kurulumunuza en
yakın çapraz platform skill'ini ve `iphone-duo-design-review` skill'ini okuyun.

> **Çapraz platform gerçeği.** Flutter da React Native de henüz iPhone Duo'yu
> desteklemiyor. Flutter'daki `MediaQuery.displayFeatures` belgelere göre
> **yalnızca Android'de** doldurulur; bu yüzden burada boş bir liste döndürür.
> React Native'in ise hiçbir katlanma API'si yok. Her iki skill de bugün
> çalışanı native köprü gerektirenden ayırır; böylece var olmayan bir API'yi
> ararken bir öğleden sonranızı kaybetmezsiniz.

## Başvuru

- [`reference/device-facts.md`](reference/device-facts.md) — ekranlar (piksel,
  ppi, nokta), boyutlar, çip, kameralar, duruşlar ve size class tablosu
- [`reference/api-index.md`](reference/api-index.md) — duyurulan her API,
  kullanım amacına göre, framework ve minimum SDK bilgisiyle
- [`reference/sources.md`](reference/sources.md) — tüm kaynaklar, bağlantılarıyla

## Bu cihazda gerçekten önemli olan

Başka hiçbir şey okumayacaksanız:

**iPhone Duo yeni bir idiom değil — daha geniş bir boyut yelpazesi.** Katlanabilir
cihaza yapılan bir uyarlamadaki her hata, uygulamanın sabit bir şeyi kesin kabul
etmesinden doğar (bu idiom, bu yön, bu ekran, bu genişlik, bu simetrik inset);
her düzeltme de bu kabulü, o anda kullanılabilir alana dair bir soruyla
değiştirir.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/layout-model-dark.svg">
  <img alt="Üç cihaz durumu — 5,4 inç dış ekranda kapalı (compact × regular, çubuklar yana geçer), iç ekranın ortasında bir bölünme bölgesiyle kısmen katlanmış (regular × regular, dokunma hedeflerini kıvrımdan uzak tutun) ve 7,6 inç iç ekranda tamamen açık (regular × regular, split view için yer var). Altta zincir: duruş, kullanılabilir alan, size class, sistemin taşıdığı öğeler." src="assets/layout-model.svg" width="900">
</picture>

<sup>Diyagram bu projeye aittir. Altta yatan davranış Apple'ın
[iPhone Duo Tech Talk'larında](https://developer.apple.com/iphone-duo/) ve
[Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
sayfasında belgelenmiştir; bkz. [`reference/sources.md`](reference/sources.md).</sup>

Üç somut sonuç:

1. **İç ekran, desteklediğinizi belirttiğiniz arayüz yönlerini yok sayar.**
   Kararı size class'a göre verin; asla yöne veya idiom'a göre vermeyin.
2. **`UIScreen.main` burada belirsizdir** ve kullanımdan kaldırılması
   planlanmaktadır. Environment'ı, trait collection'ı veya sahnenin bounds
   değerini kullanın.
3. **Güvenli alanlar asimetriktir.** `width - safeAreaInsets.left * 2`
   biçimindeki her hesap bir hatadır.

Ve en yüksek getirili tek değişiklik: **iOS 27.1 SDK'sıyla derleyin.**
Kenardan kenara içeriğin, dikey çubukların, ayrılmış bölgelerin ve
arrangement'ların kilidini bu açar.

## Doğruluk

Her teknik iddia Apple'ın Tech Talk'larına, *Designing for iPhone Duo* HIG
sayfasına, yayımlanmış API referansına ya da Newsroom duyurusuna dayanır.

**25 Eylül 2026'da Apple'ın API referansıyla doğrulandı.** Sembol belgeleri artık
yayında; bu yüzden `reference/api-index.md` içindeki imzalar Tech Talk
oturumlarından değil, bu belgelerden alınmıştır. Bu tur, yanlış olan üç şeyi
düzeltti:

- Yön koordinatörünün değişiklik işleyicisi `AVCaptureDeviceDescriptor` değil,
  bir `AVCaptureDeviceDirectionMap` alır — size aralarından seçim
  yapabileceğiniz, öne ve arkaya bakan descriptor *dizileri* verir.
- UIKit'te arrangement'ı değiştiren metotlar bir `animated:` parametresi alır.
  (Ekim ayındaki tur bunun varsayılan olarak `false` olduğunu ortaya koydu;
  yani Tech Talk'lardaki kısa çağrılar derlenir — yalnızca animasyon olmaz.)
- `toolbarVerticalEdge`, **dikey bir çubuk görünür olsun ya da olmasın**
  sistemin tercih ettiği kenarı bildirir — "öğeler şu anda dikey mi" bayrağı
  değildir.

İkinci tur **27 Eylül 2026** tarihinde yapıldı; menteşe türlerini ve SwiftUI'daki
ayrılmış bölge sorgusunu kapsadı ve üç şeyi daha düzeltti:

- UIKit'teki `UIHinge.angle` değeri **radyan** cinsindendir ve `UIHinge.Status`
  türünün dördüncü bir durumu vardır: `.unknown`. SwiftUI'daki
  `DeviceHinge.Status` ise enum değil, struct'tır.
- SwiftUI'daki `reservedRegions` sorgusu bir `layoutDirectionBehavior:`
  parametresi alır (varsayılan `.mirrors`).
- Bir ayrılmış bölgenin `frame` değeri, `margins` değerlerini **zaten içerir** —
  bunlar çevresine eklenecek ek boşluklar değildir.

Üçüncü tur, Apple'ın ayrılmış bölge ve arrangement sayfalarını kapsamlı
makalelere dönüştürmesinin ardından **23 Ekim 2026** tarihinde yapıldı; bir
soruyu çözdü, bir başkasını açtı:

- Bölge sorgusu varsayılan olarak **yalnızca aktif bölgeleri** döndürür. Eylül
  ayındaki referans aksini söylüyordu; artık Tech Talk'larla örtüşüyor.
- Tech Talk, düz açılmış bir katlanma yerinin sıfır genişlikle pasif olduğunu
  söylüyor; referans ve Group Lab Day 3 ise artık pasif bir bölgenin, önceden yer
  ayırabileceğiniz bir frame'i koruduğunu söylüyor. Skill'ler daha yeni
  kaynakları izler ve bu frame'i simülatörde kontrol etmenizi öneren bir not
  içerir.
- Bir split arrangement, yatay tutulan kapalı bir iPhone Duo'da ve hariç
  tuttuğunuz her eksen boyunca **yalnızca birincil görünümünü** gösterir.

Dördüncü tur **30 Ekim 2026** tarihinde yapıldı; belge izleyicisinin yanlış
yolda aradığı *Registering a camera capture accessory on iPhone Duo* makalesini
okudu ve bir düzeltme daha getirdi:

- UIKit'te **`CameraCaptureAccessory` yoktur**. View controller üzerinde bir
  `UISceneAccessory.cameraCapture(sceneConfiguration:userInfo:)` kaydedilir;
  geri dönen `UISceneAccessoryRegistration` ile erişilebilirlik izlenir ve
  içerik açılıp kapatılır.

Düzeltmeler ve hâlâ açık olan çelişkiler API dizininde ⚠ ile işaretlenmiştir.

## Bakım

Üç workflow bu deponun güncel kalmasını sağlar; çünkü böyle bir deponun asıl
riski, kimse fark etmeden güncelliğini yitirmesidir.

| Workflow | Ne zaman çalışır | Ne yapar |
|---|---|---|
| `validate.yml` | her push ve PR'da | Her `SKILL.md` dosyasının frontmatter'ının geçerli olduğunu, `name` alanının klasör adıyla eşleştiğini ve benzersiz olduğunu, çapraz bağlantıların çözüldüğünü ve npm paketinin hâlâ derlendiğini denetler |
| `watch-apple-docs.yml` | cuma günleri, 06:00 UTC | 32 Apple sayfasını — ana sayfa, Prepare kontrol listesi, HIG, API referansı, makaleler ve oturumlar — karşılaştırır ve bir şey değiştiğinde `apple-docs` etiketli bir issue açar (ya da mevcut issue'ya yorum yazar) |
| `publish.yml` | her GitHub release'inde | Doğrular, release tag'inin `package.json` sürümüyle eşleştiğini kontrol eder, ardından provenance ile npm'e yayımlar |

İki betik yerelde de çalışır:

```bash
python3 scripts/validate-skills.py   # CI'ın çalıştırdığı denetimlerin aynısı
python3 scripts/check-sources.py     # Apple belgelerinin referans durumunu yenile
```

## Lisans

MIT — bkz. [LICENSE](LICENSE).

Bu proje Apple ile bağlantılı değildir ve Apple tarafından onaylanmamıştır.
"iPhone" ve "iPhone Duo", Apple Inc.'in ticari markalarıdır.
