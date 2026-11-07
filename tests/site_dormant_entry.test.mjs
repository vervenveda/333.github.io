// SIte D19 — dormant entry preservation contracts; Node stdlib only.
// Run: node --test tests/site_dormant_entry.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const page=fs.readFileSync(path.join(root,"app/SIte_builder_index.html"),"utf8");

test("account sign-in remains dormant, not deleted or bypassed",()=>{
 assert.match(page,/const SITE_ACCOUNT_ACCESS_DORMANT = true/);
 assert.match(page,/function authInit\(\)\{\s*if\(SITE_ACCOUNT_ACCESS_DORMANT\)/);
 for(const id of ["authOverlay","tabSignIn","tabCreate","btnSignIn","btnCreateAccount","signInPass","createPass"])
   assert.equal(page.split('id="'+id+'"').length-1,1,id);
 assert.match(page,/derivePassHash\(pass,salt/);
 assert.match(page,/btnLogout"\)\.hidden=true/);
});
test("temporary studio never reads or overwrites old project/account keys",()=>{
 assert.match(page,/const STORAGE_KEY = "SITE_ALPHA_V070"/);
 assert.match(page,/const AUTH_KEY = "SITE_ALPHA_AUTH_V1"/);
 assert.match(page,/const STORAGE_OK=SITE_ACCOUNT_ACCESS_DORMANT\?false:storageAvailable\(\)/);
 assert.match(page,/const store=SITE_ACCOUNT_ACCESS_DORMANT\?MemStore:/);
 assert.match(page,/function readHolloIdentity\(\)\{\s*if\(SITE_ACCOUNT_ACCESS_DORMANT\)return null/);
 assert.match(page,/function readEvenMailIdentity\(\)\{\s*if\(SITE_ACCOUNT_ACCESS_DORMANT\)return null/);
});
test("embed drafts use isolated selected store rather than shared localStorage",()=>{
 for(const marker of ["store.setItem(EMBED_STUDIO_DRAFT_KEY,code)","store.getItem(EMBED_STUDIO_DRAFT_KEY)",
 "store.removeItem(EMBED_STUDIO_DRAFT_KEY)","store.setItem(EMBED_STUDIO_DRAFT_KEY,input.value)"])
 assert.ok(page.includes(marker),marker);
 assert.doesNotMatch(page,/localStorage\.(?:getItem|setItem|removeItem)\(EMBED_STUDIO_DRAFT_KEY/);
});
test("preview and project export remain, commissioning/publishing stays unavailable",()=>{
 for(const id of ["btnExportSite","btnExport","btnPreview","btnUndo","btnRedo","btnEmbedStudio","btnReset","pageCanvas","btnPublishBunya"])
   assert.equal(page.split('id="'+id+'"').length-1,1,id);
 assert.match(page,/btnPublishBunya"\)\.hidden=true/);
 assert.match(page,/btnPublishBunya"\)\.disabled=true/);
 assert.match(page,/Export Project JSON or Website/);
});
test("dormant banner is distinct from auth and fits three-column application",()=>{
 assert.equal(page.split('id="siteDormantNotice"').length-1,1);
 assert.match(page,/#app\{grid-template-rows:auto minmax\(0,1fr\)\}/);
 assert.match(page,/#siteDormantNotice\{grid-row:1;grid-column:1\/-1/);
 assert.match(page,/#leftPanel,#canvas,#rightPanel\{grid-row:2;min-height:0\}/);
});
test("future STOS service remains uncommissioned and unassigned",()=>{
 const contract=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
