const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
const BG='152A1F', GOLD='C9A84C', LGOLD='E8C96B', CREAM='F5EDE0', MUTED='8FA898';
const SERIF='Palatino Linotype', SANS='Calibri';
const W=13.33, H=7.5;

function eyebrow(s,t){s.addText(t,{x:0,y:0.42,w:W,h:0.35,fontFace:SANS,fontSize:13,bold:true,color:GOLD,charSpacing:4,align:'center',margin:0});}
function pg(s,n){s.addText(n,{x:W-1.3,y:0.42,w:0.7,h:0.35,fontFace:SANS,fontSize:12,bold:true,color:LGOLD,align:'right',margin:0});}

// COVER - centered
let s=pres.addSlide(); s.background={color:BG};
eyebrow(s,'THE GOOD, THE BAD & THE UGLY  \u00b7  EP.1');
s.addText('Off-plan is sold on projections.',{x:0,y:2.2,w:W,h:0.9,fontFace:SERIF,fontSize:40,color:CREAM,align:'center',margin:0});
s.addText('Let\u2019s see if they come true.',{x:0,y:3.1,w:W,h:1.2,fontFace:SERIF,fontSize:54,bold:true,color:LGOLD,align:'center',margin:0});
s.addText('A REAL UNIT  \u00b7  A REAL STATEMENT OF ACCOUNT  \u00b7  REAL TRANSACTIONS',{x:0,y:4.6,w:W,h:0.4,fontFace:SANS,fontSize:15,bold:true,color:CREAM,charSpacing:3,align:'center',margin:0});
s.addText('Calum MacLeod  \u00b7  @uaecalum',{x:0,y:6.7,w:W,h:0.4,fontFace:SANS,fontSize:14,color:MUTED,align:'center',margin:0});

// P1 unit - photo, centered lower block
s=pres.addSlide();
s.addImage({path:'house169.jpg',x:0,y:0,w:W,h:H});
s.addShape(pres.ShapeType.rect,{x:0,y:0,w:W,h:H,fill:{color:BG,transparency:45}});
eyebrow(s,'THE UNIT'); pg(s,'01');
s.addText('4 Bed Townhouse',{x:0,y:4.5,w:W,h:0.8,fontFace:SERIF,fontSize:44,bold:true,color:CREAM,align:'center',margin:0});
s.addText('Costa Brava  \u00b7  DAMAC Lagoons',{x:0,y:5.4,w:W,h:0.5,fontFace:SERIF,fontSize:26,color:LGOLD,align:'center',margin:0});
s.addText('BOUGHT JANUARY 2022      \u00b7      50/50 PAYMENT PLAN',{x:0,y:6.2,w:W,h:0.4,fontFace:SANS,fontSize:16,bold:true,color:CREAM,charSpacing:3,align:'center',margin:0});

// P2 series - centered
s=pres.addSlide(); s.background={color:BG};
eyebrow(s,'THE SERIES'); pg(s,'02');
s.addText('The Good, the Bad',{x:0,y:2.6,w:W,h:1.0,fontFace:SERIF,fontSize:52,bold:true,color:CREAM,align:'center',margin:0});
s.addText('& the Ugly.',{x:0,y:3.6,w:W,h:1.0,fontFace:SERIF,fontSize:52,bold:true,color:LGOLD,align:'center',margin:0});

// P3 SOA - wider crop, centered
s=pres.addSlide(); s.background={color:'111111'};
const soaH = 6.9, soaW = soaH*(1179/1094);
s.addImage({path:'soa_wide.png',x:(W-soaW)/2,y:(H-soaH)/2+0.15,w:soaW,h:soaH});
s.addText('THE ACTUAL STATEMENT OF ACCOUNT',{x:0,y:0.18,w:W,h:0.35,fontFace:SANS,fontSize:15,bold:true,color:LGOLD,charSpacing:3,align:'center',margin:0});
s.addText('03',{x:W-1.0,y:0.18,w:0.6,h:0.35,fontFace:SANS,fontSize:12,bold:true,color:LGOLD,align:'right',margin:0});

