# STATUS — Corporate Robotics Source Downloads

**Date:** 2026-10-10
**Source list:** `inbox/Corporate Robotics in 2025–2026  What Has Actually Been Built, Shipped, and Deployed.md`
**Destination:** `inbox/corporate/`
**Ingested:** no — downloads only, as requested. Nothing written to `wiki/`.

## Result

| | Count |
|---|---|
| Distinct URLs cited in the document | 90 |
| Downloaded successfully | ==78== |
| Permanently inaccessible (bot-walled) | **2** |
| Standing index / feed pages — nothing to ingest | 8 |
| Duplicate URL for an article already captured | 1 |
| Already held in `inbox/controversies/` | 1 |

On disk: **72 archived HTML pages + 6 PDFs**, plus **60 figure folders holding 539 images**.
Folder total ≈ 240 MB. `inbox/` is gitignored, so none of this enters the repo.

## What "ingestible" means here

| Source shape | Captured as |
|---|---|
| Web article / press release / company blog | One self-contained `.html` per page, scripts stripped, content figures mirrored into a sibling `<title>_figs/` folder with `src` rewritten to the local copy. Site chrome (logos, theme assets, icons) deliberately left pointing at its remote host. Each file opens with an `[Archived from <url>]` line. |
| PDF (IR decks, filings, arXiv papers) | Saved as `.pdf`, ready for `scripts/pdf2md`. Per CLAUDE.md, convert with `pdf2md` before reading — never `Read` the `.pdf` directly. |
| arXiv abstract page | Fetched as the PDF rather than the abstract page, so the full text is available. |

Filenames are the page's own title (from `og:title`, falling back to `<title>`), sanitized for Windows.

## Failures — 2 sources could not be retrieved

Both sit behind bot-detection walls (Akamai / Cloudflare) that reject automated clients regardless of headers:

| Source | Cited in | What was tried |
|---|---|---|
| Toyota Pressroom, "AI-Powered Robot by Boston Dynamics and TRI Takes a Key Step Towards General-Purpose Humanoids" | §1.1 Boston Dynamics, §2.3 Toyota/TRI | `requests` with browser headers → **HTTP 403**; curl with full Chrome header set (`sec-ch-ua`, `Sec-Fetch-*`, `Upgrade-Insecure-Requests`) → **403**; headless Chromium via Playwright → served a **403 Forbidden** page; Wayback Machine → **no snapshot exists**. |
| Forbes, Koetsier, "Humanoid Robot Shipments Up 300%, Up To 30,000 So Far In 2026" | §3.4 China Market Snapshot | Same four routes. Direct and curl → **403**; Playwright → Forbes' bot-wall stub; Wayback → **no snapshot**. |

> [!tip] Neither failure costs the document a fact
> The Toyota pressroom release is a press restatement of the Boston Dynamics engineering blog post and
> the TRI LBM paper, both captured (`Large Behavior Models and Atlas Find New Footing.html`,
> `A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation.html`).
> The Forbes piece reports the same Counterpoint H1-2026 shipment estimate carried by
> `Global humanoid robot shipments surge 300pc in H1, led by Agibot.html` (The Standard) and the
> IDC figure in `Humanoid robot shipments jump 432%…` (Yahoo Finance). If the Forbes framing is
> wanted verbatim, it needs a manual browser save.

## Not downloaded by design — 8 standing sources

The document's "Recommended Ongoing Sources" section and a few inline citations point at **feeds and index
pages rather than documents**. These have no fixed content to ingest — their value is that you revisit them —
so they were skipped rather than frozen into a snapshot that would be stale within a week:

`bostondynamics.com/blog/` · `english.sse.com.cn/` · `spectrum.ieee.org/tag/unitree` ·
`spectrum.ieee.org/topic/robotics/` · `hkexnews.hk/` · `therobotreport.com/` ·
`tri.global/publications` · `unitree.com/news/`

The specific articles cited *from* those outlets were all downloaded. The one genuinely-dated page in
that section — the IEEE RAS "Robots in Society" August 2026 column — was captured.

## Other handling notes

