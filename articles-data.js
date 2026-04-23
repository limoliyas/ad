window.ARTICLE_ITEMS = [
  {
    category: "Tech",
    date: "Apr 23",
    read: "9 min",
    titleEn: "Inside a Real AI Copilot Rollout: How a 2,000-Person Team Reworked Daily Operations",
    titleZh: "一家 2000 人公司的 AI Copilot 落地实录：他们如何重做日常运营流程",
    summaryEn:
      "A cross-functional program moved from pilot chaos to measurable gains by redesigning workflow ownership, review paths, and model governance.",
    summaryZh: "一个跨部门项目从试点混乱走向可衡量收益，关键在于重新定义流程归属、复核路径和模型治理机制。",
    bodyEn: [
      "The company did not start by buying a new model. It started by mapping work that repeatedly delayed teams: drafting customer replies, summarizing meetings, and preparing routine reports. Leaders asked each department to nominate one process owner and one reviewer before any AI feature went live.",
      "In the first month, most failures were not model hallucinations but process gaps. Drafts were generated faster, but reviewers still used old approval routes and duplicated edits in three systems. The turnaround time improved only 6%, far below the internal target.",
      "The second phase focused on workflow redesign. The team added structured prompts tied to ticket types, required evidence links for every generated claim, and pushed all drafts into a single review queue. This reduced back-and-forth coordination and made quality defects visible by category.",
      "By month three, median handling time for standard support cases dropped from 19 minutes to 11 minutes. Report preparation time for weekly ops reviews fell by 38%. More importantly, managers could trace exactly where AI helped and where human judgment still dominated.",
      "The lesson was simple: AI adoption scaled only after operational roles became explicit. The model was a component, not the operating system. Teams that treated deployment as org design work delivered durable results.",
      "For companies planning similar programs, the most useful KPI was not raw productivity. It was review-loop stability: how many AI outputs reached final delivery with one review pass. That number became the clearest signal of maturity."
    ],
    bodyZh: [
      "这家公司并不是先买模型，而是先盘点真正反复拖慢团队的工作：客服回复起草、会议纪要整理、例行报告编写。管理层要求每个部门在 AI 功能上线前，必须明确一位流程负责人和一位复核负责人。",
      "第一个月的问题并非主要来自“幻觉”，而是流程断层。草稿生成确实更快，但复核仍走旧审批链路，且在三个系统中重复修改，最终整体时效只提升了 6%，远低于预期。",
      "第二阶段的重点转向流程重构：按工单类型绑定结构化提示词；对每条生成结论强制附证据链接；把所有草稿统一进入一个复核队列。这样既减少了跨组反复沟通，也让质量缺陷能按类型被追踪。",
      "到第三个月，标准客服工单的中位处理时长从 19 分钟降到 11 分钟，周度运营报告准备时间下降 38%。更关键的是，管理者能清楚看到 AI 在哪一段产生价值、哪一段仍必须依赖人工判断。",
      "这次落地最核心的经验是：只有当组织角色和责任边界先清晰，AI 才能规模化。模型是流程组件，不是整个运营系统。把部署当作组织设计工程去做，结果才可持续。",
      "对准备推进同类项目的团队来说，最有用的 KPI 不是“总产出”，而是“单轮复核通过率”：一份 AI 产出能否在一次复核后直接进入交付。这项指标最能反映落地成熟度。"
    ],
    videoCard: {
      href: "https://vids.st/v/23670",
      titleEn: "Watch rollout case breakdown",
      titleZh: "查看落地案例拆解视频"
    }
  },
  {
    category: "Tech",
    date: "Apr 22",
    read: "8 min",
    titleEn: "RAG Is Growing Up: Why Retrieval Quality Beats Model Size in Production",
    titleZh: "RAG 正在进入成熟期：在线上场景里，检索质量往往比模型规模更关键",
    summaryEn:
      "Teams that tuned chunking, metadata, and freshness signals outperformed larger-model deployments with weaker retrieval foundations.",
    summaryZh: "实践显示，优先优化切片、元数据和时效信号的团队，往往比“只上更大模型”的方案更稳定。",
    bodyEn: [
      "A common enterprise pattern is to upgrade models when answer quality drops. In many audits, however, the root cause is retrieval noise: stale pages, duplicated chunks, and missing access controls that pollute the context before generation even begins.",
      "One infrastructure team compared two paths for its internal assistant. Path A used a larger model with unchanged indexing. Path B kept the same model but rebuilt the retrieval stack with semantic chunking, stricter source tags, and freshness scoring. Path B delivered better factual accuracy and lower token spend.",
      "The strongest gain came from metadata discipline. Documents were labeled by owner, lifecycle stage, and confidence level. Queries that previously returned mixed draft and final content now filtered by publication state, reducing contradictory answers.",
      "Latency also improved. Instead of sending broad context windows, the system passed fewer but higher-confidence snippets. Response times became more predictable, and reviewers reported less time spent checking irrelevant passages.",
      "The takeaway is practical: model choice still matters, but retrieval architecture is where reliability is won. If teams cannot explain why each context chunk was selected, they are unlikely to achieve trustworthy AI search at scale."
    ],
    bodyZh: [
      "很多企业在答案质量下降时，第一反应是升级模型。但在大量复盘中，真正的根因常常是检索噪声：过期文档、重复切片、权限混入，问题在生成前就已经发生。",
      "某基础设施团队对内部助手做了 A/B 路径对比：A 路径是换更大模型但索引不变；B 路径保持模型不变，重建检索层，包括语义切片、严格来源标签和时效评分。结果 B 路径在事实准确率与 token 成本上都更优。",
      "提升最大的一环来自元数据治理。文档被统一标注负责团队、生命周期阶段和可信等级。过去经常把草稿与正式版混合返回，现在可以按发布状态过滤，明显减少互相矛盾的回答。",
      "延迟表现也随之改善。系统不再传入冗长上下文，而是只发送更少但更高置信度的片段，响应时延更可预测，审核人员用于排除无关内容的时间显著下降。",
      "结论很务实：模型当然重要，但线上可靠性更多取决于检索架构。如果团队无法解释“每个上下文片段为什么被选中”，就很难把 AI 搜索做成可规模化的可信产品。"
    ],
    videoCard: {
      href: "https://vids.st/v/23671",
      titleEn: "Watch RAG architecture briefing",
      titleZh: "查看 RAG 架构解读视频"
    }
  },
  {
    category: "Tech",
    date: "Apr 21",
    read: "7 min",
    titleEn: "From Prompt Engineering to Prompt Operations: The New Work of AI Teams",
    titleZh: "从 Prompt Engineering 到 Prompt Operations：AI 团队的新日常",
    summaryEn:
      "Prompt quality now depends less on individual craft and more on versioning, evaluation gates, and controlled rollout discipline.",
    summaryZh: "提示词质量越来越不是“个人技巧”问题，而是版本管理、评测门禁和发布纪律的问题。",
    bodyEn: [
      "In early deployments, a few specialists wrote prompts and shared them in docs. That approach breaks once dozens of teams depend on consistent output. Small edits can silently change downstream behavior and create regression risks.",
      "Mature organizations now run prompt changes like application releases. Every update receives an owner, a test set, and a rollback path. Teams compare quality metrics before and after release, rather than relying on anecdotal feedback.",
      "A product support group introduced prompt version tags in every generated draft. When quality incidents occurred, analysts could quickly map failures to specific prompt revisions and restore the previous stable version within minutes.",
      "Evaluation design became a competitive edge. Instead of asking whether output was generally good, reviewers scored factual grounding, policy compliance, and actionability separately. This produced clearer trade-off decisions during tuning.",
      "The shift from prompt engineering to prompt operations reflects a deeper reality: sustainable AI systems need governance around language behavior, not just stronger models."
    ],
    bodyZh: [
      "在早期阶段，通常由少数专家写提示词并在文档里共享。但当几十个团队依赖同一套输出标准时，这种方式会迅速失效。一次看似轻微的修改，可能在下游引发不可见的行为回归。",
      "成熟组织开始把提示词更新当成正式发布流程来管理。每次变更都必须有负责人、评测集和回滚方案，发布前后对比量化指标，而不是只听“感觉变好了”。",
      "某产品支持团队在每份 AI 草稿里附带提示词版本标签。出现质量事故时，分析人员可以快速定位到具体版本，并在几分钟内回退到稳定版本，避免影响持续扩大。",
      "评测方法本身也成为核心能力。团队不再笼统判断“好不好”，而是把事实依据、合规性和可执行性分开打分，这让调优决策更清晰，取舍更透明。",
      "从 Prompt Engineering 走向 Prompt Operations，本质上说明一件事：可持续的 AI 系统需要“语言行为治理”，而不只是更大的模型。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 20",
    read: "8 min",
    titleEn: "Can Smaller Models Win? What 6 Production Benchmarks Reveal",
    titleZh: "小模型能赢吗？6 个生产基准给出的真实答案",
    summaryEn:
      "Across constrained business tasks, tuned small models matched or exceeded larger models on cost-adjusted throughput and response consistency.",
    summaryZh: "在边界明确的业务任务中，经过优化的小模型在成本效率和响应一致性上经常不输大模型。",
    bodyEn: [
      "A multi-team benchmark across customer support, data labeling, and policy drafting tested model sizes under identical workflow constraints. The result challenged a common assumption: larger models were not automatically better for operational tasks.",
      "For repetitive classification and extraction jobs, smaller models with domain-tuned prompts achieved similar accuracy with significantly lower latency. The difference became meaningful when queues spiked during peak business hours.",
      "Large models still led in ambiguous reasoning and long-context synthesis. But in day-to-day pipelines, most requests were short, templated, and repetitive. Under those conditions, predictability mattered more than peak reasoning ability.",
      "Teams that adopted model routing gained the best outcome: small models handled baseline traffic, while complex exceptions were escalated to larger models. This preserved quality without paying high inference cost for every request.",
      "The strategic implication is not to choose one model forever. It is to build an execution layer that can assign the right model to the right job in real time."
    ],
    bodyZh: [
      "一次覆盖客服、数据标注和政策文档起草的多团队基准测试，在统一流程约束下比较了不同模型规模。结果挑战了一个常见认知：在线上运营任务中，大模型并不总是更优。",
      "在重复性的分类与抽取任务中，使用领域化提示词的小模型能达到接近精度，但延迟更低。这在业务高峰时段尤为关键，因为排队时间会被成倍放大。",
      "大模型在复杂推理和长上下文综合上仍有优势，但日常请求多数是短文本、模板化、重复性高的任务。在这种条件下，可预测性往往比峰值能力更重要。",
      "表现最好的方案通常是“模型路由”：小模型承接主流流量，复杂异常再升级给大模型。这样既保留质量，又避免为每个请求都支付高推理成本。",
      "真正的策略并非永久绑定某个模型，而是构建一层可实时分配任务的执行系统，让“合适的模型处理合适的问题”。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 19",
    read: "8 min",
    titleEn: "The Hidden Bottleneck in AI Projects Is Data Contracts, Not GPUs",
    titleZh: "AI 项目真正的隐性瓶颈常常不是 GPU，而是数据契约",
    summaryEn:
      "Projects stalled when source systems lacked stable field definitions, ownership, and change notifications required for reliable AI pipelines.",
    summaryZh: "许多项目卡在数据源字段定义不稳定、归属不清、变更无通知，导致 AI 流水线无法可靠运行。",
    bodyEn: [
      "Executives often ask whether they have enough GPU capacity. Engineering teams increasingly ask a different question: can we trust the fields arriving from upstream systems tomorrow to look like they do today?",
      "In one enterprise migration, a customer intent classifier degraded twice in six weeks because source schemas changed without notice. The model was unchanged; the data contract was not.",
      "Teams that formalized data contracts cut recovery time dramatically. Every source field had an owner, validation rules, and expected update cadence. Breaking changes triggered alerts before they hit production inference.",
      "This discipline also improved collaboration. Product teams could plan feature updates with clearer dependency maps, and operations teams spent less time firefighting mysterious output shifts.",
      "As AI systems become embedded in core workflows, reliability depends on stable interfaces between data producers and AI consumers. Compute scale helps, but contract discipline keeps systems alive."
    ],
    bodyZh: [
      "管理层常问的问题是“GPU 够不够”，而工程团队越来越常问的是：上游系统明天给我的字段，是否还能保持今天的结构和语义。",
      "在一个企业迁移项目中，客户意图分类器在六周内两次明显退化，原因都不是模型变化，而是源系统在未通知情况下调整了数据结构。",
      "把数据契约制度化后，恢复效率显著提升。每个字段都明确责任人、校验规则和更新节奏；一旦发生破坏性变更，会在进入线上推理前被告警拦截。",
      "这种纪律也改善了协作关系。产品团队能在更清晰的依赖图下规划功能，运维团队用于“救火排障”的时间明显减少。",
      "当 AI 深度进入核心流程，系统可靠性更依赖数据生产者与 AI 使用者之间的接口稳定性。算力扩容重要，但契约治理才是长期可用性的底盘。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 18",
    read: "7 min",
    titleEn: "Why AI Incident Response Needs Its Own On-Call Playbook",
    titleZh: "为什么 AI 事故响应需要一套独立的值班手册",
    summaryEn:
      "Traditional SRE alerts miss language-quality failures; mature teams now combine system signals with content-risk monitoring.",
    summaryZh: "传统 SRE 告警无法覆盖语言质量风险，成熟团队正在把系统指标与内容风险监控一起纳入值班体系。",
    bodyEn: [
      "An AI product can remain fully available while quietly producing unsafe or low-quality output. This makes incident detection fundamentally different from conventional uptime monitoring.",
      "Leading teams define dual alert channels: system reliability signals such as latency and error rate, plus language quality signals like policy violations, unsupported claims, and response drift.",
      "A consumer platform described a high-severity event where infrastructure stayed green while generated advice quality dropped for a specific user segment. The issue was caught only because reviewers tracked semantic regression samples in near real time.",
      "Their new playbook now includes containment actions beyond traffic routing: freeze prompt updates, lower model temperature, tighten retrieval sources, and switch risky intents to human-only handling.",
      "AI incident response is no longer a niche practice. As language systems move into customer-facing operations, it becomes a core reliability function."
    ],
    bodyZh: [
      "一个 AI 产品可以在“服务可用”状态下持续输出低质量甚至高风险内容，这使事故发现机制与传统可用性监控存在本质差异。",
      "领先团队通常建立双通道告警：一条监控时延、错误率等系统指标；另一条监控策略违规、无依据断言、语义漂移等内容质量信号。",
      "某消费平台曾出现一次高优先级事故：基础设施指标全部正常，但特定用户群体的生成建议质量明显下降。问题最终是靠近实时语义抽检才被发现。",
      "他们的新手册不只包含流量切换，还加入了内容侧遏制动作：冻结提示词变更、降低采样温度、收紧检索来源、对高风险意图临时切回人工处理。",
      "AI 事故响应已经不是小众能力。随着语言系统进入客户触点，它正在成为平台可靠性体系的核心组成部分。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 17",
    read: "9 min",
    titleEn: "Building Trustworthy AI Metrics: Beyond Accuracy and Cost",
    titleZh: "构建可被信任的 AI 指标体系：不止看准确率与成本",
    summaryEn:
      "Operators are adding calibration, citation verifiability, and handoff friction to measure whether AI systems are truly usable in business settings.",
    summaryZh: "一线团队开始引入校准度、引用可验证性和交接摩擦等指标，判断 AI 是否真的“可用、可管、可交付”。",
    bodyEn: [
      "Accuracy and unit cost remain important, but they do not capture whether teams can safely rely on AI outputs in real workflows. Many organizations now track confidence calibration: when the model sounds certain, is it actually correct?",
      "Citation verifiability is another emerging metric. Reviewers score whether claims can be traced to accessible, current, and policy-compliant sources. Answers without verifiable grounding are treated as higher operational risk.",
      "Some companies also measure handoff friction: how much editing a human must do before output can be shipped. This connects language quality directly to labor cost, making improvement priorities easier to justify.",
      "In quarterly reviews, teams that reported these operational metrics made better roadmap decisions than teams that reported only benchmark scores. They could identify where trust failed, not just where models performed in isolation.",
      "The next phase of AI evaluation is therefore managerial, not purely technical. The winning metric stack is the one that aligns model behavior with accountability and delivery outcomes."
    ],
    bodyZh: [
      "准确率和单位成本依然重要，但它们并不能完整回答一个问题：团队能否在真实流程中安全依赖 AI 产出。越来越多组织开始跟踪“校准度”：模型说得越笃定，是否真的越正确。",
      "“引用可验证性”也正在成为关键指标。评审会检查结论是否可追溯到可访问、时效可接受且合规的来源；无法验证依据的回答会被定义为更高运营风险。",
      "部分公司还引入“交接摩擦”指标，即人工在交付前需要改动多少内容。这个指标把语言质量直接映射到人力成本，使优化优先级更容易被业务团队接受。",
      "在季度复盘中，能够持续报告这些运营型指标的团队，路线决策通常优于只报离线基准分数的团队，因为他们看到了“信任在哪里断裂”，而不是只看到模型单点性能。",
      "AI 评测的下一阶段因此更偏管理科学，而不只是模型科学。真正有效的指标体系，是能把模型行为与责任机制、交付结果对齐的那一套。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 16",
    read: "8 min",
    titleEn: "How AI Changed Product Review Meetings Without Replacing Product Managers",
    titleZh: "AI 如何改变产品评审会议，而不是取代产品经理",
    summaryEn:
      "Teams using meeting copilots reduced prep overhead, but final prioritization still depended on human trade-off judgment.",
    summaryZh: "会议 Copilot 显著减少了准备成本，但最终优先级取舍仍然依赖产品经理的业务判断。",
    bodyEn: [
      "Before introducing AI copilots, product review meetings often consumed hours in status collection and document alignment. Most of that effort was repetitive and weakly differentiated.",
      "After deployment, teams used AI to pre-compile issue clusters, summarize experiment outcomes, and draft decision logs. Meeting time shifted from information gathering to decision discussion.",
      "However, the hardest work did not disappear. Product managers still had to balance contradictory constraints: growth targets, engineering capacity, compliance obligations, and long-term architecture health.",
      "One director described the new rhythm as amplification, not automation. AI compressed the pre-work, but strategic trade-offs still required context that no model could fully infer from artifacts alone.",
      "The practical conclusion is balanced: AI can substantially raise decision velocity, yet product leadership remains a human coordination role anchored in judgment and accountability."
    ],
    bodyZh: [
      "在引入会议 Copilot 前，产品评审常把大量时间花在状态汇总和材料对齐上，这些工作重复性高、差异化价值低。",
      "上线后，团队用 AI 预先聚类问题、汇总实验结果、草拟决策纪要，会议重心从“收集信息”转向“讨论取舍”。",
      "但最难的部分并没有消失。产品经理仍要在增长目标、研发产能、合规约束与架构健康之间做冲突平衡。",
      "一位产品总监把这种变化总结为“放大而非替代”：AI 压缩了会前准备时间，但战略取舍仍依赖跨业务语境的判断，不能只靠模型从文档里自动推断。",
      "更现实的结论是：AI 可以显著提升决策速度，但产品领导力依旧是一种以责任与判断为核心的人类协同能力。"
    ]
  }
];
