// KANSEE D14 conference-first display contract — no browser data or camera access.
// node --test tests/kansee_gallery_layout.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const source=fs.readFileSync(path.join(root,"app/KANSEE_333_meeting_rooms_index.html"),"utf8");
test("gallery adapts to count without removing participant controls",()=>{
 assert.match(source,/grid\.dataset\.count=String\(Math\.min\(16,people\.length\)\)/);
 assert.match(source,/grid\.dataset\.count='0'/);
 for(const count of [1,2,3,4,5,9,10,16]) assert.ok(source.includes('data-count="'+count+'"'),count);
 for(const id of ["stageGrid","participantList","simulateGuestBtn","previewBtn","muteBtn","cameraBtn","shareBtn","leaveRoomBtn"]) assert.ok(source.includes('id="'+id+'"'),id);
});
test("large gallery does not imply live remote conferencing",()=>{
 assert.match(source,/The local demonstration is limited to 16 people/);
 assert.match(source,/person\.simulated\?' · Demo'/);
 assert.match(source,/Local Preview/);
 assert.match(source,/authenticated live conferences|live conferencing/i);
});
test("participant tiles show name and media indicators",()=>{
 assert.match(source,/function makeVideoTile\(person\)/);
 assert.match(source,/left\.textContent=person\.name/);
 assert.match(source,/video\.srcObject=screenStream\|\|localStream/);
 assert.match(source,/right\.className='video-badge'/);
});
test("blueprint stage and accessibility styles exist",()=>{
 assert.match(source,/--kansee-page-max:1700px/);
 assert.match(source,/grid-auto-rows:minmax\(190px,auto\)/);
 assert.match(source,/font-size:16px;line-height:1.3/);
 assert.match(source,/max-width:1510px/);
 assert.match(source,/max-width:780px/);
 assert.match(source,/max-width:520px/);
});
test("existing shared family chrome and future STOS state are untouched",()=>{
 for(const name of ["vnv-header-autopopulate.js","vnv-333-ticker.js","vnv-ticker-autopopulate.js","vnv-ecosystem-toolbar.js"])
   assert.equal(source.split("assets/"+name).length-1,1,name);
 const contract=JSON.parse(fs.readFileSync(path.join(root,"architecture/333-topology-contract.v1.json"),"utf8"));
 assert.equal(contract.governance.futureSTOSPolicy.state,"planned-uncommissioned");
 assert.equal(contract.governance.futureSTOSPolicy.slotAssignments,"not assigned");
});
