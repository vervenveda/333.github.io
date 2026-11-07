// E=Ven Mail D18 — synthetic, no-network recovery and authority regressions.
// Run: node --test tests/even_mail_integrity.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/EVen_mail_index.html"),"utf8");
const clone=x=>JSON.parse(JSON.stringify(x));
function extract(start,end,context){
 const i=source.indexOf(start),j=source.indexOf(end,i+start.length);
 assert.ok(i>=0&&j>i,"function extraction: "+start);
 return vm.runInNewContext("("+source.slice(i,j).trim()+")",context);
}
function fixture(mode="success",empty=false){
 const original={schema:"even-mail-workspace",version:"1.1.0",profile:{name:"Old"},
   messages:[{id:"m1"}],applications:[],mailboxes:[],sync:{revision:3}};
 const raw=JSON.stringify(original);
 const storage=new Map(empty?[]:[["even_mail_workspace_v2",raw]]);
 const toasts=[],actions=[];
 let count=0;
 const ctx={
  state:clone(original),observedStoredRecord:storage.get("even_mail_workspace_v2")??null,
  persistenceConflict:false,persistenceWarningShown:false,
  MAX_IMPORT_BYTES:5*1024*1024,APP_VERSION:"1.1.0",
  EVEN_MAIL_BACKEND:{mode:"local"},STORAGE_KEY:"even_mail_workspace_v2",JSON,clone,
  console:{warn(){}},
  localStorage:{
   getItem(k){if(mode==="unreadable"&&count++===0)throw Error("blocked");return storage.get(k)??null;},
   setItem(k,v){if(mode==="quota"&&count++===0)throw Error("quota");
     if(mode==="readback"&&count++===0)return;
     storage.set(k,v);},
   removeItem(k){storage.delete(k);}
  },
  showToast(x){toasts.push(x)},window:{confirm:()=>mode!=="cancel"},
  normalizeState:clone,closeModal(){actions.push("close")},renderAll(){actions.push("render")}
 };
 ctx.commitWorkspaceReplacement=extract("function commitWorkspaceReplacement(candidate){","async function importWorkspace(file){",ctx);
 const importWorkspace=extract("async function importWorkspace(file){","function openSettings(){",ctx);
 const saveState=extract("function saveState(){","function readHolloProfile(){",ctx);
 const file={size:120,text:async()=>JSON.stringify({schema:"even-mail-workspace",
   profile:{name:"New"},messages:[],mailboxes:[],applications:[]})};
 return {ctx,importWorkspace,saveState,file,storage,toasts,actions,original,raw};
}
for(const mode of ["success","quota","readback","unreadable","cancel"]){
 test("backup restore preserves prior records: "+mode,async()=>{
  const f=fixture(mode);
  await f.importWorkspace(f.file);
  const name=mode==="success"?"New":"Old";
  assert.equal(f.ctx.state.profile.name,name);
  assert.equal(JSON.parse(f.storage.get("even_mail_workspace_v2")).profile.name,name);
  assert.equal(f.actions.includes("close"),mode==="success");
  if(mode==="success")assert.match(f.toasts.at(-1),/restored and verified/);
  else assert.doesNotMatch(f.toasts.at(-1)||"",/restored and verified/);
 });
}
test("oversized or malformed backups cannot replace local drafts",async()=>{
 const f=fixture();
 let read=false;
 await f.importWorkspace({size:6*1024*1024,text:async()=>{read=true;return "{}";}});
 assert.equal(read,false);
 await f.importWorkspace({size:32,text:async()=>"{broken"});
 assert.equal(f.ctx.state.profile.name,"Old");
 assert.equal(f.storage.get("even_mail_workspace_v2"),f.raw);
});
test("first-write cross-tab race cannot overwrite another tab",()=>{
 const f=fixture("success",true);
 f.storage.set("even_mail_workspace_v2",'{"anotherTab":true}');
 assert.equal(f.saveState(),false);
 assert.equal(f.ctx.persistenceConflict,true);
 assert.equal(f.storage.get("even_mail_workspace_v2"),'{"anotherTab":true}');
});
test("imported status and sync metadata cannot claim active remote authority",()=>{
 assert.match(source,/status: \["application-draft", "application-pending", "application-withdrawn", "legacy-local"\]/);
 assert.match(source,/lastSyncedAt:null/);
 assert.match(source,/syncEnabled: false/);
 assert.match(source,/provisioningEnabled: false/);
 assert.match(source,/SMTP submission is not configured/);
});
test("bounded records, deduplication and local application status are present",()=>{
 for(const marker of ["MAX_APPLICATIONS = 250","MAX_MAILBOXES = 250",
  "MAX_MESSAGES = 500","function uniqueRecords(rows)","const linkedMailboxes"])
  assert.ok(source.includes(marker),marker);
 assert.match(source,/seen\.has\(item\.id\)/);
});
test("draft, sent-local and application success require saved data",()=>{
 assert.match(source,/if \(!saveState\(\)\) return;\s*closeModal\(\);\s*handleFolder\("drafts"\)/);
 assert.match(source,/if \(!saveState\(\)\) return;\s*closeModal\(\);\s*handleFolder\("sent"\)/);
 assert.match(source,/if \(!saveState\(\)\) return;\s*closeModal\(\);\s*renderAll\(\)/);
});
test("storage listener preserves unsaved tab before reloading",()=>{
 assert.match(source,/if\(event\.newValue!==observedStoredRecord\)/);
 assert.match(source,/persistenceConflict=true/);
 assert.match(source,/Export this tab before reloading/);
});
test("all existing shared components and STOS dormancy remain",()=>{
 for(const name of ["vnv-header-autopopulate.js","vnv-333-ticker.js",
   "vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
  assert.equal(source.split("assets/"+name).length-1,1,name);
 const contract=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