1. **Duplicate.** The Gasgoo Unitree-IPO article is cited twice under two paths (`/articles/news/…` and
   `/articles/icv/…`). Captured once.
2. **Already held.** arXiv:2507.05331 (TRI "A Careful Examination…") was downloaded during the §3.2
   controversy pass and lives in `inbox/controversies/`. Not duplicated here — it is a 46 MB file. The
   TRI *project page* for it is captured in `inbox/corporate/`, since the document cites that separately.
3. **Three files carry native-language titles**, because that is what their titles are: the Yaskawa
   Technical Report 2026 No.3 (Japanese), the Car Watch Toyota investment story (Japanese), and the
   News2Day LG physical-AI feature (Korean). Left as-is so the filename still matches the source.
4. **Two pages needed a real browser.** Pandaily (Remix app) and Chosun.com English (Fusion/React) return
   an empty shell to a plain HTTP client — their text is assembled client-side. Both were re-fetched by
   rendering in headless Chromium, which required `uv run --with playwright playwright install chromium`
   on this machine. Worth knowing for future ingests: a 200 response with a near-empty body means
   JS-rendered, not paywalled.
5. **Every captured page was length-checked** after download to catch paywall stubs and bot-wall pages
   masquerading as success. Minimum surviving body text is ~3.4 KB (`F.03 Arrives at BMW`, a genuinely
   short post); median ~10.9 KB. All 60 figure folders resolve — zero broken local image references.
6. **Paywall note.** The MIT Technology Review article captured here is the same one already in
   `inbox/controversies/`; it is duplicated across the two folders because both documents cite it.

## Full inventory

Grouped by the section of the source document that cites each URL. A URL cited in several sections is
listed under the first.

#### Executive Summary

| Status | File | Source |
|---|---|---|
| OK | `A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation.html` | https://toyotaresearchinstitute.github.io/lbm1/ |
| OK | `Large Behavior Models and Atlas Find New Footing.html` | https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/ |
| OK | `FANUC Financial Reference Materials FY2026 Q3.pdf` | https://www.fanuc.co.jp/en/ir/announce/pdf/2026/reference202512_e.pdf |
| OK | `Yaskawa Mid-Term Business Plan Briefing 2026.pdf` | https://www.yaskawa-global.com/wp-content/uploads/2026/06/IR2606_05en.pdf |
| OK | `Global humanoid robot shipments surge 300pc in H1, led by Agibot.html` | https://www.thestandard.com.hk/innovation/article/340494/Global-humanoid-robot-shipments-surge-300pc-in-H1-led-by-Agibot |
| OK | `China's Humanoid 'Mass-Production Year'_ The Gap Between Making Robots and Using Them.html` | https://pandaily.com/chinese-humanoid-mass-production |
| OK | `BMW Group advances the use of Physical AI in production with Figure 03 project in Spartanburg.html` | https://www.press.bmwgroup.com/global/article/detail/T0458778EN/bmw-group-advances-the-use-of-physical-ai-in-production-with-figure-03-project-in-spartanburg?language=en |
| OK | `Digit Moves Over 100,000 Totes in Commercial Deployment.html` | https://www.agilityrobotics.com/content/digit-moves-over-100k-totes |
| OK | `Tesla ramps Optimus to hundreds a week, but the robots can't generalize.html` | https://electrek.co/2026/09/25/tesla-optimus-production-ramp-hands-ai-generalization-problems/ |
| OK | `U.S. Bans New Foreign Mobile Robots.html` | https://spectrum.ieee.org/fcc-covered-list-mobile-robots |

#### 1.1 Boston Dynamics (Hyundai Motor Group)

