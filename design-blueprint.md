# Design Blueprint — Huaxing PCBA

## CATEGORY
- **品类**: PCB/PCBA 一站式电子制造
- **视觉意象**: 电路精密感 + 金铜金属光泽 + 暗色工业氛围
- **色彩方向**: 金橙暖铜 (非默认PCB绿) — 偏高端珠宝感

## BRAND PERSONALITY （三轴定位）

```
技术先锋型 ◉────────────────○ 可靠传统型
（暗色底+细线科技感+微动效）

高端精密型 ◉────────────────○ 规模产能型
（大量留白/字少图大/金属色/细字体）

国际通路型 ◉────────────────○ 工厂直营型
（英文优先/极简/信任信号数据化）
```

**三轴组合**: 技术 × 高端 × 国际 → "暗金精工"美学

## DESIGN DIFFERENTIATORS （≥3项）

- [x] **主色**: 非默认PCB绿 → 金橙铜色系（#C8963E #D4A843 #E0B860）
- [x] **布局系统**: 首页Hero用暗色底+微电路纹理+大标题居中，不同于图文分屏/卡片网格
- [x] **字体个性**: 全站细字体（font-weight 200-300），标题用极细 + 宽松字距
- [x] **密度节奏**: 稀疏留白主导，信息段之间呼吸感强
- [x] **CTA策略**: 弹窗询盘（modal），不跳页打断浏览
- [x] **Hero构图**: 抽象科技纹理为底（暗色电路网格），金色微光点缀

## COLOR PALETTE

```
--bg-primary:     #08080b      主背景（近黑）
--bg-secondary:   #0f0f14      次级背景
--bg-surface:     #16161d      卡片/表面
--bg-elevated:    #1c1c24      悬浮层
--border:         #252530      边框
--border-light:   #2a2a35      浅边框

--accent:         #c8963e      主强调色 金铜
--accent-light:   #d4a843      亮金
--accent-glow:    #e8c56d      金色辉光
--accent-subtle:  rgba(200,150,62,0.12)  微金透明

--text-primary:   #e8e8ec      主文字
--text-secondary: #9898a8      次级文字
--text-muted:     #686878      弱化文字

--success:        #3aac7a
--warning:        #d4a843
--error:          #d9485e
```

**差异化理由**: PCB行业默认深绿，选金橙暖铜系立刻跳脱品类印象，既有电路铜箔的联想，又是高端珠宝/奢侈品常用色，符合"高端品牌站"定位。暗底+金色对比强烈，天然适合暗色模式。

## TYPOGRAPHY

```
--font-sans: 'Inter', system-ui, -apple-system, sans-serif
--font-display: 'Inter', system-ui, sans-serif
--font-mono: 'JetBrains Mono', 'Fira Code', monospace

标题: font-weight 300 (Light), letter-spacing 0.02em
副标题: font-weight 300
正文: font-weight 300 (Light), line-height 1.75
小字/数据: font-weight 400 (Regular)
数字/规格: font-weight 200 (ExtraLight), letter-spacing 0.04em
```

**字体来源**: 系统字体栈 + Inter（零CDN），细字体优先。
**字号比例**: 1.25 modular scale (base 16px)

## PAGE COLLECTION （6页）

| # | 页面 | 路径 | 用途 |
|---|------|------|------|
| 1 | Home | /index.html | Hero+能力概述+数据亮点+CTA |
| 2 | Capabilities | /capabilities/index.html | 技术参数+工艺能力+品质标准 |
| 3 | Quote | /quote/index.html | PCB估价系统（交互表单） |
| 4 | About | /about/index.html | 工厂+认证+QC+团队 |
| 5 | Contact | /contact/index.html | 表单+地址+FAQ |
| 6 | Blog | /blog/index.html | 博客框架（预留） |

## BLOCK MANIFEST

| Block | 用途 | 复用页面 |
|-------|------|----------|
| header | 全局导航 | 所有页面 |
| footer | 全局页尾 | 所有页面 |
| hero | 首页Hero | /index.html |
| sub-hero | 子页面Hero | /about, /capabilities, /quote, /contact |
| stats-bar | 数据亮点条 | /index.html, /about |
| cert-strip | 认证徽标滚动 | /index.html, /about, /capabilities |
| media-split | 图文分屏 | 多种页面 |
| card-grid | 卡片网格 | /index.html, /capabilities |
| tech-table | 技术参数表 | /capabilities |
| cta-card | CTA卡片 | /index.html, /capabilities, /about |
| modal-inquiry | 弹窗询盘 | 全局 |
| quote-form | 估价表单 | /quote |
| process-steps | 流程步骤 | /about |
| contact-form | 联系表单 | /contact |
| faq-accordion | FAQ手风琴 | /contact |

## IMAGE STRATEGY

总计 **30张** 图片：
- hero-bg: 1
- sub-hero-bg: 4
- product-showcase: 4
- technical-diagram: 3
- process-flow: 2
- concept-scene: 4
- texture-bg: 5
- stats-bg: 2
- cta-bg: 3
- blog-cover: 1
- comparison-chart: 1

详见 image-strategy.json

## IMAGE DIRECTION

- **统一调性**: 暗色调、金色高光、精密工业感
- **Prompt 通用词**: "dark atmospheric, gold-copper accent lighting, precision manufacturing, no people faces, no text, no logos"
- **生图格式**: 全部 1024×1024 WebP
- **质量**: low (¥0.006/张)
