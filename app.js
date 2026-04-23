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


const ARTICLE_ITEMS = Array.isArray(window.ARTICLE_ITEMS) ? window.ARTICLE_ITEMS : [];

const I18N = {
  en: {
    htmlLang: "en",
    title: "AI Signal Desk | Frontier Briefing",
    description:
      "AI Signal Desk delivers real-world AI technology reporting with practical operational analysis.",
    kicker: "AI Signal Desk",
    pageTitle: "AI Signal Desk",
    heroDesc:
      "A practical AI technology brief with real deployment stories, architecture lessons, and execution takeaways.",
    navBrandText: "AI Signal Desk",
    navArticles: "AI Briefs",
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
    articlesTitle: "Real AI Technology Reporting",
    articlesDesc: "Field notes from production rollouts, platform engineering, and AI operations teams.",
    readMore: "Read full article",
    backToArticles: "← Back to Articles",
    detailBy: "By AI Signal Desk Editorial",
    notesTitle: "Method Notes",
    note1: "Articles are written with editorial structure and operational context rather than headline-only summaries.",
    note2: "The calculator is for rough planning. Actual billing still depends on provider-side tokenization and pricing updates.",
    note3: "If needed, this page can be extended with batch file analysis, history tracking, and configurable model pricing.",
    tokenizerLoading: "Tokenizer: loading real tokenizer...",
    tokenizerReady: (encodingName) => `Tokenizer: precise mode active (${encodingName}).`,
    tokenizerFallback: "Tokenizer: heuristic fallback mode (CDN unavailable or blocked).",
    pricingHint: (model) => `Input $${model.inputPer1M}/1M · Output $${model.outputPer1M}/1M`,
    demoText:
      "You are a senior analyst. Please summarize the following quarterly report and output:\n1) top 5 risks\n2) growth opportunities\n3) 90-day execution plan\n\nAlso provide both English and Chinese versions with a KPI comparison table."
  },
  zh: {
    htmlLang: "zh-CN",
    title: "AI Signal Desk | 前沿情报台",
    description: "AI Signal Desk：聚焦真实 AI 科技落地案例与可执行方法论。",
    kicker: "AI Signal Desk",
    pageTitle: "AI 前沿情报台",
    heroDesc: "这里不是拼凑资讯，而是围绕真实落地过程给出可复用的 AI 科技分析。",
    navBrandText: "AI Signal Desk",
    navArticles: "AI 深读",
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
    articlesTitle: "真实 AI 科技深度稿",
    articlesDesc: "围绕生产环境、工程治理与组织协同的现场报道与方法拆解。",
    readMore: "阅读全文",
    backToArticles: "← 返回文章列表",
    detailBy: "作者：AI Signal Desk 编辑部",
    notesTitle: "方法说明",
    note1: "文章采用编辑化结构与业务场景描述，避免空泛拼接式内容。",
    note2: "成本计算仅用于预算参考，真实计费仍以模型服务商规则和最新价格为准。",
    note3: "如需扩展，可继续加入文件批量分析、历史记录与模型价格配置能力。",
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
