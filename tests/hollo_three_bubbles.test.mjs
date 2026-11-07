// HOLLO D09 — synthetic, no-network safety tests.
// Run: node --test tests/hollo_three_bubbles.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import {fileURLToPath} from "node:url";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/HOLLO_333_direct_connect_index.html"),"utf8");
const clone=v=>JSON.parse(JSON.stringify(v));

function extract(start,end,context) {
  const a=source.indexOf(start),b=source.indexOf(end,a+start.length);
  assert.ok(a>=0&&b>a,"Function boundary not found: "+start);
  return vm.runInNewContext("("+source.slice(a,b).trim()+")",context);
}

function resetFixture(failure="none") {
  const original={schema:"hollo-backup",profile:{name:"Original"},enrollment:{complete:true}};
  const raw=JSON.stringify(original);
  const storage=new Map([["hollo_333_direct_connect_v1",raw],["333_identity_handoff_v1",'{"existing":true}']]);
  let failedOnce=false;
  const events=[];
  const ctx={
    state:clone(original),memoryState:clone(original),storageAvailable:true,
    STORAGE_KEY:"hollo_333_direct_connect_v1",IDENTITY_HANDOFF_KEY:"333_identity_handoff_v1",
    JSON,clone,
    localStorage:{
      getItem(k) {
        if(failure==="unreadable"&&k==="hollo_333_direct_connect_v1") throw Error("unreadable");
        return storage.get(k)??null;
      },
      setItem(k,v) {
        if(failure==="quota"&&k==="hollo_333_direct_connect_v1"&&!failedOnce){failedOnce=true;throw Error("quota");}
        if(failure==="bad-readback"&&k==="hollo_333_direct_connect_v1"&&!failedOnce){failedOnce=true;return;}
        storage.set(k,v);
      },
      removeItem(k) {
        if(failure==="handoff-removal"&&k==="333_identity_handoff_v1"&&!failedOnce){failedOnce=true;throw Error("denied");}
        storage.delete(k);
      },
    },
    defaultState:()=>({schema:"hollo-backup",profile:{name:"Fresh"},enrollment:{complete:false}}),
    confirm:()=>true,stopMedia(){},renderAll(){},updateCallContact(){},closeModal(){},
    activateMobileView(){},window:{setTimeout(){}},openEnrollment(){},showToast:m=>events.push(m)
  };
  return {reset:extract("function resetApp(){","function wireEvents(){",ctx),ctx,storage,events,raw};
}

for (const failure of ["none","quota","unreadable","bad-readback","handoff-removal"]) {
  test("reset: "+failure,()=>{
    const f=resetFixture(failure);
    f.reset();
    const expected=failure==="none"?"Fresh":"Original";
    assert.equal(f.ctx.state.profile.name,expected);
    assert.equal(JSON.parse(f.storage.get("hollo_333_direct_connect_v1")).profile.name,expected);
    assert.equal(f.storage.has("333_identity_handoff_v1"),failure!=="none");
    if(failure!=="none") assert.ok(f.events.some(x=>/Reset (cancelled|could not be saved)/.test(x)));
  });
}

test("imported records cannot assign prototype keys or backend verification",()=>{
  assert.match(source,/Object\.create\(null\)/);
  assert.match(source,/['"]__proto__['"]/);
  assert.match(source,/numberVerified:false/);
  assert.match(source,/lastSyncedAt:null/);
  assert.match(source,/!Array\.isArray\(input\.profile\)/);
});

test("background and cross-tab changes do not trigger unload persistence",()=>{
  const a=source.indexOf("window.addEventListener('storage',event=>");
  const b=source.indexOf("function init(){",a);
  assert.ok(a>0&&b>a);
  const handlers=source.slice(a,b);
  assert.match(handlers,/event\.key!==STORAGE_KEY/);
  assert.match(handlers,/window\.addEventListener\('pagehide'/);
  assert.match(handlers,/document\.addEventListener\('visibilitychange'/);
  assert.doesNotMatch(handlers,/saveState\(\)/);
});

test("STOS terminal remains unassigned and app routes intact",()=>{
  const contract=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
  assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
  assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
  assert.equal(contract.governance.futureSTOSPolicy.runtimeBinding,false);
  for(const n of ["3331117777","3332227777","3333337777","3334447777"]) assert.ok(source.includes(n));
});