| Status | File | Source |
|---|---|---|
| OK | `Boston Dynamics begins robotics testing at Hyundai, outlines expansion.html` | https://www.manufacturingdive.com/news/boston-dynamics-begins-robotics-testing-hyundai-atlas-humanoid/831000/ |
| **FAILED** | — | https://pressroom.toyota.com/ai-powered-robot-by-boston-dynamics-and-toyota-research-institute-takes-a-key-step-towards-general-purpose-humanoids/ |
| OK | `Atlas’ Training Secrets_ The Human Touch Behind the Robot.html` | https://spectrum.ieee.org/boston-dynamics-atlas-scott-kuindersma |
| OK | `New Video “Just Scratching the Surface” Of What Atlas Can Do.html` | https://spectrum.ieee.org/atlas-robot |
| OK | `Hello, Electric Atlas.html` | https://spectrum.ieee.org/atlas-humanoid-robot |
| OK | `Boston Dynamics and Toyota Research Team Up on Robots.html` | https://spectrum.ieee.org/boston-dynamics-toyota-research |
| OK | `Boston Dynamics Opens Robotics Metaplant Application Center to Train Humanoid Robots for Manufacturing Tasks.html` | https://bostondynamics.com/news/boston-dynamics-opens-robotics-metaplant-application-center-to-train-humanoid-robots-for-manufacturing-tasks/ |
| OK | `Boston Dynamics Unveils New Atlas Robot to Revolutionize Industry.html` | https://bostondynamics.com/blog/boston-dynamics-unveils-new-atlas-robot-to-revolutionize-industry/ |
| OK | `Hyundai Motor Group Announces AI Robotics Strategy to Lead Human-Centered Robotics Era at CES 2026.html` | https://www.hyundai.com/worldwide/en/newsroom/detail/hyundai-motor-group-announces-ai-robotics-strategy-to-lead-human-centered-robotics-era-at-ces-2026-0000001100 |
| OK | `Inside the Robotics Race_ Atlas Learns the Real World _ Journal.html` | https://www.hyundaimotorgroup.com/en/story/hyundai-motor-group-bloomberg-atlas-boston-dynamics-rmac |

#### 1.2 Tesla Optimus

| Status | File | Source |
|---|---|---|
| OK | `Tesla Optimus Archives.html` | https://electrek.co/guides/tesla-optimus/ |
| OK | `Tesla’s Optimus production is up tenfold but the robot hands lag.html` | https://thenextweb.com/news/tesla-optimus-production-hands-suppliers |
| OK | `AI breakthroughs in robotics won’t change your life any time soon.html` | https://www.technologyreview.com/2026/10/08/1145923/ai-breakthroughs-in-robotics-wont-change-your-life-any-time-soon/ |

#### 1.3 Figure AI (US reference point)

| Status | File | Source |
|---|---|---|
| OK | `Figure 02.html` | https://aiwiki.ai/wiki/figure_02 |
| OK | `F.03 Arrives at BMW.html` | https://www.figure.ai/news/f-03-at-bmw |

#### 1.4 Agility Robotics (US reference point)

| Status | File | Source |
|---|---|---|
| OK | `GXO Signs Industry-First Multi-Year Agreement with Agility Robotics.html` | https://www.agilityrobotics.com/content/gxo-signs-industry-first-multi-year-agreement-with-agility-robotics |
| OK | `Beyond the Hype.html` | https://www.agilityrobotics.com/content/beyond-the-hype |
| OK | `Agility and FORT Robotics Announce Strategic Partnership to Advance Humanoid Robot Safety.html` | https://www.agilityrobotics.com/content/agility-and-fort-robotics-announce-strategic-partnership-to-advance-humanoid-robot-safety |

#### 2.1 FANUC

| Status | File | Source |
|---|---|---|
| OK | `ROBOT New Technology_ Open Platforms & Physical AI - New Product - Products - FANUC CORPORATION.html` | https://www.fanuc.co.jp/en/product/new_product/2025/202512_robot_physicalai.html |
| OK | `iREX 2025_ From programmed to perceptive - The Robot Report.html` | https://www.therobotreport.com/irex-2025-from-programmed-perceptive/ |
| OK | `International Robot Exhibition 2025 - FANUC News - FANUC CORPORATION.html` | https://www.fanuc.co.jp/en/profile/news/article/article26.html |
| OK | `FANUC and Fujitsu Commence Discussions on Business Collaboration for the Real-World Deployment of Physical AI.html` | https://www.fanuc.co.jp/en/profile/pr/newsrelease/2026/notice20260716.html |

