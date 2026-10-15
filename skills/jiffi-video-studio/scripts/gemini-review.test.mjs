import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,writeFile,readFile,rm,open} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {options,prepare,main} from './gemini-review.mjs';

const dir=await mkdtemp(join(tmpdir(),'gemini-review-test-'));
const silence=join(dir,'misleading-funk-title.wav');
const tone=join(dir,'tone.wav');
const video=join(dir,'video.mp4');
const prompt=join(dir,'prompt.txt');
await writeFile(prompt,'Describe audible content.');
for (const [file,filter] of [[silence,'anullsrc=r=16000:cl=mono'],[tone,'sine=frequency=700:duration=1']]) {
  assert.equal(spawnSync('ffmpeg',['-v','error','-f','lavfi','-i',filter,'-t','1','-c:a','pcm_s16le',file]).status,0);
}
assert.equal(spawnSync('ffmpeg',['-v','error','-f','lavfi','-i','color=s=32x32:r=4:d=1','-c:v','libx264',video]).status,0);
const args=(file,out)=>['--media',file,'--prompt',prompt,'--out',join(dir,out),'--model','gemini-3.8-flash'];
const originalFetch=globalThis.fetch;
const oldKey=process.env.GEMINI_API_KEY;
process.env.GEMINI_API_KEY='fixture-secret-not-real';
let calls=0;
globalThis.fetch=async()=>{calls++;return {ok:true,status:200,json:async()=>({modelVersion:'fixture',candidates:[{finishReason:'STOP',content:{parts:[{text:'A tone. fixture-secret-not-real'}]}}],usageMetadata:{totalTokenCount:1}})};};

try {
  await test('reject malformed options and repeated media',()=>{
    assert.throws(()=>options([...args(tone,'bad'),'--fps','NaN']));
    assert.throws(()=>options([...args(tone,'bad'),'--media',tone]));
    assert.throws(()=>options([...args(tone,'bad'),'--unknown','x']));
  });
  await test('payload carries bytes, keeps filenames local, detects exact silence',async()=>{
    const p=await prepare(options(args(silence,'unused')));
    assert.equal(p.media[0].signal.all_samples_zero,true);
    assert.equal(Buffer.from(p.body.contents[0].parts[1].inlineData.data,'base64').compare(await readFile(silence)),0);
    assert.equal(JSON.stringify(p.body).includes('misleading-funk-title'),false);
  });
  await test('video sampling and absent audio are explicit',async()=>{
    const p=await prepare(options(args(video,'unused')));
    assert.equal(p.body.contents[0].parts[1].videoMetadata.fps,4);
    assert.equal(p.media[0].signal.has_audio_stream,false);
  });
  await test('silent result avoids network and never creates a model verdict',async()=>{
    const before=calls;await main(args(silence,'silent'));
    const r=JSON.parse(await readFile(join(dir,'silent/record.json')));
    assert.equal(calls,before);assert.equal(r.status,'local_silence_result');assert.equal(r.model_returned,null);
  });
  await test('successful call remains unverified, redacts credential, duplicate output blocks retry',async()=>{
    await main(args(tone,'success'));
    const r=JSON.parse(await readFile(join(dir,'success/record.json')));
    assert.equal(r.status,'complete');assert.equal(r.analysis_verdict,'unverified');
    assert.equal((await readFile(join(dir,'success/review.md'),'utf8')).includes('fixture-secret-not-real'),false);
    const before=calls;await assert.rejects(main(args(tone,'success')));assert.equal(calls,before);
  });
  await test('truncated response is incomplete',async()=>{
    globalThis.fetch=async()=>({ok:true,status:200,json:async()=>({candidates:[{finishReason:'MAX_TOKENS',content:{parts:[{text:'partial'}]}}]})});
    await assert.rejects(main(args(tone,'truncated')));
    assert.equal(JSON.parse(await readFile(join(dir,'truncated/record.json'))).status,'incomplete');
  });
  await test('network failure records uncertain billing without automatic retry',async()=>{
    let attempts=0;globalThis.fetch=async()=>{attempts++;throw new Error('fixture-secret-not-real');};
    await assert.rejects(main(args(tone,'timeout')),e=>!e.message.includes('fixture-secret-not-real'));
    assert.equal(attempts,1);assert.equal(JSON.parse(await readFile(join(dir,'timeout/record.json'))).status,'uncertain');
  });
  await test('HTTP errors are recorded without retry or secret response logging',async()=>{
    let attempts=0;globalThis.fetch=async()=>{attempts++;return {ok:false,status:429,json:async()=>({error:'fixture-secret-not-real'})};};
    await assert.rejects(main(args(tone,'limited')),/HTTP 429/);
    assert.equal(attempts,1);
    const r=await readFile(join(dir,'limited/record.json'),'utf8');
    assert.equal(JSON.parse(r).status,'http_error');assert.equal(r.includes('fixture-secret-not-real'),false);
  });
  await test('reject corrupt and oversized files before any network call',async()=>{
    const corrupt=join(dir,'bad.wav');await writeFile(corrupt,'not audio');
    await assert.rejects(prepare(options(args(corrupt,'corrupt'))));
    const huge=join(dir,'huge.wav');const f=await open(huge,'w');await f.truncate(80*1024*1024);await f.close();
    await assert.rejects(prepare(options(args(huge,'huge'))),/90 MiB/);
  });
} finally {
  globalThis.fetch=originalFetch;
  if(oldKey===undefined) delete process.env.GEMINI_API_KEY; else process.env.GEMINI_API_KEY=oldKey;
  await rm(dir,{recursive:true,force:true});
}
