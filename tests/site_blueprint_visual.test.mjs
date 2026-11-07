// SIte D22 — canonical visual blueprint and direct-entry preservation.
// Run with: node --test tests/site_blueprint_visual.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const html=fs.readFileSync(path.join(repo,"app/SIte_builder_index.html"),"utf8");
const end=html.indexOf("</style>");
const css=html.slice(html.indexOf("/* D22: blueprint-aligned"),end);
test("exactly one canonical header, original 333 ticker, AutoPopulate ticker and official toolbar",()=>{
 for(const component of ["vnv-header-autopopulate.js","vnv-333-ticker.js",
 "vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
  assert.equal(html.split("assets/"+component).length-1,1,component);
 assert.doesNotMatch(html,/vnv-global-ecosystem-shell|data-vnv-global-strip|assets\/vnv-support\.js/);
});
test("centered studio hero has eyebrow, title, description and session-only warning",()=>{
 assert.match(html,/<section id="siteDormantNotice" aria-labelledby="siteStudioTitle">/);
 assert.match(html,/<span class="site-studio-eyebrow">Verve N Veda · 333 Network<\/span>/);
 assert.match(html,/<h1 id="siteStudioTitle">SIte Studio<\/h1>/);
 assert.match(html,/Session-only editing\. Download Project JSON before leaving/);
});
test("three editor panels retain their identities, tools, and expanded layout",()=>{
 for(const id of ["leftPanel","canvas","rightPanel","topbar","btnExportSite","btnExport",
 "btnImportProject","btnPreview","btnUndo","btnRedo","btnEmbedStudio","btnSnapshot",
 "btnAddPage","btnToggleLeft","btnToggleRight","siteModalLayer"]){
  assert.equal(html.split('id="'+id+'"').length-1,1,id);
 }
 assert.match(css,/grid-template-columns:minmax\(245px,270px\) minmax\(0,1fr\) minmax\(270px,300px\)/);
 assert.match(css,/\.page-canvas\{/);
});
test("labels are readable, buttons are elegant and side panels collapse responsively",()=>{
 assert.match(css,/#leftPanel button,#rightPanel button,#topbar button/);
 assert.match(css,/min-height:44px/);
 assert.match(css,/font:400 16px\/1\.4/);
 assert.match(css,/@media\(max-width:1180px\)/);
 assert.match(css,/@media\(max-width:760px\)/);
 assert.match(css,/body\.right-open #rightPanel/);
 assert.match(css,/body\.left-open #leftPanel/);
});
test("entry remains login-free and past project storage is isolated",()=>{
 assert.match(html,/<div id="app">/);
 assert.doesNotMatch(html,/id="authOverlay"/);
 assert.doesNotMatch(html,/(?:^|\n)authInit\(\);\s*render\(\);/);
 assert.match(html,/const SITE_ACCOUNT_ACCESS_DORMANT = true/);
 assert.match(html,/const store=SITE_ACCOUNT_ACCESS_DORMANT\?MemStore:/);
 assert.match(html,/const STORAGE_KEY = "SITE_ALPHA_V070"/);
 assert.match(html,/const AUTH_KEY = "SITE_ALPHA_AUTH_V1"/);
});
test("safe embedded previews and downloadable recovery survive the visual pass",()=>{
 assert.match(html,/function renderIsolatedPreviewFrame\(frame,code\)/);
 assert.match(html,/sandbox="allow-scripts"/);
 assert.match(html,/downloadText\("site-project\.json"/);
 assert.match(html,/function validateSiteProject\(raw\)/);
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(new Set(ids).size,ids.length);
});
test("future sovereign terminal is still neither assigned nor commissioned",()=>{
 const contract=JSON.parse(fs.readFileSync(path.join(repo,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