// P4/P5 transactions
function txSlide(n,img,head,cap){
  const s=pres.addSlide(); s.background={color:'111111'};
  const h = W*(310/950);
  s.addImage({path:img,x:0,y:(H-h)/2-0.3,w:W,h:h});
  s.addText(head,{x:0,y:0.5,w:W,h:0.4,fontFace:SANS,fontSize:16,bold:true,color:LGOLD,charSpacing:3,align:'center',margin:0});
  s.addText(n,{x:W-1.0,y:0.5,w:0.6,h:0.35,fontFace:SANS,fontSize:12,bold:true,color:LGOLD,align:'right',margin:0});
  s.addText(cap,{x:0,y:6.3,w:W,h:0.5,fontFace:SERIF,fontSize:18,color:CREAM,align:'center',margin:0});
}
txSlide('04','recent_tx.png','SELLING TODAY - LAST 7 DAYS','Four title deeds \u00b7 4 beds \u00b7 Costa Brava \u00b7 15-17 Jul 2026 - coming out of the conflict window');
txSlide('05','preconflict_tx.png','BEFORE THE CONFLICT - FEB / MAR','Same community, same bed count - four deeds, Feb-Mar 2026');

// P6/P7 maths - FIXED param bug
function maths(pgN, tag, avg, profit, roi, roe, irr, foot){
  const s=pres.addSlide(); s.background={color:BG};
  eyebrow(s,tag); pg(s,pgN);
  const L=[['Average of the 4 sales',avg],['Purchase price (incl. 4% DLD)','\u01101,860,560'],['Actually paid in (50% + DLD)','\u0110966,100'],['Still owed at handover','\u0110894,500']];
  let y=1.6;
  for(const [k,v] of L){
    s.addText(k,{x:0.9,y:y,w:4.8,h:0.4,fontFace:SANS,fontSize:15,color:MUTED,margin:0});
    s.addText(v,{x:0.9,y:y+0.38,w:4.8,h:0.55,fontFace:SERIF,fontSize:26,bold:true,color:CREAM,margin:0});
    y+=1.15;
  }
  s.addText('PROFIT',{x:6.7,y:1.55,w:5.8,h:0.35,fontFace:SANS,fontSize:14,bold:true,color:GOLD,charSpacing:3,margin:0});
  s.addText(profit,{x:6.7,y:1.9,w:6.2,h:1.0,fontFace:SERIF,fontSize:50,bold:true,color:LGOLD,margin:0});
  const R=[['ROI on full price',roi],['ROE on cash in',roe],['IRR (annualised)',irr]];
  let y2=3.5;
  for(const [k,v] of R){
    s.addText(k,{x:6.7,y:y2,w:3.3,h:0.5,fontFace:SANS,fontSize:16,color:MUTED,margin:0});
    s.addText(v,{x:10.0,y:y2-0.1,w:2.7,h:0.6,fontFace:SERIF,fontSize:30,bold:true,color:CREAM,margin:0});
    y2+=0.95;
  }
  s.addText(foot,{x:0,y:6.6,w:W,h:0.45,fontFace:SERIF,fontSize:18,color:GOLD,align:'center',margin:0});
}
maths('06','THE MATHS - SELLING TODAY','\u01102,680,000','+\u0110819,440','44%','85%','17.8%','Cash back at handover sale: \u01101,785,500 from \u0110966,100 in');
maths('07','THE MATHS - AT PRE-CONFLICT PRICES','\u01102,962,500','+\u01101,101,940','59%','114%','22.4%','The conflict knocked ~\u0110280K off the top - and it STILL returns 85% on cash');

// P8 verdict - centered
s=pres.addSlide(); s.background={color:BG};
eyebrow(s,'THE VERDICT'); pg(s,'08');
s.addText('Real numbers. Handing over now.',{x:0,y:2.0,w:W,h:0.9,fontFace:SERIF,fontSize:44,bold:true,color:CREAM,align:'center',margin:0});
s.addText('This one worked.',{x:0,y:3.0,w:W,h:0.9,fontFace:SERIF,fontSize:44,bold:true,color:LGOLD,align:'center',margin:0});
s.addText('Next episode: one that didn\u2019t.',{x:0,y:4.4,w:W,h:0.5,fontFace:SERIF,fontSize:24,color:CREAM,align:'center',margin:0});
s.addText('COMMENT THE PROJECT YOU WANT ON THE TABLE NEXT',{x:0,y:5.4,w:W,h:0.4,fontFace:SANS,fontSize:16,bold:true,color:GOLD,charSpacing:3,align:'center',margin:0});
s.addText('@uaecalum  \u00b7  +971 55 350 2699',{x:0,y:6.7,w:W,h:0.4,fontFace:SANS,fontSize:14,color:MUTED,align:'center',margin:0});

pres.writeFile({fileName:'lagoons-review-ep1.pptx'}).then(()=>console.log('written'));
