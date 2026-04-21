const MODEL_PRICING = [
  {
    id: "gpt-5.4",
    name: "GPT-5.4",
    inputPer1M: 8.0,
    outputPer1M: 24.0
  },
  {
    id: "gpt-5.4-mini",
    name: "GPT-5.4 Mini",
    inputPer1M: 1.2,
    outputPer1M: 4.8
  },
  {
    id: "gpt-5.2",
    name: "GPT-5.2",
    inputPer1M: 5.0,
    outputPer1M: 15.0
  },
  {
    id: "gpt-4o",
    name: "GPT-4o",
    inputPer1M: 5.0,
    outputPer1M: 15.0
  }
];

const ARTICLE_ITEMS = [
  {
    category: "Tech",
    date: "Apr 21",
    read: "6 min",
    titleEn: "AI Agents Move from Demos to Daily Operations",
    titleZh: "AI Agent 从演示走向日常业务执行",
    summaryEn:
      "Enterprise teams are embedding agents into support, reporting, and QA workflows with measurable cost and cycle-time gains.",
    summaryZh: "企业团队正在把 Agent 嵌入客服、报表与测试流程，成本和交付周期出现可量化改善。",
    bodyEn: [
      "AI agent deployment is shifting from innovation labs to production workflows. Teams now treat agents as process components with measurable SLAs.",
      "The most successful rollouts narrow scope first, then scale through clear guardrails, human review checkpoints, and performance instrumentation."
    ],
    bodyZh: [
      "AI Agent 正从创新试点进入生产流程，团队开始把它当作有 SLA 的流程组件，而非一次性演示工具。",
      "落地效果最好的路径通常是先缩小场景边界，再通过人工复核、规则护栏和性能监控逐步扩展。"
    ]
  },
  {
    category: "Finance",
    date: "Apr 21",
    read: "5 min",
    titleEn: "High-Rate Era Rewrites Startup Burn Models",
    titleZh: "高利率周期正在重写创业公司的烧钱模型",
    summaryEn:
      "Boards now prioritize runway quality and margin durability over pure top-line acceleration.",
    summaryZh: "董事会开始把现金流质量和利润韧性放在纯增长之前。",
    bodyEn: [
      "Capital efficiency has become a board-level discipline. Financing narratives now require downside resilience, not only growth projections.",
      "Startups that connect unit economics with realistic funding assumptions are outperforming peers in late-stage fundraising."
    ],
    bodyZh: [
      "资本效率已经变成董事会级别的经营纪律，融资叙事不再只看增长曲线，也看下行场景韧性。",
      "能把单元经济模型和真实融资环境打通的公司，在后期融资中明显更占优。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 20",
    read: "7 min",
    titleEn: "GPU Supply Is Easing, but Power Constraints Replace It",
    titleZh: "GPU 供给在缓解，但电力约束成为新瓶颈",
    summaryEn:
      "Data center expansion is increasingly blocked by grid timelines, not by chip shipments.",
    summaryZh: "数据中心扩容越来越受制于电网接入周期，而不再只是芯片到货。",
    bodyEn: [
      "Procurement pressure on accelerators is easing, yet deployment timelines still slip due to interconnection approvals and utility upgrades.",
      "Compute strategy now includes energy planning, with operators prioritizing locations that can provide predictable power expansion."
    ],
    bodyZh: [
      "加速卡采购压力正在缓解，但机房上线仍常因并网审批和电力改造而延后。",
      "算力布局策略正在并入能源规划，运营方更倾向优先选择具备稳定扩电能力的区域。"
    ]
  },
  {
    category: "Finance",
    date: "Apr 20",
    read: "6 min",
    titleEn: "Tokenized Treasury Products Enter Corporate Pilots",
    titleZh: "代币化国债产品进入企业资金试点阶段",
    summaryEn:
      "Treasury teams test 24/7 liquidity rails while keeping conservative risk controls.",
    summaryZh: "财资团队在保守风控前提下尝试 7x24 的流动性管理路径。",
    bodyEn: [
      "Corporate treasury pilots focus on settlement speed and transparency rather than speculative return.",
      "Adoption remains bounded by custody controls, accounting clarity, and redemption reliability into traditional banking rails."
    ],
    bodyZh: [
      "企业财资试点关注点主要是结算效率和透明度，而不是投机收益。",
      "规模化采用仍取决于托管安全、会计口径清晰度以及回到传统银行通道的赎回稳定性。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 19",
    read: "5 min",
    titleEn: "Cybersecurity Budgets Shift to Identity and Runtime",
    titleZh: "网络安全预算转向身份与运行时防护",
    summaryEn:
      "Organizations consolidate overlapping tools and invest in faster response orchestration.",
    summaryZh: "组织正在整合重复安全工具，并把预算投向更快的响应编排。",
    bodyEn: [
      "Identity telemetry provides the most persistent security signal across hybrid environments.",
      "Security teams are prioritizing runtime detection and automated response playbooks to reduce mean-time-to-contain."
    ],
    bodyZh: [
      "在混合架构下，身份行为数据已成为最稳定、最可持续的安全信号来源。",
      "安全团队将预算进一步转向运行时检测和自动化响应编排，以缩短事件收敛时间。"
    ]
  },
  {
    category: "Finance",
    date: "Apr 19",
    read: "6 min",
    titleEn: "FX Volatility Brings Hedging Back to the CEO Agenda",
    titleZh: "汇率波动让套保重新回到 CEO 议程",
    summaryEn:
      "Multinationals expand hedge tenors as policy divergence keeps currencies unstable.",
    summaryZh: "在政策分化背景下，跨国企业延长套保期限以对冲币值波动。",
    bodyEn: [
      "Currency volatility is now discussed as strategic earnings risk, not just treasury noise.",
      "Firms are combining exposure forecasting with dynamic hedge policy reviews to improve planning quality."
    ],
    bodyZh: [
      "汇率波动已从财资层面的噪音变成经营利润层面的战略风险议题。",
      "企业正在把敞口预测与动态套保策略联动，以提升预算和经营计划可靠性。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 18",
    read: "6 min",
    titleEn: "Enterprise Search Becomes a Trust Product",
    titleZh: "企业搜索正在变成“可信度产品”",
    summaryEn:
      "Citation quality, permission fidelity, and freshness signals now define adoption.",
    summaryZh: "引用质量、权限一致性与内容新鲜度成为采用率关键指标。",
    bodyEn: [
      "Users adopt AI search when answers are verifiable and permission-safe by design.",
      "Vendors that expose source grounding and freshness indicators are seeing broader enterprise rollout success."
    ],
    bodyZh: [
      "企业用户只有在答案可追溯、权限一致时，才会真正信任并持续使用 AI 搜索。",
      "能够明确展示来源引用和内容时效性的系统，更容易在组织内规模化推广。"
    ]
  },
  {
    category: "Finance",
    date: "Apr 18",
    read: "5 min",
    titleEn: "Retail Broker Apps Pivot from Trading to Education",
    titleZh: "零售券商应用从交易刺激转向教育留存",
    summaryEn:
      "Platforms launch scenario tools and risk explainers to improve long-term user retention.",
    summaryZh: "平台通过情景工具和风险解释功能提升长期留存。",
    bodyEn: [
      "Acquisition costs are forcing retail broker apps to invest in informed decision support.",
      "Educational features that contextualize volatility reduce churn and improve customer trust."
    ],
    bodyZh: [
      "随着获客成本上升，零售券商应用必须投入“决策辅助型”产品能力。",
      "能够解释波动和风险的教育功能，通常能降低流失并提升用户信任度。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 17",
    read: "6 min",
    titleEn: "Open-Source AI Governance Becomes Procurement Standard",
    titleZh: "开源 AI 治理能力成为采购新标准",
    summaryEn:
      "Buyers request model lineage, patch cadence, and reproducible deployment evidence.",
    summaryZh: "采购方开始要求模型谱系、补丁节奏与可复现部署证据。",
    bodyEn: [
      "Open-source model selection now includes governance maturity as a first-class criterion.",
      "Teams increasingly require transparent maintenance timelines and reproducible deployment workflows."
    ],
    bodyZh: [
      "开源模型选型正在把治理成熟度纳入一等评估指标，而不仅看性能和成本。",
      "采购方越来越强调维护节奏透明和部署流程可复现，以降低长期运维风险。"
    ]
  },
  {
    category: "Finance",
    date: "Apr 17",
    read: "7 min",
    titleEn: "Insurance Markets Reprice Climate Exposure Asset by Asset",
    titleZh: "保险市场按资产颗粒度重定价气候风险",
    summaryEn:
      "Premium and coverage structures now reflect location-level resilience signals.",
    summaryZh: "保费和承保结构正在基于资产所在地韧性指标精细化调整。",
    bodyEn: [
      "Underwriters are using higher-resolution climate data to differentiate risk with greater precision.",
      "Assets with adaptation investments are increasingly receiving better coverage terms and financing conditions."
    ],
    bodyZh: [
      "承保机构正在用更高分辨率的气候数据进行风险定价，颗粒度显著提升。",
      "具备防灾和适应性投入的资产，更容易获得更优承保条款与融资条件。"
    ]
  },
  {
    category: "Tech",
    date: "Apr 16",
    read: "5 min",
    titleEn: "Edge AI Delivers ROI in Industrial QA Lines",
    titleZh: "边缘 AI 在工业质检线上开始稳定回报",
    summaryEn:
      "Factories scale compact inference stacks for defect detection and throughput control.",
    summaryZh: "工厂正在规模化部署轻量推理系统用于缺陷识别和节拍优化。",
    bodyEn: [
      "Edge inference is proving commercially viable where latency and process continuity are critical.",
      "Factories that pair model monitoring with operator workflows are seeing stronger and more stable ROI."
    ],
    bodyZh: [
      "在低延迟和连续作业要求高的产线场景里，边缘推理已经具备明确商业价值。",
      "将模型监控与一线操作流程结合的工厂，通常能够获得更稳定的投资回报。"
    ]
  },
  {
    category: "Finance",
    date: "Apr 16",
    read: "6 min",
    titleEn: "Private Markets Track Public Multiples More Closely",
    titleZh: "私募市场估值与二级市场倍数关联更紧",
    summaryEn:
      "Late-stage deals reprice faster as public comparables transmit valuation signals sooner.",
    summaryZh: "随着可比公司信号传导加速，后期融资估值调整速度明显提升。",
    bodyEn: [
      "Late-stage investors now react faster to public market multiple compression and expansion cycles.",
      "Founders that communicate risk-adjusted growth scenarios clearly can reduce negotiation friction in repricing rounds."
    ],
    bodyZh: [
      "后期投资人对二级市场倍数压缩或扩张的反应速度明显更快，估值传导周期缩短。",
      "能清晰表达风险调整后增长路径的团队，在估值重谈阶段通常更有主动权。"
    ]
  }
];

const I18N = {
  en: {
    htmlLang: "en",
    title: "Token Calculator | Prompt Cost Lab",
    description:
      "Token calculator for estimating token usage, context occupancy, and approximate API cost in real time.",
    kicker: "Prompt Cost Lab",
    pageTitle: "Token Calculator",
    heroDesc:
      "Paste your text to estimate tokens, context usage, and approximate API cost in real time.",
    navBrandText: "Prompt Cost Lab",
    navArticles: "Articles",
    languageLabel: "Language",
    languageOptionEn: "English",
    languageOptionZh: "Chinese",
    modelLabel: "Model",
    contextLabel: "Context Window",
    useDemo: "Use Demo",
    clear: "Clear",
    textInputLabel: "Input Text",
    textPlaceholder: "Paste your prompt, instructions, chat history, or document snippets here...",
    outputTokensLabel: "Estimated Output Tokens",
    currencyLabel: "Currency",
    exchangeRateLabel: "Exchange Rate (USD→CNY)",
    statCharsLabel: "Characters",
    statWordsLabel: "Words",
    statInputTokensLabel: "Estimated Input Tokens",
    statTotalTokensLabel: "Total Tokens (with Output)",
    costTitle: "Cost Estimation",
    inputCostLabel: "Input Cost",
    outputCostLabel: "Output Cost",
    totalCostLabel: "Total Cost",
    contextUsageLabel: "Context Usage",
    articlesTitle: "Featured Tech & Finance Reads",
    articlesDesc: "Selected insights for operators, investors, and product teams.",
    readMore: "Read full article",
    backToArticles: "← Back to Articles",
    detailBy: "By Atlas Wire Desk",
    notesTitle: "Notes",
    note1: "This is a front-end estimator for budgeting reference, not official billing precision.",
    note2: "Mixed-language prompts are estimated with heuristics and may differ from real tokenizer output.",
    note3: "You can ask for file batch analysis, history tracking, and configurable model pricing.",
    tokenizerLoading: "Tokenizer: loading real tokenizer...",
    tokenizerReady: (encodingName) => `Tokenizer: precise mode active (${encodingName}).`,
    tokenizerFallback: "Tokenizer: heuristic fallback mode (CDN unavailable or blocked).",
    pricingHint: (model) => `Input $${model.inputPer1M}/1M · Output $${model.outputPer1M}/1M`,
    demoText:
      "You are a senior analyst. Please summarize the following quarterly report and output:\n1) top 5 risks\n2) growth opportunities\n3) 90-day execution plan\n\nAlso provide both English and Chinese versions with a KPI comparison table."
  },
  zh: {
    htmlLang: "zh-CN",
    title: "Token 计算器 | Prompt Cost Lab",
    description: "Token 计算器：实时估算 Token 用量、上下文占用与大致调用成本。",
    kicker: "Prompt Cost Lab",
    pageTitle: "Token 计算器",
    heroDesc: "粘贴文本后，实时估算 Token、上下文占用和大致 API 成本。",
    navBrandText: "Prompt 成本实验室",
    navArticles: "文章",
    languageLabel: "语言",
    languageOptionEn: "英文",
    languageOptionZh: "中文",
    modelLabel: "模型",
    contextLabel: "上下文窗口",
    useDemo: "填充示例",
    clear: "清空",
    textInputLabel: "输入文本",
    textPlaceholder: "在这里粘贴 Prompt、系统指令、对话历史或文档片段...",
    outputTokensLabel: "预估输出 Tokens",
    currencyLabel: "货币",
    exchangeRateLabel: "汇率 (USD→CNY)",
    statCharsLabel: "字符数",
    statWordsLabel: "单词数",
    statInputTokensLabel: "预估输入 Tokens",
    statTotalTokensLabel: "总 Tokens（含输出）",
    costTitle: "费用估算",
    inputCostLabel: "输入费用",
    outputCostLabel: "输出费用",
    totalCostLabel: "总费用",
    contextUsageLabel: "上下文占用",
    articlesTitle: "科技与财经精选文章",
    articlesDesc: "为运营者、投资人和产品团队准备的重点洞察内容。",
    readMore: "阅读全文",
    backToArticles: "← 返回文章列表",
    detailBy: "作者：Atlas Wire 编辑部",
    notesTitle: "说明",
    note1: "这是前端估算器，结果仅用于预算参考，不等于官方精确计费。",
    note2: "中英文混合文本采用经验规则估算，和真实 tokenizer 结果可能有偏差。",
    note3: "你可以继续让我加：文件批量统计、历史记录、模型价格配置化。",
    tokenizerLoading: "Tokenizer：正在加载真实分词器...",
    tokenizerReady: (encodingName) => `Tokenizer：已启用精确模式（${encodingName}）。`,
    tokenizerFallback: "Tokenizer：已回退到经验估算模式（CDN 不可用或被拦截）。",
    pricingHint: (model) => `输入 $${model.inputPer1M}/1M · 输出 $${model.outputPer1M}/1M`,
    demoText:
      "你是一名资深分析师。请总结以下季度报告，并输出：\n1）前 5 个风险\n2）增长机会\n3）90 天执行计划\n\n同时提供中英文双语版本，并使用表格展示 KPI 对比。"
  }
};

const MODEL_ENCODING_MAP = {
  "gpt-5.4": "o200k_base",
  "gpt-5.4-mini": "o200k_base",
  "gpt-5.2": "o200k_base",
  "gpt-4o": "o200k_base"
};

const modelSelect = document.getElementById("modelSelect");
const contextSize = document.getElementById("contextSize");
const textInput = document.getElementById("textInput");
const outputTokensInput = document.getElementById("outputTokens");
const currencySelect = document.getElementById("currency");
const usdToCnyInput = document.getElementById("usdToCny");
const pasteDemoBtn = document.getElementById("pasteDemoBtn");
const clearBtn = document.getElementById("clearBtn");
const languageSelect = document.getElementById("languageSelect");
const tokenizerStatus = document.getElementById("tokenizerStatus");

const charCount = document.getElementById("charCount");
const wordCount = document.getElementById("wordCount");
const inputTokens = document.getElementById("inputTokens");
const totalTokens = document.getElementById("totalTokens");
const inputCost = document.getElementById("inputCost");
const outputCost = document.getElementById("outputCost");
const totalCost = document.getElementById("totalCost");
const contextUsage = document.getElementById("contextUsage");
const usageFill = document.getElementById("usageFill");
const modelPriceHint = document.getElementById("modelPriceHint");
const metaDescription = document.getElementById("metaDescription");
const articlesGrid = document.getElementById("articlesGrid");

let currentLang = "en";
let getEncodingFn = null;
let tokenizerState = "loading";
const encoderCache = new Map();

function initModelOptions() {
  if (!modelSelect) {
    return;
  }

  modelSelect.innerHTML = MODEL_PRICING.map(
    (model) => `<option value="${model.id}">${model.name}</option>`
  ).join("");

  modelSelect.value = MODEL_PRICING[0].id;
}

function ensureModelOptions() {
  if (!modelSelect) {
    return;
  }

  if (modelSelect.options.length === 0) {
    initModelOptions();
  }
}

function getSelectedModel() {
  return MODEL_PRICING.find((model) => model.id === modelSelect.value) || MODEL_PRICING[0];
}

function countWords(text) {
  return text
    .trim()
    .split(/\s+/)
    .filter(Boolean).length;
}

function countCjkChars(text) {
  const matches = text.match(/[\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF]/g);
  return matches ? matches.length : 0;
}

function estimateTokensHeuristic(text) {
  if (!text.trim()) {
    return 0;
  }

  const totalChars = text.length;
  const cjkChars = countCjkChars(text);
  const nonCjkChars = Math.max(0, totalChars - cjkChars);

  // 中文按约 1.7 字符/Token，英文按约 4 字符/Token 混合估算
  const cjkTokens = cjkChars / 1.7;
  const latinTokens = nonCjkChars / 4;

  // 预留消息结构开销，降低纯文本估算偏低的概率
  const overhead = 12;

  return Math.max(0, Math.round(cjkTokens + latinTokens + overhead));
}

function resolveEncodingByModel(modelId) {
  return MODEL_ENCODING_MAP[modelId] || "cl100k_base";
}

function estimateTokens(text, modelId) {
  if (!text.trim()) {
    return 0;
  }

  if (getEncodingFn) {
    try {
      const encodingName = resolveEncodingByModel(modelId);
      let encoder = encoderCache.get(encodingName);
      if (!encoder) {
        encoder = getEncodingFn(encodingName);
        encoderCache.set(encodingName, encoder);
      }

      // 真实 tokenizer 结果叠加最小消息结构开销
      return encoder.encode(text).length + 4;
    } catch (error) {
      tokenizerState = "fallback";
      return estimateTokensHeuristic(text);
    }
  }

  return estimateTokensHeuristic(text);
}

function toCurrency(valueUsd) {
  const currency = currencySelect.value;
  const rate = Number(usdToCnyInput.value) || 0;

  if (currency === "CNY") {
    return {
      symbol: "¥",
      value: valueUsd * rate
    };
  }

  return {
    symbol: "$",
    value: valueUsd
  };
}

function formatMoney(value, symbol) {
  return `${symbol}${value.toFixed(4)}`;
}

function updateTokenizerStatus() {
  const locale = I18N[currentLang] || I18N.en;
  const modelId = getSelectedModel().id;
  const encodingName = resolveEncodingByModel(modelId);

  if (tokenizerState === "loading") {
    tokenizerStatus.textContent = locale.tokenizerLoading;
    return;
  }

  if (tokenizerState === "ready") {
    tokenizerStatus.textContent = locale.tokenizerReady(encodingName);
    return;
  }

  tokenizerStatus.textContent = locale.tokenizerFallback;
}

function applyI18n(lang) {
  const locale = I18N[lang] || I18N.en;

  document.documentElement.lang = locale.htmlLang;
  document.title = locale.title;
  metaDescription.setAttribute("content", locale.description);

  const textIds = [
    "pageTitle",
    "heroDesc",
    "navBrandText",
    "navArticles",
    "languageLabel",
    "modelLabel",
    "contextLabel",
    "textInputLabel",
    "outputTokensLabel",
    "currencyLabel",
    "exchangeRateLabel",
    "statCharsLabel",
    "statWordsLabel",
    "statInputTokensLabel",
    "statTotalTokensLabel",
    "costTitle",
    "inputCostLabel",
    "outputCostLabel",
    "totalCostLabel",
    "contextUsageLabel",
    "articlesTitle",
    "articlesDesc",
    "notesTitle",
    "note1",
    "note2",
    "note3"
  ];

  textIds.forEach((id) => {
    const el = document.getElementById(id);
    if (el && locale[id]) {
      el.textContent = locale[id];
    }
  });

  pasteDemoBtn.textContent = locale.useDemo;
  clearBtn.textContent = locale.clear;
  textInput.placeholder = locale.textPlaceholder;
  languageSelect.options[0].textContent = locale.languageOptionEn;
  languageSelect.options[1].textContent = locale.languageOptionZh;

  updateTokenizerStatus();
  renderArticles();
}

function renderArticles() {
  if (!articlesGrid) {
    return;
  }

  const isZh = currentLang === "zh";

  articlesGrid.innerHTML = ARTICLE_ITEMS.map((item, index) => {
    const title = isZh ? item.titleZh : item.titleEn;
    const summary = isZh ? item.summaryZh : item.summaryEn;
    const category = isZh ? (item.category === "Tech" ? "科技" : "财经") : item.category;
    const readLabel = isZh ? `${item.read.replace("min", "分钟")}` : item.read;
    const locale = I18N[currentLang] || I18N.en;

    return `\n      <a class=\"article-card\" href=\"./article.html?id=${index}&lang=${currentLang}\">\n        <div class=\"article-meta\">\n          <span>${category}</span>\n          <span>${item.date} · ${readLabel}</span>\n        </div>\n        <h4>${title}</h4>\n        <p>${summary}</p>\n        <p class=\"article-read-more\">${locale.readMore}</p>\n      </a>\n    `;
  }).join("");
}

function update() {
  ensureModelOptions();

  const text = textInput.value || "";
  const words = countWords(text);
  const chars = text.length;
  const selectedModel = getSelectedModel();

  const inTokens = estimateTokens(text, selectedModel.id);
  const outTokens = Math.max(0, Number(outputTokensInput.value) || 0);
  const total = inTokens + outTokens;

  const inCostUsd = (inTokens / 1_000_000) * selectedModel.inputPer1M;
  const outCostUsd = (outTokens / 1_000_000) * selectedModel.outputPer1M;
  const totalCostUsd = inCostUsd + outCostUsd;

  const inMoney = toCurrency(inCostUsd);
  const outMoney = toCurrency(outCostUsd);
  const totalMoney = toCurrency(totalCostUsd);

  const contextLimit = Number(contextSize.value) || 0;
  const usagePercent = contextLimit > 0 ? Math.min(100, (total / contextLimit) * 100) : 0;

  charCount.textContent = chars.toLocaleString();
  wordCount.textContent = words.toLocaleString();
  inputTokens.textContent = inTokens.toLocaleString();
  totalTokens.textContent = total.toLocaleString();

  inputCost.textContent = formatMoney(inMoney.value, inMoney.symbol);
  outputCost.textContent = formatMoney(outMoney.value, outMoney.symbol);
  totalCost.textContent = formatMoney(totalMoney.value, totalMoney.symbol);

  contextUsage.textContent = `${usagePercent.toFixed(1)}%`;
  usageFill.style.width = `${usagePercent}%`;

  if (usagePercent >= 85) {
    usageFill.style.background = "linear-gradient(90deg, #ffb26f 0%, #ff6f6f 100%)";
  } else {
    usageFill.style.background = "linear-gradient(90deg, #4ad6a6 0%, #5bb8ff 100%)";
  }

  const locale = I18N[currentLang] || I18N.en;
  modelPriceHint.textContent = locale.pricingHint(selectedModel);
  updateTokenizerStatus();
}

function bindEvents() {
  [
    textInput,
    modelSelect,
    contextSize,
    outputTokensInput,
    currencySelect,
    usdToCnyInput
  ].forEach((el) => {
    el.addEventListener("input", update);
    el.addEventListener("change", update);
  });

  languageSelect.addEventListener("change", () => {
    currentLang = languageSelect.value;
    applyI18n(currentLang);
    update();
  });

  pasteDemoBtn.addEventListener("click", () => {
    const locale = I18N[currentLang] || I18N.en;
    textInput.value = locale.demoText;
    update();
  });

  clearBtn.addEventListener("click", () => {
    textInput.value = "";
    outputTokensInput.value = "512";
    update();
  });
}

async function initTokenizer() {
  tokenizerState = "loading";
  updateTokenizerStatus();

  try {
    const module = await import("https://esm.sh/js-tiktoken@1.0.21/lite");
    if (typeof module.getEncoding === "function") {
      getEncodingFn = module.getEncoding;
      tokenizerState = "ready";
    } else {
      tokenizerState = "fallback";
    }
  } catch (error) {
    tokenizerState = "fallback";
  }

  update();
}

initModelOptions();
bindEvents();
languageSelect.value = currentLang;
applyI18n(currentLang);
update();
initTokenizer();
