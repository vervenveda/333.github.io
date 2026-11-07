// HOLLO synthetic, no-network regression checks.
// Run from repository root: node --test tests/hollo_hardening.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/HOLLO_333_direct_connect_index.html"),"utf8");

function isolatedFunction(start,next,context) {
  const begin=source.indexOf(start);
  const finish=source.indexOf(next,begin+start.length);
  assert.ok(begin>=0&&finish>begin,"Missing extraction boundary: "+start);
  return vm.runInNewContext("("+source.slice(begin,finish).trim()+")",context);
}

function fixture({canSave=true,canRead=true,handoff=true,confirmRestore=true,available=true}={}){
  const old={schema:"hollo-backup",profile:{name:"Existing"},enrollment:{complete:true},sync:{revision:4},settings:{mobileView:"contacts"}};
  const saved=JSON.stringify(old);
  const records=new Map([["hollo_333_direct_connect_v1",saved],["333_identity_handoff_v1",'{"prior":true}']]);
  const toasts=[];
  const candidate={schema:"hollo-backup",profile:{name:"Restored"},enrollment:{complete:true},sync:{revision:0},settings:{mobileView:"messages"}};
  const context={
    state:structuredClone(old),memoryState:structuredClone(old),storageAvailable:available,
    STORAGE_KEY:"hollo_333_direct_connect_v1",IDENTITY_HANDOFF_KEY:"333_identity_handoff_v1",
    APP_VERSION:"1.3.0",HOLLO_BACKEND:{mode:"local"},
    localStorage:{
      getItem(k){return canRead?records.get(k)??null:(k==="hollo_333_direct_connect_v1"?"corrupt":records.get(k)??null);},
      setItem(k,v){if(!canSave)throw new Error("QuotaExceededError");records.set(k,v);},
      removeItem(k){records.delete(k);}
    },
    validateAndMergeState(){return structuredClone(candidate);},
    writeIdentityHandoff(){
      records.set("333_identity_handoff_v1",'{"new":true}');
      return handoff;
    },
    clone:structuredClone,JSON,
    confirm(){return confirmRestore;},
    showToast(text){toasts.push(text);},
    renderAll(){},updateCallContact(){},closeModal(){},activateMobileView(){}
  };
  const importBackup=isolatedFunction("async function importBackup(file){","function resetApp(){",context);
  const file={size:200,text:async()=>JSON.stringify(candidate)};
  return {importBackup,file,context,records,toasts,saved,old};
}

test("valid backup commits only after verified browser storage and updates handoff",async()=>{
  const f=fixture();
  await f.importBackup(f.file);
  assert.equal(JSON.parse(f.records.get("hollo_333_direct_connect_v1")).profile.name,"Restored");
  assert.equal(f.context.state.profile.numberVerified,false);
  assert.equal(f.toasts.at(-1),"HOLLO backup restored and verified on this device.");
});

test("storage quota failure never replaces active workspace",async()=>{
  const f=fixture({canSave:false});
  await f.importBackup(f.file);
  assert.equal(f.records.get("hollo_333_direct_connect_v1"),f.saved);
  assert.equal(f.context.state.profile.name,"Existing");
  assert.match(f.toasts.at(-1),/previous HOLLO workspace/);
});

test("failed identity handoff attempts rollback of both storage records",async()=>{
  const f=fixture({handoff:false});
  await f.importBackup(f.file);
  assert.equal(f.records.get("hollo_333_direct_connect_v1"),f.saved);
  assert.equal(f.records.get("333_identity_handoff_v1"),'{"prior":true}');
  assert.equal(f.context.state.profile.name,"Existing");
});

test("failed persistence readback must not claim restore success",async()=>{
  const f=fixture({canRead:false});
  await f.importBackup(f.file);
  assert.equal(f.context.state.profile.name,"Existing");
  assert.doesNotMatch(f.toasts.at(-1),/restored and verified/);
});

test("cancelled restore leaves both records unchanged",async()=>{
  const f=fixture({confirmRestore:false});
  await f.importBackup(f.file);
  assert.equal(f.records.get("hollo_333_direct_connect_v1"),f.saved);
  assert.equal(f.records.get("333_identity_handoff_v1"),'{"prior":true}');
});

test("unavailable storage refuses import without mutating account",async()=>{
  const f=fixture({available:false});
  await f.importBackup(f.file);
  assert.equal(f.records.get("hollo_333_direct_connect_v1"),f.saved);
  assert.match(f.toasts.at(-1),/Restore cancelled/);
});

test("oversized backup is refused before reading file data",async()=>{
  const f=fixture();
  let read=false;
  await f.importBackup({size:6*1024*1024,text:async()=>{read=true;return "{}";}});
  assert.equal(read,false);
  assert.equal(f.records.get("hollo_333_direct_connect_v1"),f.saved);
});

test("malformed backup and wrong schema never overwrite records",async()=>{
  for(const payload of ["broken",JSON.stringify({schema:"other"})]){
    const f=fixture();
    await f.importBackup({size:100,text:async()=>payload});
    assert.equal(f.records.get("hollo_333_direct_connect_v1"),f.saved);
    assert.match(f.toasts.at(-1),/not a valid HOLLO backup/);
  }
});

test("source preserves identity, media cleanup and accessibility boundaries",()=>{
  for(const marker of [
    "numberVerified:false // Browser backups never verify membership",
    "out.enrollment.verification=out.enrollment.complete?",
    "function normalizeInviteRecords(value,contacts,direction)",
    "function normalizeActivityRecords(value,contacts)",
    "mediaRequestRevision+=1;",
    "captured.getTracks().forEach(track=>track.stop())",
    "document.addEventListener('focusin'",
    "el.getClientRects().length>0",
    "document.visibilityState==='hidden'"
  ]) assert.ok(source.includes(marker),marker);
});
