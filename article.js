(function () {
  const items = Array.isArray(window.ARTICLE_ITEMS) ? window.ARTICLE_ITEMS : [];

  const detailTitle = document.getElementById("detailTitle");
  const detailMeta = document.getElementById("detailMeta");
  const detailBody = document.getElementById("detailBody");
  const detailLang = document.getElementById("detailLang");
  const detailBackBtn = document.getElementById("detailBackBtn");
  const backListLink = document.getElementById("backListLink");

  const dict = {
    en: {
      titleFallback: "Article Not Found",
      bodyFallback: "The requested article does not exist.",
      back: "← Back to Articles",
      navArticles: "Articles",
      by: "By Atlas Wire Desk"
    },
    zh: {
      titleFallback: "未找到文章",
      bodyFallback: "你访问的文章不存在。",
      back: "← 返回文章列表",
      navArticles: "文章",
      by: "作者：Atlas Wire 编辑部"
    }
  };

  function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
  }

  function getArticleIndex() {
    const raw = getQueryParam("id");
    const parsed = Number(raw);
    if (!Number.isInteger(parsed) || parsed < 0 || parsed >= items.length) {
      return -1;
    }
    return parsed;
  }

  function getLang() {
    const q = getQueryParam("lang");
    return q === "zh" ? "zh" : "en";
  }

  function updateBackLinks(lang) {
    const hashUrl = `./index.html#articles`;
    const withLang = `./index.html#articles?lang=${lang}`;

    if (backListLink) {
      backListLink.textContent = dict[lang].navArticles;
      backListLink.href = hashUrl;
      backListLink.setAttribute("data-lang-url", withLang);
    }

    if (detailBackBtn) {
      detailBackBtn.textContent = dict[lang].back;
    }
  }

  function render(index, lang) {
    updateBackLinks(lang);

    if (index < 0 || !items[index]) {
      document.title = dict[lang].titleFallback;
      detailTitle.textContent = dict[lang].titleFallback;
      detailMeta.textContent = "";
      detailBody.innerHTML = `<p>${dict[lang].bodyFallback}</p>`;
      return;
    }

    const item = items[index];
    const isZh = lang === "zh";
    const title = isZh ? item.titleZh : item.titleEn;
    const body = isZh ? item.bodyZh : item.bodyEn;
    const category = isZh ? (item.category === "Tech" ? "科技" : "财经") : item.category;
    const readText = isZh ? item.read.replace("min", "分钟") : item.read;

    document.documentElement.lang = isZh ? "zh-CN" : "en";
    document.title = title;
    detailTitle.textContent = title;
    detailMeta.textContent = `${dict[lang].by} · ${category} · ${item.date} · ${readText}`;
    detailBody.innerHTML = body.map((p) => `<p>${p}</p>`).join("");
  }

  const index = getArticleIndex();
  let lang = getLang();

  if (detailLang) {
    detailLang.value = lang;
    detailLang.addEventListener("change", () => {
      lang = detailLang.value === "zh" ? "zh" : "en";
      const params = new URLSearchParams(window.location.search);
      params.set("lang", lang);
      if (index >= 0) {
        params.set("id", String(index));
      }
      window.history.replaceState(null, "", `?${params.toString()}`);
      render(index, lang);
    });
  }

  if (detailBackBtn) {
    detailBackBtn.addEventListener("click", () => {
      window.location.href = "./index.html#articles";
    });
  }

  render(index, lang);
})();
