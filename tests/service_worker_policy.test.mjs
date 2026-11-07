// D04: exercise the real service-worker policy with in-memory mocks only.
// Run with: node --test tests/service_worker_policy.test.mjs
// No browser profile, network, data storage or STOS connection required.
import assert from "node:assert/strict";
import test from "node:test";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const source = fs.readFileSync(path.join(root, "service-worker.js"), "utf8");
const scope = "https://vervenveda.com/333.github.io/";
const listeners = new Map();
const worker = {
  registration: { scope },
  location: { origin: "https://vervenveda.com" },
  addEventListener(name, fn) { listeners.set(name, fn); },
};
const sandbox = { self: worker, URL, Request, Response, Headers, console };
vm.runInNewContext(source + "\n;globalThis.policyUnderTest={approvedPublicCacheRequest,approvedPublicCacheResponse};", sandbox);
const policy = sandbox.policyUnderTest;

function request(target, { method = "GET", auth = false, mode = "cors" } = {}) {
  return {
    method,
    url: new URL(target, scope).href,
    mode,
    headers: new Headers(auth ? { Authorization: "Bearer fixture-only" } : {}),
  };
}
function response({ cacheControl = "", contentType = "text/html", cookie = false } = {}) {
  const headers = new Headers({ "Content-Type": contentType });
  if (cacheControl) headers.set("Cache-Control", cacheControl);
  if (cookie) headers.set("Set-Cookie", "session=fixture");
  return { ok: true, type: "basic", headers };
}

test("core application pages and listed offline shell remain cacheable", () => {
  for (const target of [
    "./index.html", "./offline.html", "./app/HOLLO_333_direct_connect_index.html",
    "./app/FleaPit™_media_gate_Index.html", "./app/FleaPit™ _media_hub_index.html"
  ]) assert.equal(policy.approvedPublicCacheRequest(request(target, { mode: "navigate" })), true, target);
});

test("unknown navigation paths and out-of-scope URLs cannot enter runtime cache", () => {
  for (const target of ["./member/dashboard", "./secret/page.html", "https://other.example/file.js", "/api/v1/account/profile"]) {
    assert.equal(policy.approvedPublicCacheRequest(request(target, { mode: "navigate" })), false, target);
  }
});

test("authorised, query-bearing and non-GET requests are refused", () => {
  assert.equal(policy.approvedPublicCacheRequest(request("./index.html", { auth: true })), false);
  assert.equal(policy.approvedPublicCacheRequest(request("./index.html?session=secret")), false);
  assert.equal(policy.approvedPublicCacheRequest(request("./index.html", { method: "POST" })), false);
});

test("public static assets are allowed but sensitive resource namespaces are blocked", () => {
  assert.equal(policy.approvedPublicCacheRequest(request("./assets/site.css")), true);
  assert.equal(policy.approvedPublicCacheRequest(request("./assets/icon.png")), true);
  assert.equal(policy.approvedPublicCacheRequest(request("./api/private.js")), false);
  assert.equal(policy.approvedPublicCacheRequest(request("./auth/session.js")), false);
  assert.equal(policy.approvedPublicCacheRequest(request("./member/profile.js")), false);
});

test("private, non-store, non-cache, cookies, and JSON responses cannot be cached", () => {
  assert.equal(policy.approvedPublicCacheResponse(response()), true);
  for (const cacheControl of ["private", "no-store", "no-cache", "public, private, max-age=0"]) {
    assert.equal(policy.approvedPublicCacheResponse(response({ cacheControl })), false);
  }
  assert.equal(policy.approvedPublicCacheResponse(response({ cookie: true })), false);
  assert.equal(policy.approvedPublicCacheResponse(response({ contentType: "application/json" })), false);
  assert.equal(policy.approvedPublicCacheResponse(response({ contentType: "text/event-stream" })), false);
});

test("offline worker still retains fetch/install/activate handlers", () => {
  for (const event of ["install", "activate", "fetch", "message"]) assert.equal(listeners.has(event), true);
});
