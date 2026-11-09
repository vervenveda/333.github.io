// Synthetic, offline regression checks for Bazaar Art Live restore recovery.
// No member records, production storage, network requests, or STOS access.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const html=readFileSync(new URL('../app/Bazaar_Art_Live_index.html',import.meta.url),'utf8');
const start=html.indexOf('async function importWorkspaceFile(file){');
const end=html.indexOf('function resetWorkspace(){',start);
assert.ok(start>=0&&end>start,'Restore function must exist');
const source=html.slice(start,end);
function fixture({failWrite=false}={}){
  let workspace='{"old":true}',pending=null;
  const rows=[],messages=[];
  const db={transaction(){const staged=[];const tx={oncomplete:null,onabort:null,onerror:null,
    objectStore:()=>({add:x=>staged.push(x)})};
    queueMicrotask(()=>{rows.push(...staged);tx.oncomplete?.()});return tx;}};
  const env={
    MediaDB:{open:async()=>db,all:async()=>rows.map(x=>({...x}))},
    localStorage:{
      getItem:k=>k.endsWith(':pending-media-restore')?pending:workspace,
      setItem(k,v){if(k.endsWith(':pending-media-restore')){pending=v;return;}
        if(failWrite)throw Error('quota');workspace=v;},
      removeItem:k=>{if(k.endsWith(':pending-media-restore'))pending=null;}
    },
    STATE_KEY:'test-bazaar',APP_VERSION:1,normalizeState:x=>x,
    safeText:String,confirm:()=>true,state:{old:true},
    applySettings(){},updateProfileChip(){},updateBadges(){},closeModal(){},setView(){},
    toast:m=>messages.push(m),console:{warn(){}}
  };
  const get=new Function(...Object.keys(env),'"use strict";'+source+
    ';return {run:importWorkspaceFile,current:()=>state};');
  const instance=get(...Object.values(env));
  const payload={schema:'bazaar-art-live-workspace',
    state:{users:[],posts:[],stories:[],activeView:'home'},
    media:[{id:'new',type:'image/png',dataUrl:'data:image/png;base64,AAAA'}]};
  return {run:()=>instance.run({size:500,text:async()=>JSON.stringify(payload)}),
    snapshot:()=>({workspace,pending,rows,messages,state:instance.current()})};
}
test('successful restore clears its pending recovery marker',async()=>{
  const f=fixture();await f.run();const s=f.snapshot();
  assert.equal(s.pending,null);assert.equal(s.rows.length,1);
  assert.match(s.workspace,/"version":1/);
});
test('failed workspace write preserves original and records uncertain media',async()=>{
  const f=fixture({failWrite:true});await f.run();const s=f.snapshot();
  assert.equal(s.workspace,'{"old":true}');
  assert.deepEqual(s.state,{old:true});
  assert.deepEqual(JSON.parse(s.pending).mediaIds,['new']);
  assert.equal(s.rows.length,1);
  assert.ok(!s.messages.some(x=>x.includes('imported.')));
});