#### 2.2 Yaskawa

| Status | File | Source |
|---|---|---|
| OK | `MOTOMAN NEXT - Komplettlösung für adaptive Robotikautomation.html` | https://www.yaskawa.de/robotik/motoman-next |
| OK | `テクニカルレポート 2026 No.3 人手に依存した作業領域の自動化に挑むAIロボティクス ～AIロボットMOTOMAN NEXT活用事例の紹介～ _ テクニカルレポート _ テクノロジー.html` | https://www.yaskawa.co.jp/technology/technical-report/detail260623 |
| OK | `MOTOMAN NEXT AI Robot’s Agentic Robot System Powered by Gemini Robotics _ Category_ News.html` | https://www.yaskawa-global.com/newsrelease/news/179679 |

#### 2.3 Toyota / Toyota Research Institute (TRI)

| Status | File | Source |
|---|---|---|
| already held | `inbox/controversies/A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation.pdf` | https://arxiv.org/abs/2507.05331 |
| OK | `トヨタ、毎年1兆円を投資し工場とロボットを更新 40万台をフィジカルAIであるLarge Behavior Models搭載ロボなどに.html` | https://car.watch.impress.co.jp/docs/news/2142008.html |
| OK | `Samsung to Expand 'Humanoid Alliance' with Toyota…Robot Supply Up 5x.html` | https://en.etnews.com/20260707200002 |

#### 2.4 Fujitsu

| Status | File | Source |
|---|---|---|
| OK | `Fujitsu to explore physical AI development and implementation across industries with FANUC, Yaskawa Electric,.html` | https://global.fujitsu/en-global/pr/news/2026/07/16-01 |
| OK | `Towards the Social Implementation of Physical AI_ The “Shared Future” Envisioned by Five Leaders Shaping the W.html` | https://note.com/fujitsu_pr/n/nc2be466ac140?hl=en |
| OK | `Fujitsu, CMU Launch Joint Center for Physical AI.html` | https://www.cs.cmu.edu/news/2026/cmu-fujitsu-physical-ai-center |
| OK | `Fujitsu Technology Strategy 2026.pdf` | https://global.fujitsu/-/media/Project/Fujitsu/Fujitsu-HQ/pr/news/2026/04/23-01/news-20260423-01b-en.pdf?rev=913f642effeb4afe94514953246b0468&hash=B62F9571B5A962B7D354AA532A0B3505 |
| OK | `Fujitsu IR Day 2026 - Technology Strategy.pdf` | https://resources.global.fujitsu/prir/2026/09/2026-IRDay-02-en.pdf |

#### 3.1 Unitree Robotics (Hangzhou; STAR Market 688836.SH)

| Status | File | Source |
|---|---|---|
| OK | `China Daily _ Unitree IPO draws spotlight to China's fast-growing humanoid robot sector.html` | https://english.sse.com.cn/news/newsrelease/voice/c/c_20260811_10828578.shtml |
| OK | `Global Times _ Shanghai Stock Exchange to review Unitree Robotics IPO on June 1, with over 4.2 billion yuan fu.html` | https://english.sse.com.cn/news/newsrelease/voice/c/c_20260526_10819716.shtml |
| OK | `What Unitree's filing actually says about humanoid robots.html` | https://www.insidedeeptech.com/unitree-humanoid-robot-filing/ |
| OK | `Unitree Profits, but Humanoid Robots Fail to Make Money.html` | https://eu.36kr.com/en/p/3735276262601477 |
| OK | `Unitree's IPO_ The Absence of a VisiCalc.html` | https://eu.36kr.com/en/p/3825497010229890 |
| OK | `Unitree Wins IPO Approval as Robot Makers Face Tougher Profit Challenges.html` | https://autonews.gasgoo.com/articles/news/unitree-wins-ipo-approval-as-robot-makers-face-tougher-profit-challenges-2061816669448765440 |
| duplicate | same article, already captured | https://autonews.gasgoo.com/articles/icv/unitree-wins-ipo-approval-as-robot-makers-face-tougher-profit-challenges-2061816669448765440 |
| not a document | standing index / feed page — see note 3 | https://spectrum.ieee.org/tag/unitree |
| not a document | standing index / feed page — see note 3 | https://www.unitree.com/news/ |
| OK | `Unitree Robotics files for $610 million IPO as humanoid robot sales surge.html` | https://roboticsandautomationnews.com/2026/03/31/unitree-robotics-files-for-610-million-ipo-as-humanoid-robot-sales-surge/100272/ |
| OK | `Will Robotics Have a ChatGPT Moment.html` | https://spectrum.ieee.org/robotics-ai-breakthrough |
| OK | `The Robots Cometh.html` | https://time.com/article/2026/07/23/unitree-china-human-robotics/ |

