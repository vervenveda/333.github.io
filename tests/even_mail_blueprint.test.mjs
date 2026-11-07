// E=Ven Mail D16 layout and preservation contract.
// node --test tests/even_mail_blueprint.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const base=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const html=fs.readFileSync(path.join(base,"app/EVen_mail_index.html"),"utf8");
test("exactly one canonical header, two tickers, one official toolbar",()=>{
 for(const part of ["vnv-header-autopopulate.js","vnv-333-ticker.js","vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
 assert.equal(html.split("assets/"+part).length-1,1,part);
 assert.doesNotMatch(html,/vnv-support\.js|data-vnv-global-strip/);
});
test("mailbox uses the correspondence-first three-pane layout and readable text",()=>{
 assert.match(html,/--max:1760px/);
 assert.match(html,/grid-template-columns:minmax\(245px,260px\) minmax\(325px,\.92fr\) minmax\(420px,1\.35fr\)/);
 assert.match(html,/\.sender,\.subject\{font-size:16px/);
 assert.match(html,/\.preview,\.mail-time\{font-size:16px/);
 assert.match(html,/\.reader-body\{padding:24px 28px 40px;font-size:17px/);
});
test("mobile reader class agrees with existing application JavaScript",()=>{
 assert.match(html,/classList\.add\("mobile-open"\)/);
 assert.match(html,/classList\.remove\("mobile-open"\)/);
 assert.match(html,/\.reader\.mobile-open\{display:block\}/);
 assert.doesNotMatch(html,/reader\.mobile-visible/);
});
test("original correspondence features and modal controls remain",()=>{
 for(const id of ["sidebarToggle","mailSearch","applyEmailButton","syncButton",
 "settingsButton","profileButton","holloIdentityChip","sidebar","folderList",
 "mailList","reader","readerContent","modalLayer","accountList","storageSummary"]){
 assert.equal(html.split('id="'+id+'"').length-1,1,id);
 }
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(ids.length,new Set(ids).size);
});
test("local mailbox language does not claim operational provisioned email",()=>{
 assert.match(html,/An application is not yet a live mailbox/);
 assert.match(html,/Real approval requires authenticated review/);
 assert.match(html,/Local Workspace/);
});
test("STOS remains unassigned and uncommissioned",()=>{
 const contract=JSON.parse(fs.readFileSync(path.join(base,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
