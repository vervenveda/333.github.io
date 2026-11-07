// KANSEE read-only synthetic source and restore regressions.
// Run: node --test tests/kansee_hardening.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/KANSEE_333_meeting_rooms_index.html"),"utf8");
const clone=v=>JSON.parse(JSON.stringify(v));
function extract(start,end,ctx){
 const i=source.indexOf(start),j=source.indexOf(end,i+start.length);
 assert.ok(i>=0&&j>i,"missing function boundary "+start);
 return vm.runInNewContext("("+source.slice(i,j).trim()+")",ctx);
}
function fixture(kind="normal"){
 const old={schemaVersion:1,profile:{name:"Before",verified:false},meetings:[{id:"m1"}],sync:{revision:4},currentRoomId:"m1"};
 const data=new Map([["kansee_333_workspace_v1",JSON.stringify(old)]]);
 const messages=[],actions=[];
 let rejected=false;
 const ctx={
   STORAGE_KEY:"kansee_333_workspace_v1",JSON,BUILD:"test",KANSEE_SERVICE:{mode:"local"},
   state:clone(old),currentRoom:{id:"m1"},memoryState:clone(old),safeClone:clone,
   localStorage:{
     getItem(k){if(kind==="unreadable")throw Error("blocked");return data.get(k)??null},
     setItem(k,v){
       if(kind==="quota"&&!rejected){rejected=true;throw Error("quota");}
       if(kind==="bad-readback"&&!rejected){rejected=true;return;}
       data.set(k,v);
     },
     removeItem(k){data.delete(k)}
   },
   normalizeState(raw){return {...clone(raw),profile:{...clone(raw.profile),verified:false},sync:{revision:1,mode:"local"}}},
   confirm(){return kind!=="cancel"},
   stopAllMedia(){actions.push("stop")},
   renderAll(){actions.push("render")},
   toast(x){messages.push(x)}
 };
 const restore=extract("async function importWorkspace(file){","function clearHistory(){",ctx);
 const backup={workspace:{schemaVersion:1,profile:{name:"After",verified:true},meetings:[{id:"m2"}],currentRoomId:"m2"}};
 return {restore,ctx,data,messages,actions,file:{size:150,text:async()=>JSON.stringify(backup)}};
}
for(const kind of ["normal","quota","bad-readback","unreadable","cancel"]){
 test("restore scenario: "+kind,async()=>{
   const x=fixture(kind);
   await x.restore(x.file);
   const expected=kind==="normal"?"After":"Before";
   assert.equal(x.ctx.state.profile.name,expected);
   assert.equal(JSON.parse(x.data.get("kansee_333_workspace_v1")).profile.name,expected);
   assert.equal(x.actions.includes("stop"),kind==="normal");
   if(kind==="normal"){
     assert.equal(x.ctx.state.profile.verified,false);
     assert.match(x.messages.at(-1),/restored and verified/);
   }else assert.doesNotMatch(x.messages.at(-1)||"",/restored and verified/);
 });
}
test("oversized and malformed imports do not replace local workspace",async()=>{
 const x=fixture();
 let read=false;
 await x.restore({size:6*1024*1024,text:async()=>{read=true;return "{}";}});
 assert.equal(read,false);
 await x.restore({size:12,text:async()=>"{not JSON"});
 assert.equal(x.ctx.state.profile.name,"Before");
 assert.equal(x.actions.length,0);
});
test("imported identity cannot establish verified backend membership",()=>{
 assert.match(source,/s\.profile\.verified=false/);
 assert.match(source,/verified:false, \/\/ Local HOLLO records cannot assert verified membership/);
 assert.match(source,/candidate\.profile\.verified=false/);
 assert.match(source,/lastSyncedAt:null/);
});
test("late media responses and room departure invalidate capture",()=>{
 assert.match(source,/mediaRequestRevision\+=1/);
 assert.match(source,/captured\?\.getTracks\(\)\.forEach\(track=>track\.stop\(\)\)/);
 assert.match(source,/currentMeeting\(\)\?\.id!==roomId/);
 assert.match(source,/document\.visibilityState==='hidden'/);
});
test("one canonical header, two tickers, one official toolbar",()=>{
 for(const name of ["vnv-header-autopopulate.js","vnv-333-ticker.js","vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
   assert.equal(source.split("assets/"+name).length-1,1,name);
 assert.doesNotMatch(source,/vnv-global-ecosystem-shell|data-vnv-global-strip|vnv-support\.js/);
});
test("meeting navigation and app feature targets remain intact",()=>{
 for(const id of ["createMeetingBtn","joinRoomBtn","previewBtn","shareBtn","chatForm",
 "meetingList","participantList","importWorkspaceBtn","sideCollab","inviteHistoryList"]){
   assert.ok(source.includes('id="'+id+'"'),id);
 }
 const ids=[...source.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 assert.equal(new Set(ids).size,ids.length);
});
test("future STOS terminal is still unassigned and uncommissioned",()=>{
 const doc=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(doc.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(doc.governance.futureSTOSPolicy.slotAssignments,"not assigned");
 assert.equal(doc.governance.futureSTOSPolicy.runtimeBinding,false);
});
