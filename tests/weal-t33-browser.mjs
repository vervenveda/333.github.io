import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {createServer} from "node:http";
import {chromium} from "playwright";

const root=path.resolve("app"),html=fs.readFileSync(path.join(root,"WEAL_domain_hosting_index.html"),"utf8");
const site=fs.readFileSync(path.join(root,"SIte_builder_index.html"),"utf8");
const bunya=fs.readFileSync(path.join(root,"Bunya_digital_infrastructure_index.html"),"utf8");
assert.match(html,/Terminal 33|T33/);
assert.match(html,/UNCOMMISSIONED/);
assert.match(html,/readOnly:true/);
assert.match(html,/liveRouting:false/);
assert.match(html,/listenPort:null/);
assert.match(site,/Open WEAL Hosting Studio/);
assert.match(site,/Download HTML for WEAL/);
assert.match(bunya,/WEAL Hosting/);
assert.match(site,/const BunyaPublishingService=Object\.freeze\(\{\s*mode:"local"/);
assert.match(site,/const SITE_ACCOUNT_ACCESS_DORMANT = true/);
const server=createServer((req,res)=>{
 const target=path.resolve(root,"."+new URL(req.url,"http://localhost").pathname);
 if(!target.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
 try{res.writeHead(200,{"Content-Type":"text/html; charset=utf-8"});res.end(fs.readFileSync(target))}
 catch{res.writeHead(404);res.end("Not found")}
});
await new Promise(ok=>server.listen(0,"127.0.0.1",ok));
const origin="http://127.0.0.1:"+server.address().port;
const browser=await chromium.launch({headless:true});
const results=[];
try{
 for(const viewport of [{width:1440,height:900},{width:390,height:844}]){
  const ctx=await browser.newContext({viewport,acceptDownloads:true});
  const page=await ctx.newPage();const errors=[],remote=[];
  page.on("pageerror",err=>errors.push(err.message));
  await page.route("**/*",route=>{
   if(route.request().url().startsWith(origin+"/"))return route.continue();
   remote.push(route.request().url());return route.abort();
  });
  try{
   await page.goto(origin+"/WEAL_domain_hosting_index.html");
   assert.match(await page.locator("#terminalStatus").innerText(),/UNCOMMISSIONED/);
   assert.equal(await page.locator("#exportManifest").isDisabled(),true);
   await page.locator("#projectName").fill("Academy Preview — Synthetic");
   await page.locator("#targetEnv").selectOption("preview");
   const fakeHtml='<!doctype html><html><head><title>Test only</title></head><body>TEST ONLY — no student data</body></html>';
   await page.locator("#htmlFile").setInputFiles({name:"audit-site.html",mimeType:"text/html",buffer:Buffer.from(fakeHtml)});
   await page.locator("#inspectButton").click();
   await page.waitForFunction(()=>document.querySelector("#fileState")?.textContent==="audit-site.html");
   assert.match(await page.locator("#hashShort").innerText(),/^[a-f0-9]{14}…/);
   assert.equal(await page.locator("#exportManifest").isDisabled(),true);
   await page.locator("#sourceReview").check();
   await page.locator("#ownerReview").check();
   assert.equal(await page.locator("#exportManifest").isDisabled(),false);
   const [releaseDownload]=await Promise.all([page.waitForEvent("download"),page.locator("#exportManifest").click()]);
   const stream=releaseDownload.createReadStream();const chunks=[];for await(const chunk of stream)chunks.push(chunk);
   const exported=JSON.parse(Buffer.concat(chunks).toString("utf8"));
   assert.equal(exported.terminalTarget,"T33");
   assert.equal(exported.releaseStatus,"DRAFT_UNAUTHORIZED");
   assert.equal(exported.activation.allowed,false);
   assert.equal(exported.content.fileName,"audit-site.html");
   assert.equal(exported.content.sha256.length,64);
   assert.equal(exported.content.byteLength,Buffer.byteLength(fakeHtml));
   const [contractDownload]=await Promise.all([page.waitForEvent("download"),page.locator("#exportContract").click()]);
   const cstream=contractDownload.createReadStream();const cb=[];for await(const chunk of cstream)cb.push(chunk);
   const contract=JSON.parse(Buffer.concat(cb).toString("utf8"));
   assert.equal(contract.terminal,"T33");
   assert.equal(contract.authoritative,false);
   assert.equal(contract.serviceUrl,null);
   assert.deepEqual(contract.excludedTerminalSlots,["T01","T02","T03"]);
   assert.deepEqual(remote,[]);
   assert.deepEqual(errors,[]);
   await page.locator("#clearButton").click();
   assert.equal(await page.locator("#exportManifest").isDisabled(),true);
   results.push({viewport,releaseSha256:exported.content.sha256,contractState:contract.mode,passed:true});
   console.log("WEAL_BROWSER=PASS "+viewport.width+"x"+viewport.height);
  }finally{await ctx.close();}
 }
}finally{await browser.close();await new Promise(ok=>server.close(ok))}
fs.writeFileSync("weal-t33-browser-evidence.json",JSON.stringify({schema:"weal-t33-source-only-browser-v1",tests:results,terminalCommissioned:false,liveDeployment:false,sourceOnly:true},null,2)+"\n");
console.log("WEAL_T33_UI=PASS AUTHORIZATION=FAIL_CLOSED LIVE_TERMINAL=HOLD");
