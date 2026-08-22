import puppeteer from 'puppeteer';
const b = await puppeteer.launch({ headless:'new', args:['--no-sandbox'] });
const p = await b.newPage(); await p.setViewport({width:1920,height:1080});
const errs=[];
p.on('pageerror', e => errs.push('PAGEERROR: '+e.message.slice(0,140)));
p.on('console', m => m.type()==='error' && errs.push('CONSOLE: '+m.text().slice(0,140)));
await p.goto('https://fortyguard-hackathon.vercel.app',{waitUntil:'networkidle0',timeout:60000});
await new Promise(r=>setTimeout(r,2500));
const tabs = await p.evaluate(()=>Array.from(document.querySelectorAll('nav button')).map(b=>b.textContent.trim()));
console.log('bundle:', await p.evaluate(()=>[...document.scripts].map(s=>s.src.split('/').pop()).filter(s=>s.startsWith('index'))[0]));
for (const t of tabs) {
  await p.evaluate((x)=>{Array.from(document.querySelectorAll('nav button')).find(b=>b.textContent.trim()===x)?.click();},t);
  await new Promise(r=>setTimeout(r,1800));
  const chars = await p.evaluate(()=>document.body.innerText.length);
  console.log(`${errs.length?'✗':'✓'} ${t.padEnd(22)} chars=${chars}`);
  if (errs.length) { errs.forEach(e=>console.log('     '+e)); errs.length=0; }
}
await b.close();
