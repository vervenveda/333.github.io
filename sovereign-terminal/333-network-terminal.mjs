import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import {execFileSync} from "node:child_process";
import {fileURLToPath} from "node:url";

const HERE=path.dirname(fileURLToPath(import.meta.url));
const ROOT=path.resolve(HERE,"..");
const HOST="127.0.0.1";
const PORT=18733;
const SERVICE="khaemenes-333-network-master-key";
const ACCOUNT="333-network-terminal";
const DATA_ROOT=path.join(os.homedir(),"Library","Application Support","Khaemenes","333-Network");
const NS_ROOT=path.join(DATA_ROOT,"namespaces");
const AUDIT_PATH=path.join(DATA_ROOT,"audit.jsonl");
const ALLOWED=new Set(["gateway","bazaar","bunya","even","fleapit","fleapit-gate","hollo","kansee","site","weal"]);

function fail(msg){console.error("[WITHHOLD]",msg);process.exit(1)}
function ensureDir(p){fs.mkdirSync(p,{recursive:true,mode:0o700})}
function readKey(){
  let raw;
  try{raw=execFileSync("/usr/bin/security",["find-generic-password","-s",SERVICE,"-a",ACCOUNT,"-w"],{encoding:"utf8"}).trim()}catch{fail("Master key not found in macOS Keychain")}
  let key;
  try{key=Buffer.from(raw,"base64")}catch{fail("Master key is not valid base64")}
  if(key.length!==32)fail("Master key must decode to exactly 32 bytes");
  return key;
}
function approvedClients(){return JSON.parse(fs.readFileSync(path.join(HERE,"approved-clients.json"),"utf8")).clients}
function gitBlobSha(buf){
  const head=Buffer.from("blob "+buf.length+"\0","utf8");
  return crypto.createHash("sha1").update(head).update(buf).digest("hex");
}
function verifyClients(){
  for(const c of approvedClients()){
    const p=path.join(ROOT,c.path);
    if(!fs.existsSync(p))fail("Approved client missing: "+c.path);
    const actual=gitBlobSha(fs.readFileSync(p));
    if(actual!==c.git_blob_sha)fail("Approved client integrity mismatch: "+c.path);
  }
}
function audit(event){
  ensureDir(DATA_ROOT);
  fs.appendFileSync(AUDIT_PATH,JSON.stringify({at:new Date().toISOString(),...event})+"\n",{mode:0o600});
}
function nsFile(ns){if(!ALLOWED.has(ns))throw new Error("namespace denied");return path.join(NS_ROOT,ns,"snapshot.enc.json")}
function encrypt(key,obj){
  const iv=crypto.randomBytes(12),cipher=crypto.createCipheriv("aes-256-gcm",key,iv);
  const plain=Buffer.from(JSON.stringify(obj),"utf8");
  const body=Buffer.concat([cipher.update(plain),cipher.final()]);
  return {schema:"333-encrypted-snapshot-v1",alg:"AES-256-GCM",iv:iv.toString("base64"),tag:cipher.getAuthTag().toString("base64"),ciphertext:body.toString("base64")};
}
function decrypt(key,env){
  if(!env||env.schema!=="333-encrypted-snapshot-v1"||env.alg!=="AES-256-GCM")throw new Error("invalid encrypted snapshot");
  const decipher=crypto.createDecipheriv("aes-256-gcm",key,Buffer.from(env.iv,"base64"));
  decipher.setAuthTag(Buffer.from(env.tag,"base64"));
  return JSON.parse(Buffer.concat([decipher.update(Buffer.from(env.ciphertext,"base64")),decipher.final()]).toString("utf8"));
}
function load(ns,key){
  const p=nsFile(ns); if(!fs.existsSync(p))return {revision:0,payload:null,updatedAt:null};
  return decrypt(key,JSON.parse(fs.readFileSync(p,"utf8")));
}
function save(ns,key,expectedRevision,payload){
  const current=load(ns,key);
  if(Number(expectedRevision)!==Number(current.revision))throw Object.assign(new Error("revision conflict"),{code:"CONFLICT",currentRevision:current.revision});
  const next={revision:current.revision+1,payload,updatedAt:new Date().toISOString()};
  const p=nsFile(ns); ensureDir(path.dirname(p));
  const tmp=p+".tmp-"+process.pid;
  fs.writeFileSync(tmp,JSON.stringify(encrypt(key,next),null,2),{mode:0o600});
  fs.renameSync(tmp,p);
  const verify=load(ns,key);
  if(verify.revision!==next.revision)throw new Error("readback verification failed");
  audit({type:"snapshot.write",namespace:ns,revision:next.revision});
  return next;
}
function json(res,status,obj){const body=JSON.stringify(obj);res.writeHead(status,{"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff","referrer-policy":"no-referrer","content-length":Buffer.byteLength(body)});res.end(body)}
function body(req,max=20*1024*1024){return new Promise((resolve,reject)=>{let size=0,ch=[];req.on("data",c=>{size+=c.length;if(size>max){reject(new Error("body too large"));req.destroy();return}ch.push(c)});req.on("end",()=>{try{resolve(JSON.parse(Buffer.concat(ch).toString("utf8")||"{}"))}catch(e){reject(e)}});req.on("error",reject)})}