#### 3.2 UBTech Robotics (Shenzhen; HKEX 9880)

| Status | File | Source |
|---|---|---|
| OK | `UBTech Robotics 2026 Interim Report.pdf` | https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0924/2026092401451.pdf |
| OK | `UBTech’s full-size humanoid robot revenue jumps 1,445% in H1 2026.html` | https://kr-asia.com/ubtechs-full-size-humanoid-robot-revenue-jumps-1445-in-h1-2026 |
| OK | `UBTECH Robotics - Company Profile, Milestones & Funding.html` | https://www.ventureatlas.org/company/ubtech-robotics |
| OK | `China’s UBTECH Launched Factory Capable of Producing Humanoid Robot Every 10 Minutes.html` | https://militarnyi.com/en/news/china-ubtech-factory-humanoid-robot-10-mins/ |
| OK | `UBTECH Robotics.html` | https://www.humanoidsdaily.com/companies/ubtech-robotics |

#### 3.3 AgiBot (Zhiyuan; Shanghai)

| Status | File | Source |
|---|---|---|
| OK | `AgiBot World Colosseo - A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems.pdf` | https://arxiv.org/abs/2503.06669 |
| OK | `Humanoid Robot Shipments Jump 432%, China Has 95% Market Share.html` | https://finance.yahoo.com/technology/ai/articles/humanoid-robot-shipments-jump-432-025835160.html |
| OK | `AGIBOT and Chimelong Launch Large-Scale Embodied AI Theme Park with More Than 300 Robots.html` | https://www.prnewswire.com/apac/news-releases/agibot-and-chimelong-launch-large-scale-embodied-ai-theme-park-with-more-than-300-robots-302888863.html |
| OK | `AGIBOT Has Built 20,000 Robots.html` | https://www.humanoidsdaily.com/news/agibot-20000-robots-production-milestone |
| OK | `AgiBot.html` | https://www.robonaissance.com/p/inside-chinas-machine-agibot |

#### 3.4 China Market Snapshot

| Status | File | Source |
|---|---|---|
| **FAILED** | — | https://www.forbes.com/sites/johnkoetsier/2026/08/20/humanoid-robot-shipments-up-300-up-to-30000-so-far-in-2026/ |
| OK | `The US is building barriers around drones and robots, but China has scale to get around them.html` | https://techcrunch.com/2026/08/30/the-u-s-is-building-barriers-around-drones-and-robots-china-still-has-scale/ |
| OK | `From boxing to folding shirts_ China’s humanoid robot boom faces real-world test.html` | https://www.straitstimes.com/asia/east-asia/from-boxing-to-folding-shirts-chinas-humanoid-robot-boom-faces-real-world-test?ref=latest-headlines |

#### 4.1 Samsung Electronics and Rainbow Robotics

