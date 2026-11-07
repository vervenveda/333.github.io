// SIte D23 — editor organization and presentation source contract.
// Run: node --test tests/site_studio_visual_d23.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const page=fs.readFileSync(path.join(repo,"app/SIte_builder_index.html"),"utf8");
const toolbar=page.slice(page.indexOf('<div id="topbar">'),page.indexOf('<div id="statusBar">'));
const css=page.slice(page.indexOf("/* D23:"),page.indexOf("</style>",page.indexOf("/* D23:")));
test("five toolbar groups preserve all original actions",()=>{
 for(const name of ["site-tool-navigation","site-tool-view","site-tool-edit","site-tool-create","site-tool-export"])
 assert.equal(toolbar.split("site-tool-group "+name).length-1,1,name);
 for(const id of ["btnNetworkDirectory","btnToggleLeft","btnToggleRight","btnUndo","btnRedo",
 "btnSnapshot","btnEmbedStudio","btnPreview","btnExportSite","btnExport",
 "btnImportProject","btnReset","btnPublishBunya","btnLogout"])
 assert.equal(toolbar.split('id="'+id+'"').length-1,1,id);
});
test("primary editor toolbar structure is balanced and uses 16px labels",()=>{
 const count=(tag,close)=> (toolbar.match(new RegExp(close?"</"+tag+">":"<"+tag+"\\b","g"))||[]).length;
 assert.equal(count("div",false),count("div",true));
 assert.match(css,/\.site-tool-group-label/);
 assert.match(css,/font:400 16px\/1\.35/);
 assert.match(css,/min-height:44px/);
 assert.match(css,/\.device-btn\.active/);
});
test("pages, languages, domains and inspector sections remain",()=>{
 for(const label of ["Pages","Languages","Domains (prep)","Inspector","Add Block"])
 assert.ok(page.includes("<h3>"+label+"</h3>"),label);
 assert.equal(page.split('class="site-rail-section').length-1,5);
 for(const id of ["pageList","langList","primaryDomain","aliasDomains","liveUrl","inspector",
 "btnAddSection","btnAddText","btnAddButton","btnAddImage","btnAddEmbed"])
 assert.equal(page.split('id="'+id+'"').length-1,1,id);
});
test("framed canvas does not introduce coordinate scaling or replace pageCanvas",()=>{
 assert.match(page,/class="site-canvas-heading"/);
 assert.match(css,/#canvas \.canvas-shell/);
 assert.match(css,/#canvas \.page-canvas/);
 assert.doesNotMatch(css,/(?:transform:\s*scale|zoom:\s*[0-9])/);
 assert.equal(page.split('id="pageCanvas"').length-1,1);
});
test("responsive rails and printable canvas remain supported",()=>{
 assert.match(css,/@media\(max-width:1180px\)/);
 assert.match(css,/@media\(max-width:760px\)/);
 assert.match(css,/@media print/);
 assert.match(page,/body\.left-collapsed\.right-collapsed #app/);
});
test("login-free mode and safe project recovery survive",()=>{
 assert.match(page,/<div id="app">/);
 assert.doesNotMatch(page,/id="authOverlay"/);
 assert.match(page,/const SITE_ACCOUNT_ACCESS_DORMANT = true/);
 assert.match(page,/const store=SITE_ACCOUNT_ACCESS_DORMANT\?MemStore:/);
 assert.match(page,/downloadText\("site-project\.json"/);
 assert.match(page,/function renderIsolatedPreviewFrame\(frame,code\)/);
 const ids=[...page.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(new Set(ids).size,ids.length);
});
test("future STOS terminal still requires separate commissioning",()=>{
 const contract=JSON.parse(fs.readFileSync(path.join(repo,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
