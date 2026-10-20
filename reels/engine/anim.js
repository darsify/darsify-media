// Darsify reel engine — deterministic renderFrame(t) for frame-by-frame capture.
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), lerp=(a,b,t)=>a+(b-a)*t;
const eout=t=>1-Math.pow(1-clamp(t),3), ein=t=>Math.pow(clamp(t),3);
const eio=t=>{t=clamp(t);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;};
const back=t=>{t=clamp(t);const c1=1.7,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2);};
const $=id=>document.getElementById(id);
const num=(el,k,d=0)=>el.dataset[k]!==undefined?parseFloat(el.dataset[k]):d;

// ---------- one-time layout: fit headline lines to the safe width ----------
function fitLines(){
  document.querySelectorAll('[data-fit]').forEach(el=>{
    const max=parseFloat(el.dataset.fit); let fs=parseFloat(getComputedStyle(el).fontSize);
    el.style.whiteSpace='nowrap';
    for(let i=0;i<60 && el.scrollWidth>max;i++){fs*=0.96; el.style.fontSize=fs+'px';}
  });
}

function entry(el,lt){
  const a=el.dataset.a||'up', t0=num(el,'in'), dur=num(el,'dur',.45);
  const p=clamp((lt-t0)/dur); let o=lt<t0?0:1, tr='';
  const base=el.dataset.base||'';
  if(a==='up'){o=clamp(p*2.2); tr=`translateY(${(1-eout(p))*60}px)`;}
  else if(a==='down'){o=clamp(p*2.2); tr=`translateY(${-(1-eout(p))*60}px)`;}
  else if(a==='left'){o=clamp(p*2.2); tr=`translateX(${-(1-eout(p))*140}px)`;}
  else if(a==='right'){o=clamp(p*2.2); tr=`translateX(${(1-eout(p))*140}px)`;}
  else if(a==='pop'){o=clamp(p*3); tr=`scale(${lt<t0?.4:.4+.6*back(p)})`;}
  else if(a==='fade'){o=p;}
  else if(a==='stamp'){o=lt<t0?0:1; tr=`scale(${lerp(2.4,1,eout(clamp((lt-t0)/.18)))}) rotate(${num(el,'rot',-10)}deg)`;}
  else if(a==='drop'){const q=clamp((lt-t0)/.55); o=lt<t0?0:1; const y=-1200*(1-ein(q)); const b=q>=1?Math.max(0,Math.sin(Math.PI*clamp((lt-t0-.55)/.2)))*18:0;
    tr=`translateY(${y-b}px) rotate(${num(el,'rot',0)*(q)}deg)`;}
  else if(a==='zoom'){o=clamp(p*2); tr=`scale(${lerp(1.25,1,eout(p))})`;}
  if(el.dataset.out!==undefined){const q=clamp((lt-num(el,'out'))/.25); o*=1-q; if(el.dataset.outa==='up') tr+=` translateY(${-q*80}px)`; if(el.dataset.outa==='shrink') tr+=` scale(${1-q*.6})`;}
  if(el.dataset.float!==undefined && lt>t0){const f=num(el,'float'),ph=num(el,'ph',0); tr+=` translate(${Math.sin(lt*1.3+ph)*f}px,${Math.cos(lt*1.1+ph*1.7)*f}px) rotate(${Math.sin(lt*.9+ph)*2}deg)`;}
  el.style.opacity=o; el.style.transform=(base+' '+tr).trim();
}

function special(el,lt){
  if(el.dataset.type!==undefined){const [a,b]=el.dataset.type.split(',').map(Number); const s=el.dataset.text;
    const n=Math.round(s.length*clamp((lt-a)/(b-a))); el.textContent=s.slice(0,n); const c=el.nextElementSibling;
    if(c&&c.classList.contains('caret')) c.style.opacity=(lt<b+.3&&Math.floor(lt*3)%2)?1:0;}
  if(el.dataset.count!==undefined){const [a,b,f,t]=el.dataset.count.split(',').map(Number); const v=lerp(f,t,eio((lt-a)/(b-a)));
    const dec=num(el,'dec',0); let txt=dec?v.toFixed(dec):Math.round(v).toLocaleString('en-US'); if(el.dataset.clock){const r=Math.round(v); txt=Math.floor(r/60)+':'+String(r%60).padStart(2,'0');} el.textContent=(el.dataset.fmt||'{}').replace('{}',txt);}
  if(el.dataset.bar!==undefined){const [a,d,w]=el.dataset.bar.split(',').map(Number); el.style.width=(w*eio((lt-a)/d))+'%';}
  if(el.dataset.press!==undefined){const a=num(el,'press'); const pr=Math.max(0,Math.sin(Math.PI*clamp((lt-a)/.22))); el.style.transform=`scale(${1-.1*pr})`; el.style.filter=pr>0?`brightness(${1+.25*pr})`:'';}
  if(el.dataset.swap!==undefined){const a=num(el,'swap'); el.querySelectorAll(':scope > .sa').forEach(x=>x.style.display=lt<a?'':'none'); el.querySelectorAll(':scope > .sb').forEach(x=>x.style.display=lt<a?'none':'');
    if(el.dataset.swapcls){const [c1,c2]=el.dataset.swapcls.split('|'); el.className=el.className.replace(c1,'').replace(c2,'').trim()+' '+(lt<a?c1:c2);}}
  if(el.dataset.tick!==undefined){const a=num(el,'tick'); const p=eout((lt-a)/.25); el.querySelectorAll('path').forEach(pth=>pth.style.strokeDashoffset=1-p);
    if(el.dataset.fill){el.style.background=p>0?el.dataset.fill:'transparent'; el.style.borderColor=p>0?el.dataset.fill:'';}}
  if(el.dataset.strike!==undefined){const a=num(el,'strike'); el.style.setProperty('--sk',(eout((lt-a)/.3)*100)+'%');}
  if(el.dataset.shake!==undefined){const a=num(el,'shake'); if(lt>a&&lt<a+.5) el.style.transform+=` rotate(${Math.sin(lt*45)*3*(1-(lt-a)/.5)}deg)`;}
  if(el.dataset.hl!==undefined){const a=num(el,'hl'); el.style.setProperty('--hl',(eout((lt-a)/.35)*100)+'%');}
  if(el.dataset.spin!==undefined){const [a,b,deg]=el.dataset.spin.split(',').map(Number); el.style.transform=`rotate(${num(el,'r0',0)+deg*ein(clamp((lt-a)/(b-a)))}deg)`;}
  if(el.dataset.pulse!==undefined){el.style.opacity=.55+.45*Math.abs(Math.sin(lt*3));}
}

