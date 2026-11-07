// HOLLO D11: canonical page chrome and preservation regression.
// node --test tests/hollo_blueprint_chrome.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const html=fs.readFileSync(path.join(root,"app/HOLLO_333_direct_connect_index.html"),"utf8");
const count=v=>html.split(v).length-1;

test("exactly one approved header and each of two tickers plus toolbar",()=>{
 for(const name of ["vnv-header-autopopulate.js","vnv-333-ticker.js","vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"]){
   assert.equal(count("assets/"+name),1,name);
 }
 assert.equal(count("VNV_HEADER.mount("),1);
});

test("retired page-wide header strip and duplicate menu loader are absent",()=>{
 assert.doesNotMatch(html,/data-vnv-global-strip|vnv-global-ecosystem-shell|vnv-support\.js/);
 assert.equal(count('class="hollo-network-menu"'),1);
 assert.match(html,/How HOLLO protects your local workspace/);
});

test("historical navigation and support actions remain reachable",()=>{
 for(const href of [
  "../index.html","./KANSEE_333_meeting_rooms_index.html",
  "./Bazaar_Art_Live_index.html","./EVen_mail_index.html",
  "./SIte_builder_index.html","./Bunya_digital_infrastructure_index.html",
  "https://vervenveda.com/#directory",
  "https://vervenveda.com/core/directory-agi/",
  "https://vervenveda.com/cloud/",
  "https://buy.stripe.com/7sY9AU9Nv6G02jj3En4AU0r"
 ]) assert.ok(html.includes(href),href);
});

test("account and communications event targets are present",()=>{
 for(const id of ["profileBtn","emailApplicationBtn","settingsBtn","profileIdentity","contactsPanel","messagesPanel","callPanel","contactList","messageForm","importBackupBtn"])assert.ok(html.includes('id="'+id+'"'),id);
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(ids.length,new Set(ids).size);
});

test("workspace status reserves a dock-safe right edge at laptop widths",()=>{
 assert.match(html,/max-width:1479px/);
 assert.match(html,/padding-right:clamp\(296px,27vw,330px\)/);
 assert.match(html,/max-width:959px/);
});

test("HOLLO does not claim a commissioned STOS terminal",()=>{
 const doc=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(doc.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(doc.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
