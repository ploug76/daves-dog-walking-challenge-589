# Pop-up overlap test for Dave's Dog Walking Challenge: start tip / hint / dog-info boxes, floats, HUD panels, buttons.
import sys,asyncio,json
from playwright.async_api import async_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8800/daves-dog-walking-challenge/'
VIEWS=[(390,844,None),(375,667,None),(430,932,None),(390,844,{'t':47,'b':34})]
JS=r'''(L)=>{const T=__T;T.startLevel(L);T.setState('play');const lv=T.lv(),sol=T.sol();const ov=(a,b)=>a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h;
 const HUD=[{x:6,y:56,w:180,h:38,k:'clock'},{x:214,y:56,w:180,h:38,k:'sunset'},{x:6,y:100,w:150,h:22,k:'leash'},{x:300,y:100,w:94,h:22,k:'earned'},{x:0,y:542,w:400,h:178,k:'panel'}];
 const btns=()=>[...document.querySelectorAll('.tb')].filter(e=>getComputedStyle(e).display!='none').map(e=>{const b=e.getBoundingClientRect(),Ly=T.layout();return{x:(b.left-Ly.OXs)/Ly.SC,y:(b.top-Ly.OYs)/Ly.SC,w:b.width/Ly.SC,h:b.height/Ly.SC,k:'btn'}});
 let frames=0;const bad=[];const check=()=>{frames++;const Ly=T.layout(),O=Ly.ov,B=btns();
  for(let i=0;i<O.length;i++){for(let j=i+1;j<O.length;j++)if(ov(O[i],O[j]))bad.push(['ov-ov',O[i].k,O[j].k]);for(const h of HUD)if(ov(O[i],h))bad.push(['ov-'+h.k,O[i].k]);if(O[i].x<0||O[i].x+O[i].w>400)bad.push(['ov-edge'])}
  for(const h of HUD)for(const b of B)if(ov(h,b))bad.push(['hud-btn',h.k]);
  for(let k=0;k<Ly.nf;k++){const f={x:60,y:Ly.fy+k*24-15-4,w:280,h:25};for(const o of O)if(ov(f,o))bad.push(['float-ov',o.k]);if(k<3)for(const h of HUD)if(ov(f,h))bad.push(['float-'+h.k])}
  // the stack must not hide Dave / the house it talks about, unless neither slot is free
  const tg=[[Ly.dv[0],Ly.dv[1]-10]];if(Ly.hint!=null)tg.push(Ly.houses[Ly.hint]);if(Ly.sel>=0)tg.push(Ly.houses[Ly.sel]);
  if(O.length){const y0=O[0].y,y1=O[O.length-1].y+O[O.length-1].h;if(tg.some(([x,y])=>y+18>y0&&y-24<y1)){const tot=y1-y0;const top=tg.some(([x,y])=>y+18>128&&y-24<128+tot),bot=tg.some(([x,y])=>y+18>538-tot&&y-24<538);if(!(top&&bot))bad.push(['hides-target'])}}};
 check();T.getHint();check();T.select(Math.floor(Math.random()*lv.dogs.length));check();
 let cur=lv.home;for(const [k,i,len] of sol.plan){const node=lv.dogs[i].node,sp=lv.D[cur][node];let pad=len-sp;const nb=lv.A[cur].find(n=>lv.dogs.every(d=>d.node!=n))??lv.A[cur][0];while(pad>=2){T.addWaypoint(nb,false);T.addWaypoint(cur,false);pad-=2}T.addWaypoint(node,true);cur=node}
 let n=0;while(T.get().state=='play'&&n<60000){T.update(1/30);n++;if(n%12==0){const r=Math.random();if(r<.3)T.getHint();else if(r<.6)T.select(Math.floor(Math.random()*lv.dogs.length));else if(r<.7)T.select(-1);check()}}
 return{L,frames,overlaps:bad.length,sample:bad.slice(0,4)}}'''
async def main():
  tot=0;fr=0
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for (w,h,safe) in VIEWS:
      pg=await b.new_page(viewport={'width':w,'height':h},is_mobile=True,has_touch=True);errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
      if safe:await pg.add_init_script('window.__SAFE='+json.dumps(safe))
      await pg.goto(URL);await pg.wait_for_timeout(700);await pg.evaluate("document.querySelectorAll('.tb').forEach(e=>e.style.display='block')")
      for L in range(1,21):
        r=await pg.evaluate(JS,L);tot+=r['overlaps'];fr+=r['frames']
        if r['overlaps']:print(w,h,safe,r)
      if errs:print('ERR',errs);tot+=len(errs)
      print(f'{w}x{h} {"safe" if safe else ""} done');await pg.close()
    await b.close()
  print(f'TOTAL frames {fr} overlaps {tot}');sys.exit(1 if tot else 0)
asyncio.run(main())