verifyClients();
ensureDir(NS_ROOT);
const key=readKey();
const pairingCode=String(crypto.randomInt(10000000,100000000));
let attempts=0,pairedToken=null;
console.log("333 Network Sovereign Terminal");
console.log("Bind:",HOST+":"+PORT);
console.log("Owner pairing code:",pairingCode);
console.log("Namespaces:",[...ALLOWED].join(", "));
console.log("Network authority: NONE · Public publishing: NONE · STOS authority: NONE");

const server=http.createServer(async(req,res)=>{
  const remote=req.socket.remoteAddress||"";
  if(!["127.0.0.1","::1","::ffff:127.0.0.1"].includes(remote))return json(res,403,{error:"loopback only"});
  if(req.method==="GET"&&req.url==="/health")return json(res,200,{ok:true,service:"333-network-sovereign-terminal",host:HOST,port:PORT,networkAuthority:false,publicPublishing:false,stosAuthority:false});
  if(req.method==="POST"&&req.url==="/pair"){
    if(attempts>=5)return json(res,423,{error:"pairing locked"});
    attempts++;
    try{const b=await body(req,4096);if(String(b.code)!==pairingCode)return json(res,403,{error:"pairing denied",attempts});pairedToken=crypto.randomBytes(32).toString("base64url");audit({type:"owner.paired"});return json(res,200,{token:pairedToken})}catch{return json(res,400,{error:"invalid request"})}
  }
  const token=req.headers["x-333-session"];
  if(!pairedToken||token!==pairedToken)return json(res,401,{error:"owner pairing required"});
  if(req.method==="GET"&&req.url==="/api/status"){
    const namespaces={}; for(const ns of ALLOWED){try{const x=load(ns,key);namespaces[ns]={revision:x.revision,updatedAt:x.updatedAt}}catch{namespaces[ns]={error:"unreadable"}}}
    return json(res,200,{namespaces});
  }
  const m=req.url?.match(/^\/api\/([a-z0-9-]+)\/snapshot$/);
  if(m&&ALLOWED.has(m[1])){
    const ns=m[1];
    if(req.method==="GET"){try{return json(res,200,load(ns,key))}catch(e){return json(res,500,{error:"snapshot unreadable"})}}
    if(req.method==="POST"){try{const b=await body(req);const out=save(ns,key,b.expectedRevision,b.payload);return json(res,200,{revision:out.revision,updatedAt:out.updatedAt})}catch(e){if(e.code==="CONFLICT")return json(res,409,{error:"revision conflict",currentRevision:e.currentRevision});return json(res,400,{error:e.message})}}
  }
  if(req.method==="GET"&&req.url==="/api/audit"){
    const lines=fs.existsSync(AUDIT_PATH)?fs.readFileSync(AUDIT_PATH,"utf8").trim().split("\n").filter(Boolean).slice(-250).map(x=>JSON.parse(x)):[];
    return json(res,200,{events:lines});
  }
  return json(res,404,{error:"not found"});
});
server.on("error",e=>fail(e.message));
server.listen(PORT,HOST,()=>audit({type:"terminal.started",port:PORT}));
for(const sig of ["SIGINT","SIGTERM"])process.on(sig,()=>server.close(()=>process.exit(0)));