function setExpr(m,lt){
  const ex=JSON.parse(m.dataset.ex); let cur=ex[0][1]; for(const [t,e] of ex) if(lt>=t) cur=e;
  m.querySelectorAll('.ex').forEach(x=>x.style.opacity=x.dataset.e===cur?1:0);
}
function mascot(m,lt){
  const t0=num(m,'in'); const p=eout((lt-t0)/.6); const ph=num(m,'ph',0); const br=Math.sin(2*Math.PI*lt/2.0+ph);
  let y=(1-p)*420+br*4, sy=1+br*.012, r=0;
  const hop=m.dataset.hop!==undefined?num(m,'hop'):null;
  if(hop!==null&&lt>hop){const h=Math.abs(Math.sin(Math.PI*(lt-hop)/.5)); y-=h*42; sy+=(h-.5)*.04;}
  if(m.dataset.shake!==undefined){const a=num(m,'shake'); if(lt>a&&lt<a+.8) r=Math.sin(lt*30)*3;}
  if(m.dataset.jump!==undefined){m.dataset.jump.split(',').map(Number).forEach(a=>{const c=Math.max(0,Math.sin(Math.PI*clamp((lt-a)/.4))); y-=c*50; sy-=c*.03;});}
  if(m.dataset.out!==undefined){const q=clamp((lt-num(m,'out'))/.3); y+=ein(q)*500;}
  m.style.opacity=lt<t0?0:1; m.style.transform=`translateY(${y}px) rotate(${r}deg) scale(${num(m,'flip',1)*1},${sy})`;
  m.querySelectorAll('.arms').forEach(a=>{a.style.transformBox='view-box';a.style.transformOrigin='104px 160px';
    a.style.transform=`rotate(${Math.sin(2*Math.PI*lt/(hop!==null&&lt>hop?.5:2.0))*(hop!==null&&lt>hop?8:2.5)}deg)`;});
  setExpr(m,lt);
}

const SC=[...document.querySelectorAll('.scene')];
window.renderFrame=function(t){
  for(const s of SC){
    const a=num(s,'s'), b=num(s,'e'), lt=t-a, on=t>=a-.001&&t<b;
    if(!on){s.style.opacity=0; s.style.visibility='hidden'; continue;}
    s.style.visibility='visible';
    const tin=s.dataset.tin||'up'; const pin=eout(lt/.35); const pout=s.dataset.last?0:clamp((t-(b-.25))/.25);
    s.style.opacity=(tin==='cut'?1:clamp(lt/.2))*(1-pout);
    s.style.transform=tin==='cut'?'':(tin==='zoom'?`scale(${lerp(1.08,1,pin)})`:`translateY(${(1-pin)*70}px)`);
    s.querySelectorAll('[data-in]').forEach(el=>entry(el,lt));
    s.querySelectorAll('[data-type],[data-count],[data-bar],[data-press],[data-swap],[data-tick],[data-strike],[data-shake],[data-hl],[data-spin],[data-pulse]').forEach(el=>special(el,lt));
    s.querySelectorAll('.masc').forEach(m=>mascot(m,lt));
  }
  // background crossfade per scene family
  document.querySelectorAll('.bgl').forEach(l=>{const a=num(l,'s'),b=num(l,'e'); l.style.opacity=t<a?0:(t<b?clamp((t-a)/.3):1-clamp((t-b)/.3));});
  const w=$('wipe'); if(w){const a=num(w,'at'); const p=eio((t-a)/.45); w.style.clipPath=`circle(${p*120}% at 50% 62%)`; w.style.opacity=t<a?0:(t<a+.6?1:1-clamp((t-a-.6)/.3));}
};
window.addEventListener('load',()=>{fitLines(); window.renderFrame(0); window.ready=true;});
