// KANSEE D15 — meeting-first layout and Focus Mode source regression tests.
// Run: node --test tests/kansee_focus_mode.test.mjs
// No network, member records, camera, screen capture, or STOS access.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/KANSEE_333_meeting_rooms_index.html"),"utf8");
function focusFixture({rejectFullscreen=false}={}){
  const start=source.indexOf("// Focus Mode is presentation-only");
  const end=source.indexOf("$('#createMeetingBtn').addEventListener",start);
  assert.ok(start>=0&&end>start,"Focus Mode source block missing");
  const block=source.slice(start,end);
  const handlers={},attrs={},events=[];
  const doc={
    fullscreenElement:null,
    addEventListener(name,callback){handlers[name]=callback;},
    body:{classList:{toggle(name,enabled){events.push([name,enabled]);}}}
  };
  const panel={
    async requestFullscreen(){
      if(rejectFullscreen)throw new Error("Fullscreen is disabled in this synthetic browser");
      doc.fullscreenElement=panel;
      handlers.fullscreenchange?.();
    }
  };
  doc.exitFullscreen=async()=>{doc.fullscreenElement=null;handlers.fullscreenchange?.();};
  const button={
    setAttribute(name,value){attrs[name]=value;},
    set textContent(value){events.push(["label",value]);},
    focus(){events.push(["focus",true]);},
    addEventListener(name,callback){handlers["button-"+name]=callback;}
  };
  const run=new Function("document","window","$","activateMobilePanel",
    block+";return {toggleFocusMode,syncFocusMode};");
  const methods=run(doc,{},selector=>selector==="#stagePanel"?panel:button,
    ()=>events.push(["mobile","stagePanel"]));
  return {doc,panel,button,handlers,attrs,events,...methods};
}
test("Focus Mode exposes one keyboard-accessible action",()=>{
  assert.equal(source.split('id="stageFocusBtn"').length-1,1);
  assert.match(source,/aria-label="Enter meeting Focus Mode"/);
  assert.match(source,/aria-pressed="false"/);
  assert.match(source,/focus-toggle/);
});
test("native fullscreen enters and exits without mutating meeting state",async()=>{
  const f=focusFixture();
  await f.toggleFocusMode();
  assert.equal(f.doc.fullscreenElement,f.panel);
  assert.equal(f.attrs["aria-pressed"],"true");
  await f.toggleFocusMode();
  assert.equal(f.doc.fullscreenElement,null);
  assert.equal(f.attrs["aria-pressed"],"false");
});
test("fullscreen denial uses a reversible local CSS fallback",async()=>{
  const f=focusFixture({rejectFullscreen:true});
  await f.toggleFocusMode();
  assert.equal(f.attrs["aria-pressed"],"true");
  await f.toggleFocusMode();
  assert.equal(f.attrs["aria-pressed"],"false");
  assert.ok(f.events.some(([name,enabled])=>name==="kansee-focus-mode"&&enabled===true));
});
test("Escape exits the fallback and restores focus",async()=>{
  const f=focusFixture({rejectFullscreen:true});
  await f.toggleFocusMode();
  f.handlers.keydown({key:"Escape"});
  assert.equal(f.attrs["aria-pressed"],"false");
  assert.ok(f.events.some(([name])=>name==="focus"));
});
test("privacy status remains accessible inside a summary disclosure",()=>{
  assert.match(source,/<details class="kansee-readiness-disclosure">/);
  assert.match(source,/<summary>Connection &amp; Privacy Status/);
  assert.match(source,/id="kanseeReadinessTitle"/);
  assert.match(source,/Local meeting preview/);
});
test("rooms, participants, chat and collaboration controls remain present",()=>{
  for(const id of ["meetingsPanel","stagePanel","rightPanel","stageGrid",
    "previewBtn","muteBtn","cameraBtn","shareBtn","simulateGuestBtn",
    "leaveRoomBtn","copyInviteBtn","roomDetailsBtn","meetingList",
    "chatForm","sideCollab","importWorkspaceBtn","stageFocusBtn"]){
    assert.equal(source.split('id="'+id+'"').length-1,1,id);
  }
  const ids=[...source.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
  assert.equal(ids.length,new Set(ids).size);
});
test("responsive stage and readable controls are retained",()=>{
  assert.match(source,/--kansee-page-max:1820px/);
  assert.match(source,/grid-template-columns:minmax\(245px,18fr\) minmax\(0,62fr\) minmax\(270px,20fr\)/);
  assert.match(source,/\.stage-panel:fullscreen/);
  assert.match(source,/font:400 16px\/1\.4 system-ui,sans-serif/);
  assert.match(source,/max-width:780px/);
  assert.match(source,/max-width:520px/);
});
test("gallery remains explicitly local with 16 demo participants maximum",()=>{
  assert.match(source,/The local demonstration is limited to 16 people/);
  assert.match(source,/grid\.dataset\.count=String\(Math\.min\(16,people\.length\)\)/);
  assert.match(source,/Local Preview/);
});
test("one official header, two tickers and one official toolbar",()=>{
  for(const name of ["vnv-header-autopopulate.js","vnv-333-ticker.js",
    "vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
    assert.equal(source.split("assets/"+name).length-1,1,name);
});
test("future STOS terminal remains unassigned and uncommissioned",()=>{
  const contract=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
  assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
  assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
  assert.equal(contract.governance.futureSTOSPolicy.runtimeBinding,false);
});
