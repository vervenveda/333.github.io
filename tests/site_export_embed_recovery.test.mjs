// SIte D20 — embed isolation, standalone export, and recovery contracts.
// Node-only synthetic tests; no browser storage or STOS access.
// Run: node --test tests/site_export_embed_recovery.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/SIte_builder_index.html"),"utf8");
function slice(a,b){
 const i=source.indexOf(a),j=source.indexOf(b,i+a.length);
 assert.ok(i>=0&&j>i,"Missing code boundary "+a);
 return source.slice(i,j).trim();
}
const sample={
 languages:{default:"en",list:[{code:"en",name:"English"}]},
 pages:[{id:"home",title:"Example site",blocks:[
  {id:"a",type:"embed",t:{en:'<script>alert("hello")</script>'}},
  {id:"b",type:"button",t:{en:"Malicious",},link:{type:"url",url:"javascript:alert(1)"},style:{}},
  {id:"c",type:"text",t:{en:"Welcome"},style:{}}
 ]}]
};
const escape=x=>String(x).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
test("embedded blocks never inject authored HTML into the parent editor DOM",()=>{
 assert.doesNotMatch(source,/el\.innerHTML=getText\(b,lang\)/);
 assert.doesNotMatch(source,/inner\.innerHTML=getText\(b,lang\)/);
 assert.equal((source.match(/renderIsolatedEmbed\((?:el|inner),getText\(b,lang\)\)/g)||[]).length,3);
 assert.match(source,/frame\.setAttribute\("sandbox","allow-scripts"\)/);
 assert.doesNotMatch(source,/sandbox="allow-scripts allow-forms/);
});
test("both editor preview paths enforce a unique-origin, network-denying CSP",()=>{
 assert.match(source,/function renderIsolatedPreviewFrame\(frame,code\)/);
 assert.match(source,/default-src \\'none\\'/);
 assert.match(source,/connect-src \\'none\\'/);
 assert.match(source,/form-action \\'none\\'/);
 assert.match(source,/frame\.srcdoc=/);
 assert.match(source,/renderIsolatedPreviewFrame\(frame,documentCode\)/);
});
test("export output sandboxes custom embeds and rejects javascript links",()=>{
 const context={
  site:sample,JSON,escapeHtml:escape,
  getText:(b,lang)=>b.t[lang],styleToCss:()=>"",
 };
 const functions=slice("function safeExportUrl(","function styleToCss(");
 const {buildStaticWebsite,safeExportUrl}=vm.runInNewContext(
  "(function(context){with(context){"+functions+";return {buildStaticWebsite,safeExportUrl};}})",{}
 )(context);
 const html=buildStaticWebsite();
 assert.match(html,/sandbox="allow-scripts"/);
 assert.match(html,/&lt;script&gt;/);
 assert.doesNotMatch(html,/href="javascript:/);
 assert.equal(safeExportUrl("javascript:alert(1)"),"#");
 assert.equal(safeExportUrl("https://example.com"),"https://example.com");
});
test("project imports validate shape and reject invalid or oversized files",()=>{
 const funcs=slice("function validateSiteProject(","function undo(){");
 const validate=vm.runInNewContext("("+funcs.slice(0,funcs.indexOf("function restoreSerialized")).trim()+")");
 assert.equal(validate(sample),true);
 assert.equal(validate({...sample,pages:"not pages"}),false);
 assert.equal(validate({...sample,pages:[{id:"home",title:"T",blocks:[{id:"x",type:"unsupported"}]}]}),false);
 assert.match(source,/file\.size>5\*1024\*1024/);
 assert.match(source,/createRestorePoint\("Before Project JSON import"\)/);
});
test("Project JSON has real export and import controls without account admission",()=>{
 for(const id of ["btnExport","btnImportProject","siteProjectImportFile","btnExportSite","btnUndo","btnRedo","btnSnapshot"]){
  assert.equal(source.split('id="'+id+'"').length-1,1,id);
 }
 assert.match(source,/downloadText\("site-project\.json",JSON\.stringify\(site,null,2\),"application\/json"\)/);
 assert.match(source,/const SITE_ACCOUNT_ACCESS_DORMANT = true/);
 assert.match(source,/const store=SITE_ACCOUNT_ACCESS_DORMANT\?MemStore:/);
});
test("snapshots validate before restore and preserve current site until confirmed",()=>{
 assert.match(source,/function validateSiteProject\(raw\)/);
 assert.match(source,/if\(!validateSiteProject\(item\.site\)\)/);
 assert.match(source,/createRestorePoint\("Before snapshot restore"\)/);
 assert.match(source,/function getSnapshots\(\)/);
 assert.match(source,/const ok=saveSnapshots\(list\)/);
});
test("previous account keys, all editor controls and future STOS remain untouched",()=>{
 assert.match(source,/const STORAGE_KEY = "SITE_ALPHA_V070"/);
 assert.match(source,/const AUTH_KEY = "SITE_ALPHA_AUTH_V1"/);
 const ids=[...source.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(ids.length,new Set(ids).size);
 const contract=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
