// Renderiza builder.mmd em PNG, embutindo os ícones como data URI (o mmdc não resolve caminhos relativos).
// Uso: NODE_PATH=<pasta com @mermaid-js/mermaid-cli> node render.mjs [saida.png]
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const out = process.argv[2] ?? join(here, "../png/builder-upstream-downstream.png");
const mime = { png: "image/png", svg: "image/svg+xml" };

const src = readFileSync(join(here, "builder.mmd"), "utf8").replace(
  /src='(icons\/[^']+)'/g,
  (_, p) => `src='data:${mime[p.split(".").pop()]};base64,${readFileSync(join(here, p)).toString("base64")}'`
);
const tmp = join(here, ".builder.render.mmd");
writeFileSync(tmp, src);

const chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const pcfg = join(here, ".puppeteer.json");
writeFileSync(pcfg, JSON.stringify(existsSync(chrome) ? { executablePath: chrome } : {}));

const mcfg = join(here, ".mermaid.json");
writeFileSync(mcfg, JSON.stringify({
  maxTextSize: 2000000,
  themeCSS: "* { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; }",
})); // ícones em base64 passam do limite padrão (50k)

const mmdc = process.env.MMDC ?? "mmdc";
execFileSync(mmdc, ["-i", tmp, "-o", out, "-s", "3", "-b", "white", "-p", pcfg, "-c", mcfg], { stdio: "inherit" });
console.log("ok", out);
