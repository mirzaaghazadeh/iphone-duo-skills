# iPhone Duo 技能库 (iPhone Duo Skills)

[English](README.md) | [简体中文](README_CN.md) | [Français](README_FR.md) | [Türkçe](README_TR.md)

> 本文是英文 [README](README.md) 的译文。如有出入，以英文版为准。

![iPhone Duo 半折叠状态，展示内屏右侧垂直排列的 Dock 与系统控制项](https://raw.githubusercontent.com/mirzaaghazadeh/iphone-duo-skills/main/assets/iphone-duo-hero.webp)

<sup>图片 © Apple Inc.，取自 [iPhone Duo 开发者页面](https://developer.apple.com/iphone-duo/)，仅用于识别说明。本项目非 Apple 官方产品，亦未获 Apple 赞助或认可。</sup>

专为 **iPhone Duo** 构建 iOS 应用的 AI Agent 技能库（Skills）——iPhone Duo 是 Apple 于 2026 年 9 月 9 日发布的首款折叠屏 iPhone。

Apple 针对 iPhone Duo 发布的官方开发者资料目前包含：6 场 Tech Talk 视频讲座、[Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) 人机交互指南（HIG）、[Prepare](https://developer.apple.com/iphone-duo/prepare/) 准备清单以及正式发布的 API 参考文档。后两者在该项目启动后上线——API 参考文档更正了最初宣称的三处技术细节，Prepare 指南随后补充了更多信息。这两轮更新的修正内容均已沉淀在此仓库中。

本技能库将所有官方资料提炼为 AI Agent 可直接执行的结构化指引，并配套提供了设备硬件参数速查表以及完整的 API 索引。

---

## 安装使用

```bash
npx skills add mirzaaghazadeh/iphone-duo-skills
```

该命令将安装全部 11 个技能。Skills CLI 会自动检测你的开发环境与 AI Agent（包括 Claude Code、Cursor、Copilot、Gemini、Antigravity 等），并自动部署到对应 Agent 的技能读取路径。

常用安装参数：

```bash
# 仅安装指定单个技能
npx skills add mirzaaghazadeh/iphone-duo-skills --skill iphone-duo-readiness

# 全局用户级安装（而非仅在当前项目）
npx skills add mirzaaghazadeh/iphone-duo-skills --global

# 在不安装的情况下查看包含的技能列表
npx skills add mirzaaghazadeh/iphone-duo-skills --list
```

如需免安装直接单次调用技能：

```bash
npx skills use mirzaaghazadeh/iphone-duo-skills@iphone-duo-readiness
```

<details>
<summary>手动安装说明</summary>

```bash
git clone https://github.com/mirzaaghazadeh/iphone-duo-skills.git
cp -r iphone-duo-skills/skills/* ~/.claude/skills/
```

或者复制到项目本地目录（例如放入当前仓库的 `.claude/skills/` 中）。

</details>

每个技能都是包含 YAML frontmatter 的独立 `SKILL.md` 文件，因此在任何支持纯 Markdown 规范的 Agent 环境中都能即开即用。重启会话后技能即可生效；你可以通过技能名称直接调用，或者直接用自然语言描述折叠屏相关的开发任务。

---

## 包含的技能（11 个）

| 技能名称 | 适用技术栈 | 适用场景 |
|---|---|---|
| **iphone-duo-readiness** | SwiftUI · UIKit | **总入口**。评估或迁移现有 App：SDK 适配梯度、硬编码假设排查、安全区问题排查、并路由至其他专项技能。 |
| **iphone-duo-adaptive-layout** | SwiftUI · UIKit | 内容跨越折痕。保留区域（Reserved Regions）、分割与遮挡区域、位移避让模式、`ArrangementView` 容器。 |
| **iphone-duo-vertical-bars** | SwiftUI · UIKit | 工具栏与标签栏适配。侧边垂直轴向、图标与文字协同、`AxisBehavior`、溢出菜单与可见性优先级。 |
| **iphone-duo-hinge-and-scenes** | SwiftUI · UIKit | 铰链角度驱动动效、Split View 分屏多任务、多 Scene 架构、利用场景配件（Scene Accessory）跨双屏呈现 UI。 |
| **iphone-duo-camera** | AVFoundation · AVKit | 相机摄录 App。虚拟前置相机与物理单摄选型、朝向协调器（Direction Coordinator）、镜像与取景预览。 |
| **iphone-duo-dual-pane-patterns** | SwiftUI · UIKit | 双窗格内容规划。像素与点阵尺寸、安全区与布局令牌、精确铰链回调类型、姿态与模式映射、铰链驱动动效、双屏付费墙与折痕感知引导页。 |
| **iphone-duo-design-review** | 全技术栈通用 | 设计评审而非代码实现：设备姿态、侧边控件、非对称布局、折痕避让、模态弹窗（Sheets）。 |
| **iphone-duo-games** | Unity · Unreal · Godot · SpriteKit · Metal | 游戏项目。各姿态下的全屏填充策略、宽高比自适应 vs 留黑边、屏幕虚拟触控避让折痕。 |
| **iphone-duo-flutter** | Flutter · Dart | Flutter App 适配。`MediaQuery` 的真实行为、为何 `displayFeatures` 在 iOS 上无效、通过 Platform Channels 桥接原生能力。 |
| **iphone-duo-react-native** | React Native · Expo | React Native App 适配。非对称 Insets 处理、重绘尺寸响应、通过原生模块（TurboModule）桥接 iOS 27.1 API。 |
| **iphone-duo-capacitor** | Capacitor · Ionic · Angular · React · Vue | 基于 WebView 的 App。为何 Device Posture / Viewport Segments 无法直接到达网页、非对称安全区、从原生侧获取折痕状态。 |

---

### 如何根据技术栈选用技能

- **原生 iOS 开发（SwiftUI / UIKit）**：
  从 `iphone-duo-readiness` 开始，它会指导整体排查并引导你进入其他专项技能。5 个针对 Swift 的专项技能详细覆盖了真实的 iOS 27.1 API；`iphone-duo-design-review` 则无论使用什么框架都适合做体验把关。

- **Flutter 开发**：
  首先阅读 `iphone-duo-flutter`，然后阅读 `iphone-duo-design-review`（设计规范是跨框架通用的）。浏览 `iphone-duo-adaptive-layout` 以理解保留区域与位移避让的*底层逻辑*；即便代码不同，设计理念是完全相通的。

- **React Native 或 Expo 开发**：
  路线类似：先查阅 `iphone-duo-react-native`，再参考 `iphone-duo-design-review`，最后查看 `iphone-duo-adaptive-layout` 补充底层背景。

- **包含相机摄录功能的任意框架 App**：
  无论使用何种技术栈，`iphone-duo-camera` 都至关重要。因为“两颗前置相机”以及“当前相机到底朝向哪一边”是 AVFoundation 底层的硬件事实。跨平台框架无论通过插件还是自定义桥接，最终都会直面这些硬件特性。

- **游戏开发（Unity、Unreal、Godot、SpriteKit、Metal）**：
  阅读 `iphone-duo-games`。游戏虽然可以规避大部分系统 UI 控件的规范，但无法避开窗口动态缩放，且折痕对于屏幕触控按钮来说是真实的物理盲区与操作障碍。

- **Capacitor、Ionic 或其他 WebView 混合应用**：
  先看 `iphone-duo-capacitor`，再看 `iphone-duo-design-review`。核心关键在于：相关的标准 Web API 虽然已经存在，但在 `WKWebView` 中被一个只有 Safari 才能开启的实验性开关关闭，App 无法自行开启。因此即便对应的 CSS 已有规范，折叠状态与折痕尺寸也必须由原生端桥接传递给前端。

- **Kotlin Multiplatform (KMP)、.NET MAUI 等其他生态**：
  虽然没有专属名称的独立技能，但其适配逻辑与 Flutter / React Native 技能完全一致：要么是*在现有跨平台层做尺寸变更与安全区监听*，要么是*编写原生桥接调用 iOS 27.1 API*。请参考相近的跨平台技能并配合 `iphone-duo-design-review`。

> **跨平台现实提醒**：
> 目前 Flutter 和 React Native 官方均未内置对 iPhone Duo 折叠屏特性的原生支持。Flutter 的 `MediaQuery.displayFeatures` 在官方文档中明确标注为**仅在 Android 上填充**，因此在 iPhone Duo 上返回空列表；React Native 官方也尚未提供折叠 API。跨平台技能清晰划分了“当前直接可用能力”与“需要原生桥接能力”，避免开发者把时间浪费在寻找不存在的开箱即用 API 上。

---

## 参考资料 (Reference)

- [`reference/device-facts.md`](reference/device-facts.md) — 屏幕参数（像素、PPI、点阵）、机身尺寸、芯片、相机、设备姿态（Poses）与 Size-Class 映射表
- [`reference/api-index.md`](reference/api-index.md) — 按功能分类的已公布 API 清单、所属框架与最低 SDK 要求
- [`reference/sources.md`](reference/sources.md) — 全部官方来源链接

---

## iPhone Duo 适配的核心准则

如果只记住一条原则：

**iPhone Duo 并非一种全新的设备类型（idiom），而是一个连续变化的尺寸光谱。**

折叠屏适配中的每一个缺陷，本质上都源于应用做出了某种“固定不变”的假设（固定设备类型、固定屏幕方向、固定屏幕对象、固定宽度、或假定安全区边距左右对称）；而每一个正确的修复方案，都是将该假设替换为对**当前可用空间**的动态查询。

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/layout-model-dark.svg">
  <img alt="三种设备状态：闭合（5.4英寸外屏，Compact x Regular，控件移至侧边）、半折叠（内屏中央有分割区域，Regular x Regular，触控区域避开折痕弧度）、平展展开（7.6英寸内屏，Regular x Regular，支持分屏浏览）。下方为关联链：姿态、可用空间、Size Class、系统移动项。" src="assets/layout-model.svg" width="900">
</picture>

<sup>本图由本项目制作。底层行为规范记录于 Apple 的 [iPhone Duo Tech Talks](https://developer.apple.com/iphone-duo/) 与 [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)；详见 [`reference/sources.md`](reference/sources.md)。</sup>

由此引出三条核心结论：

1. **内屏会忽略你的 `supportedInterfaceOrientations`。** 请基于 Size Class 进行分支判断，绝不要依据屏幕朝向或设备类型做硬编码判断。
2. **`UIScreen.main` 在此设备上语义歧义且已被列入弃用计划。** 请通过 Environment、Trait Collection 或 Scene 的实际 Bounds 来获取尺寸。
3. **安全区是非对称的（Asymmetric）。** 任何形式为 `width - safeAreaInsets.left * 2` 的计算公式在 iPhone Duo 上都是潜在的 Bug。

最关键的高杠杆动作：**使用 iOS 27.1 SDK 进行构建。**
这是解锁全屏延伸显示、侧边垂直工具栏、保留区域（Reserved Regions）与自适应容器（Arrangements）的唯一闸门。

---

## 准确性与官方勘误

所有技术主张均可追溯至 Apple 的 Tech Talks 讲座、HIG 交互指南、已发布的官方 API 参考或 Newsroom 新闻公告。

**2026 年 9 月 25 日依据 Apple API 参考文档进行了第一轮核验**。官方符号文档正式发布后，`reference/api-index.md` 中的函数签名直接对齐了官方头文件而非早期的演讲幻灯片。此轮校对更正了此前流传的三处偏差：
- 方向协调器的回调闭包接收的是 `AVCaptureDeviceDirectionMap`，而非单个 `AVCaptureDeviceDescriptor` —— 它会提供朝前和朝后的设备描述符*数组*供你选择。
- UIKit 的 arrangement 变更方法包含 `animated:` 参数。（10 月份核验发现其默认值为 `false`，因此 Tech Talk 中的简略调用代码能编译，只是默认没有动画）。
- `toolbarVerticalEdge` 返回系统偏好的边缘位置，**无论当前是否正在显示垂直工具栏** —— 它不是一个“工具项当前是否处于垂直状态”的布尔标记。

**2026 年 9 月 27 日进行了第二轮核验**，覆盖铰链类型与 SwiftUI 保留区域查询，修正了另外三处细节：
- UIKit 的 `UIHinge.angle` 单位为**弧度（radians）**，且 `UIHinge.Status` 拥有第四个枚举值 **`.unknown`**。SwiftUI 的 `DeviceHinge.Status` 是结构体而非枚举。
- SwiftUI 的 `reservedRegions` 查询带有 `layoutDirectionBehavior:` 参数（默认值为 `.mirrors`）。
- 保留区域的 `frame` **已经包含**了其 `margins` —— 它们不是需要你在外部额外附加的外边距。

**2026 年 10 月 23 日进行了第三轮核验**（在 Apple 将保留区域与 arrangement 页面扩展为完整专题文章后），解决了一个问题，同时引出了另一个问题：
- 保留区域查询默认**仅返回活跃区域（Active Regions）**。九月版参考文档此前的说法与此相反，现已与 Tech Talk 保持一致。
- Tech Talk 称完全平展时折痕是非活跃且宽度为 0；但最新参考文档与 Group Lab Day 3 表明非活跃区域仍保留其 Frame，以便开发者提前为其留出布局空间，避免设备弯折时界面跳动。本技能库以较新的来源为准，并附注提醒你在模拟器中核实该 Frame。
- 分割布局（Split Arrangement）在闭合横屏或排除的轴向上，**仅展示其主要视图（Primary View）**。

在 API 索引文件中，已修正项与争议点均使用 ⚠ 明确标注。

---

## 自动化与日常维护

为了防止随着 Apple 官方文档演进而出现信息滞后，本项目配置了三套 GitHub Actions 工作流：

| 工作流 | 触发时机 | 功能 |
|---|---|---|
| `validate.yml` | 每次 Push 和 PR | 检查每个 `SKILL.md` 的 YAML frontmatter、确保 `name` 与目录一致且唯一、检查所有相对 Markdown 链接有效性、验证 npm 包构建配置 |
| `watch-apple-docs.yml` | 每周五 06:00 UTC | 监控 16 个 Apple 官方页面（主页、Prepare 指南、HIG 及 API 参考），并在发生变更时自动创建或更新标签为 `apple-docs` 的 Issue |
| `publish.yml` | 发布 GitHub Release 时 | 校验内容、确认版本号匹配 `package.json`，并通过带有 Provenance 的流程自动发布至 npm |

本地运行校验与监控脚本：

```bash
python3 scripts/validate-skills.py   # 运行与 CI 完全相同的技能校验
python3 scripts/check-sources.py     # 刷新与 Apple 官方文档的对照基准
```

---

## 开源协议

基于 [MIT 协议](LICENSE) 开源。

本项目与 Apple Inc. 无隶属关系，亦未获其背书。"iPhone" 与 "iPhone Duo" 为 Apple Inc. 的商标。
