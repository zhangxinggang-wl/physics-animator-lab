const {chromium}=require('playwright');
(async()=>{
 const b=await chromium.launch();const p=await b.newPage();
 await p.goto('file:///'+process.argv[2].replace(/\\/g,'/'));
 await p.waitForTimeout(3500);
 const r=await p.evaluate(()=>Array.from(document.querySelectorAll('merror')).map(e=>e.textContent.slice(0,90)));
 console.log(JSON.stringify(r,null,1));
 await Promise.race([b.close(),new Promise(s=>setTimeout(s,5000))]);process.exit(0);
})();
