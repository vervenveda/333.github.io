// E=Ven Mail D17 restrained palette / symmetry preservation contract.
// node --test tests/even_mail_palette.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const html=fs.readFileSync(path.join(repo,"app/EVen_mail_index.html"),"utf8");
const last=html.slice(html.indexOf("/* D17 — E=Ven Mail restrained correspondence palette"));
test("refined cream and charcoal dominate the D17 presentation layer",()=>{
 assert.ok(last.length>3000);
 for(const rule of ["--paper:#f5f2ea","--ink:#252d2b",".header{",".identity-strip{",".sidebar{",".reader{"])
   assert.ok(last.includes(rule),rule);
 assert.match(last,/\.header-button\.primary\{background:#fff9ee/);
 assert.match(last,/\.compose-button,\.apply-button\{/);
});
test("centered search and symmetrical mailbox ratios are defined",()=>{
 assert.match(last,/grid-template-columns:44px minmax\(182px,232px\) minmax\(260px,1fr\) auto/);
 assert.match(last,/\.search-wrap\{width:100%;max-width:630px;margin:0 auto;justify-self:center\}/);
 assert.match(last,/grid-template-columns:246px minmax\(355px,34fr\) minmax\(400px,51fr\)/);
 assert.match(last,/\.identity-strip-inner\{/);
});
test("existing controls retain their element IDs and mobile reader class",()=>{
 for(const id of ["sidebarToggle","mailSearch","applyEmailButton","syncButton","settingsButton",
   "profileButton","holloIdentityChip","holloIdentityText","sidebar","composeButton",
   "sidebarApplyButton","mailList","reader","readerContent","modalLayer"]){
   assert.equal(html.split('id="'+id+'"').length-1,1,id);
 }
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(new Set(ids).size,ids.length);
 assert.match(last,/\.reader\.mobile-open\{display:block\}/);
});
test("canonical family chrome is exactly one of each component",()=>{
 for(const component of ["vnv-header-autopopulate.js","vnv-333-ticker.js",
   "vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
   assert.equal(html.split("assets/"+component).length-1,1,component);
});
test("local email is not misrepresented as operational delivery",()=>{
 assert.match(html,/An application is not yet a live mailbox/);
 assert.match(html,/Local Workspace/);
});
test("dedicated STOS terminal remains unassigned",()=>{
 const contract=JSON.parse(fs.readFileSync(path.join(repo,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
