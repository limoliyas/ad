import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const ROOT_DIR = process.cwd();
const DIST_DIR = resolve(ROOT_DIR, "dist");

const REQUIRED_ENV = [
  "AD_ZONE_AUTOTAG",
  "AD_ZONE_INPAGE_PUSH",
  "AD_ZONE_BANNER",
];

function assertRequiredEnv() {
  const missing = REQUIRED_ENV.filter((key) => !process.env[key] || !process.env[key].trim());
  if (missing.length > 0) {
    const error = `缺少环境变量：${missing.join(", ")}`;
    throw new Error(error);
  }
}

function replaceAdZones(content) {
  const replacements = {
    "__AD_ZONE_AUTOTAG__": process.env.AD_ZONE_AUTOTAG,
    "__AD_ZONE_INPAGE_PUSH__": process.env.AD_ZONE_INPAGE_PUSH,
    "__AD_ZONE_BANNER__": process.env.AD_ZONE_BANNER,
  };

  let output = content;
  for (const [key, value] of Object.entries(replacements)) {
    output = output.split(key).join(value);
  }
  return output;
}

function writeProcessedHtml(fileName) {
  const sourcePath = resolve(ROOT_DIR, fileName);
  const distPath = resolve(DIST_DIR, fileName);
  const sourceContent = readFileSync(sourcePath, "utf8");
  const outputContent = replaceAdZones(sourceContent);
  writeFileSync(distPath, outputContent, "utf8");
}

function copyStaticFiles() {
  const staticFiles = ["app.js", "article.js", "articles-data.js", "styles.css", "favicon.svg"];
  for (const fileName of staticFiles) {
    copyFileSync(resolve(ROOT_DIR, fileName), resolve(DIST_DIR, fileName));
  }
}

function main() {
  assertRequiredEnv();
  mkdirSync(DIST_DIR, { recursive: true });
  writeProcessedHtml("index.html");
  writeProcessedHtml("article.html");
  copyStaticFiles();
  console.log("构建完成：已生成 dist 目录并注入广告位配置");
}

main();