| Status | File | Source |
|---|---|---|
| OK | `Humanoid enters first commercial warehouse trial in South Korea.html` | https://interestingengineering.com/ai-robotics/samsung-backed-robot-enters-coupang-warehouse |
| OK | `iM Securities backs Rainbow Robotics as key Samsung humanoid partner in Korea.html` | https://biz.chosun.com/en/en-finance/2026/08/19/TJYGBH3GWFBFTPKAS6RCGYKUNU/ |
| OK | `Humanoid Robots Assist Surgeon in World-First Team Surgery.html` | https://www.chosun.com/english/national-en/2026/09/18/3KOXERFXP5E7XJ3LX345MG5YDE/ |
| OK | `[Edaily] “From Factory Automation to the Home”… Samsung Unveils Roadmap for Commercializing ‘Robots’.html` | https://rainbow-robotics.com/edaily-from-factory-automation-to-the-home-samsung-unveils-roadmap-for-commercializing-robots/ |
| OK | `Samsung Aims to Unveil First Humanoid Robot at CES 2027.html` | https://en.sedaily.com/finance/2026/09/07/samsung-to-unveil-first-humanoid-robot-at-ces-2027 |

#### 4.3 LG Electronics

| Status | File | Source |
|---|---|---|
| OK | `LG Electronics Presents LG ClOiD Home Robot To Demonstrate “Zero Labor Home” at CES 2026.html` | https://www.lg.com/global/newsroom/news/home-appliance-solution/lg-electronics-presents-lg-cloid-home-robot-to-demonstrate-zero-labor-home-at-ces-2026/ |
| OK | `Physical AI transforms Korea industry and homes with ready-to-launch devices.html` | https://biz.chosun.com/en/en-it/2026/01/10/BFYLKSS4TRHP3HS5HAUIZ4EUGY/?outputType=amp |
| OK | `[전기차 전환을 넘어 모빌리티 혁명으로 (12)] LG그룹, 근육에서 두뇌까지.. 피지컬 AI 주도권 잡기 위해 박차(上).html` | https://www.news2day.co.kr/article/20260530500020 |

#### 4.4 Doosan Robotics

| Status | File | Source |
|---|---|---|
| OK | `South Korea brings AI into the physical world at CES 2026.html` | https://www.thedailystar.net/business/news/south-korea-brings-ai-physical-world-ces-2026-4076141 |

#### Part 5 — The US Regulatory Backdrop

| Status | File | Source |
|---|---|---|
| OK | `FCC Updates Covered List to Include Foreign-Produced Advanced Robotic Devices and Power Inverters on National.html` | https://www.skadden.com/insights/publications/2026/08/fcc-updates-covered-list-to-include-foreign-produced-advanced-robotic-devices |
| OK | `FCC Adds All Foreign-Produced Advanced Robotic Devices to the Covered List _ Insights.html` | https://www.sidley.com/en/insights/newsupdates/2026/08/fcc-adds-all-foreign-produced-advanced-robotic-devices-to-the-covered-list |
| OK | `Foreign-Produced Advanced Robotic Devices and Certain Foreign-Produced Power Inverters Added to FCC Covered Li.html` | https://www.kirkland.com/publications/kirkland-alert/2026/08/foreign-produced-advanced-robotic-devices-and-certain-foreign-produced-power-inverters-added |
| OK | `FCC Restrictions on Foreign-Produced Advanced Robotic Devices.html` | https://ifr.org/ifr-press-releases/news/fcc-restrictions-on-foreign-produced-advanced-robotic-devices |

#### Recommended Ongoing Sources

| Status | File | Source |
|---|---|---|
| not a document | standing index / feed page — see note 3 | https://spectrum.ieee.org/topic/robotics/ |
| not a document | standing index / feed page — see note 3 | https://www.therobotreport.com/ |
| OK | `Robots in Society, Business and Culture_ August 2026 - IEEE Robotics and Automation Society Website.html` | https://www.ieee-ras.org/robots-in-society-business-and-culture-august-2026/ |
| not a document | standing index / feed page — see note 3 | https://www.hkexnews.hk/ |
| not a document | standing index / feed page — see note 3 | https://english.sse.com.cn/ |
| not a document | standing index / feed page — see note 3 | https://www.tri.global/publications |
| not a document | standing index / feed page — see note 3 | https://bostondynamics.com/blog/ |
| OK | `Gemini Robotics 2 brings whole body intelligence to robots.html` | https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/ |
| OK | `A Steerable Model with Emergent Capabilities.html` | https://www.pi.website/blog/pi07 |

