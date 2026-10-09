#!/usr/bin/env python3
"""Quad Report generator.
   python3 build_quad.py quad-config.json out.pptx"""
import json, sys, textwrap
try:
    from pptx import Presentation
except ImportError:
    sys.exit("This needs python-pptx.  Install it with:  pip install python-pptx")
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

INK   = RGBColor(0x18,0x1D,0x24); MUTED = RGBColor(0x62,0x6E,0x7C)
RULE  = RGBColor(0xD8,0xDE,0xE4); NAVY  = RGBColor(0x14,0x33,0x55)
TINT  = RGBColor(0xEC,0xF1,0xF6); BAND  = RGBColor(0xF6,0xF8,0xFA)
WHITE = RGBColor(0xFF,0xFF,0xFF); PALE  = RGBColor(0xBF,0xD2,0xE4)
GOOD  = RGBColor(0x10,0x6B,0x36); BAD   = RGBColor(0xA8,0x1F,0x1F)
WATCH = RGBColor(0xB0,0x6A,0x00)

WIDE = True
W = Inches(13.333) if WIDE else Inches(10)
H = Inches(7.5)
M, HDR, GUT, FOOT, QHD = Inches(0.24), Inches(0.80), Inches(0.18), Inches(0.20), Inches(0.42)
QW = (W - 2*M - GUT) / 2
QAV = H - M - HDR - Inches(0.10) - GUT - FOOT - M
QH_TOP, QH_BOT = int(QAV*0.49), int(QAV*0.51)

T_TITLE, T_QHEAD, T_QSUB = 23, 13.5, 9
T_VAL, T_NAME, T_BODY, T_META, T_LBL = 13, 11.5, 10, 9, 8

# ---------- hard content caps (the one-pager only works if these hold) ----------
CAP = {"kpi_status":84, "goal":72, "goal_status":84, "strategy":40,
       "theme":44, "how":88,
       "bullet":58, "process":86, "other":84}

# Write all content in American English (color, organize, formalize, analyze).

WARN = []

def clamp(s, n, field=""):
    s = " ".join((s or "").split())
    if len(s) <= n: return s
    WARN.append(f"truncated {field or 'text'} at {n} chars ({len(s)} given): {s[:46]}...")
    return s[:n-1].rstrip(" ,.;:")+"…"


# ---------- wording ----------
PLAIN = {
 "q1":("How We Did","The month, against plan"),
 "q2":("This Year's Goals","What we said we'd do by December"),
 "q3":("How We Get There","The work that moves the goals"),
 "q4":("What's On My Mind","Think, ask, decide, do"),
 "strategies":"The six things we're working on",
 "wins":"What went well","short":"What didn't",
 "process":"What's come off my desk",
 "topics":"What I want from the group",
 "think":"Worth thinking about","questions":"Questions I can't answer yet",
 "decisions":"Decisions I have to make","actions":"What I'm doing about it",
 "done":"DONE","stuck":"STUCK {m} MONTHS","stuck_short":"stuck",
 "ok":"on track","watch":"watch","behind":"behind",
 "foot":"KEY      Green = at or ahead of plan      Amber = missed by 5% or less      "
        "Red = missed by more than 5%      STUCK = no change for two months or more",
}
CLASSIC = {
 "q1":("Key Performance Indicators","(Historic Performance Outcomes)"),
 "q2":("Breakthrough Goals","(Future Performance Outcomes)"),
 "q3":("Core Strategies","(Which Best Drive Traction for Your Multi-year Journey)"),
 "q4":("Other \u2026","(The Next Most Traction Creating \u201cions\u201d of Your Journey)"),
 "strategies":"Core Strategies: Actions Ending in \u201cing\u201d",
 "wins":"Most Significant Accomplishments","short":"Most Significant Shortfalls vs. Desired Accomplishments",
 "process":"How\u2019s it going in building / improving processes in your position within the company?",
 "topics":"Conference Call Topics Application",
 "think":"Things to Think About","questions":"Questions to Ponder",
 "decisions":"Decisions to Make","actions":"Actions to Take",
 "done":"DONE","stuck":"STUCK {m} MONTHS","stuck_short":"stuck",
 "ok":"on track","watch":"watch","behind":"behind",
 "foot":"SMART: Specific, Measurable, Achievable, Results-Oriented, Time-Bound",
}

def L(cfg):
    """Label set, with optional per-report overrides from the config.
       "label_overrides": {"q1": ["How We Did", "Rolling 3 months, on hours worked"]}"""
    base = dict(CLASSIC if cfg.get("labels")=="classic" else PLAIN)
    for k, v in (cfg.get("label_overrides") or {}).items():
        base[k] = tuple(v) if isinstance(v, list) else v
    return base

# ---------- primitives ----------
def tbox(slide,l,t,w,h,pad=0.07,anchor=MSO_ANCHOR.TOP):
    tf = slide.shapes.add_textbox(l,t,w,h).text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(pad)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    tf.vertical_anchor = anchor
    return tf

def P(tf,before=0,first=False,indent=0,align=PP_ALIGN.LEFT):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(before); p.space_after = Pt(0)
    if indent:
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(int(Inches(indent)))); pPr.set('indent','0')
    return p

def R(p,text,size=T_BODY,bold=False,color=INK,italic=False):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = "Calibri"

def line(tf,text,size=T_BODY,bold=False,color=INK,before=0,first=False,
         italic=False,indent=0,align=PP_ALIGN.LEFT):
    R(P(tf,before,first,indent,align),text,size,bold,color,italic)

def rect(slide,l,t,w,h,fill=None,line_col=None,lw=0.75):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,l,t,w,h)
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb = fill
    if line_col is None: s.line.fill.background()
    else: s.line.color.rgb = line_col; s.line.width = Pt(lw)
    s.shadow.inherit = False; s.text_frame.text = ""
    return s

def panel(slide,l,t,w,h,num,title,sub,edge="top",side="left"):
    """One quadrant. Sherpa original puts the heading on the OUTER edge of the
       page (top row headed at the top, bottom row headed at the bottom) with the
       numeral pointing in toward the centre cross. edge: top|bottom. side: left|right."""
    rect(slide,l,t,w,h,WHITE,RULE)
    hy = t if edge=="top" else t+h-QHD
    rect(slide,l,hy,w,QHD,TINT,None)
    rect(slide,l,hy,Inches(0.055),QHD,NAVY,None)
    hd = tbox(slide,l+Inches(0.06),hy,w-Inches(0.12),QHD,anchor=MSO_ANCHOR.MIDDLE)
    if side=="left":
        p = P(hd,first=True,align=PP_ALIGN.RIGHT)
        R(p,f"{sub}      ",T_QSUB,False,MUTED,italic=True)
        R(p,f"{num})  ",T_QHEAD,True,MUTED); R(p,title,T_QHEAD,True,NAVY)
    else:
        p = P(hd,first=True)
        R(p,f"{num})  ",T_QHEAD,True,MUTED); R(p,title,T_QHEAD,True,NAVY)
        R(p,f"      {sub}",T_QSUB,False,MUTED,italic=True)
    cy = t+QHD+Inches(0.05) if edge=="top" else t+Inches(0.05)
    return (l+Inches(0.02), cy, w-Inches(0.04), h-QHD-Inches(0.09))

def sect(slide,l,t,w,label,color=NAVY):
    """Small-caps section label with a hairline under it. Returns y below it.
       Grows to two lines when the label is too long for the column, so the
       classic Sherpa wording (which is wordy) never collides with the bullets."""
    import math
    per_line = max(int(w/914400 * 15.5), 10)          # chars that fit at 8pt bold caps
    rows = max(1, math.ceil(len(label)/per_line))
    bh = Inches(0.17) + Inches(0.115)*(rows-1)
    tf = tbox(slide,l,t,w,bh,pad=0.04)
    line(tf,label.upper(),T_LBL,bold=True,color=color,first=True)
    rect(slide,l+Inches(0.04),t+bh-Inches(0.015),w-Inches(0.08),Inches(0.008),RULE,None)
    return t+bh+Inches(0.01)

# ---------- formatting ----------
def money(v):
    a=abs(v); sg="-" if v<0 else ""
    if a>=1_000_000: return f"{sg}${a/1_000_000:,.2f}M"
    if a>=1_000:     return f"{sg}${a/1_000:,.1f}K"
    return f"{sg}${a:,.0f}"

def val(v,u):
    if v is None: return "n/a"
    if u=="$": return money(v)
    if u=="%": return f"{v:,.1f}%"
    if u=="#": return f"{v:,.0f}"
    return f"{v:,.1f} {u}"

def var(a,t,u,hib=True,band=0.05):
    """Returns (text, color, state). state: good | watch | bad.
       watch = missed the target by 5% or less of its value."""
    if a is None or t is None: return "",INK,"good"
    d=a-t; good=(d>=0) if hib else (d<=0)
    if u=="%": s=f"{d:+,.1f} pts"
    elif u=="$": s=("+" if d>=0 else "-")+money(abs(d)).lstrip("-")
    elif u=="#": s=f"{d:+,.0f}"
    else: s=f"{d:+,.1f} {u}"
    if t: s+=f"  ({d/abs(t)*100:+,.0f}%)"
    if good: return s,GOOD,"good"
    miss = abs(d)/abs(t) if t else 1.0
    if miss <= band: return s,WATCH,"watch"
    return s,BAD,"bad"

def trend(k):
    t=k.get("trend") or {}
    d=t.get("direction")
    if not d: return ""
    word={"up":"rising","down":"falling","flat":"flat"}.get(d,d)
    s=t.get("label") or word
    if t.get("months"): s+=f" {t['months']} months"
    return s

# ---------- quadrant i : KPI stat rows ----------
def q1(slide,box,cfg):
    lab=L(cfg); l,t,w,h = box
    ks = cfg.get("kpis",[])[:5]
    rh = h/max(len(ks),1)
    for i,k in enumerate(ks):
        y = t + i*rh
        if i % 2 == 0: rect(slide,l,y,w,rh,BAND,None)
        u = k.get("unit","$")
        v,vc,state = var(k.get("actual"),k.get("target"),u,k.get("higher_is_better",True))
        rect(slide,l,y+Inches(0.03),Inches(0.045),rh-Inches(0.06),vc,None)
        tf = tbox(slide,l+Inches(0.08),y,w-Inches(0.10),rh,pad=0.05)
        p = P(tf,first=True)
        R(p,val(k.get("actual"),u)+"   ",T_VAL,True,INK)
        R(p,k["name"],T_NAME,True,NAVY)
        R(p,f"     plan {val(k.get('target'),u)}",T_META,False,MUTED)
        if v: R(p,f"     {v}",T_META,True,vc)
        R(p,f"     {lab[{'good':'ok','watch':'watch','bad':'behind'}[state]]}",T_META,True,vc)
        tr=trend(k)
        if tr: R(p,f"     {tr}",T_META,False,MUTED)
        if k.get("status"):
            line(tf,clamp(k["status"],CAP["kpi_status"]),T_BODY,color=MUTED,before=2)

# ---------- quadrant ii : goals ----------
def q2(slide,box,cfg):
    """Two shapes supported:
       themed  {theme, bullets:[...], flag, stalled_months}
       simple  {goal, status, flag, stalled_months}"""
    lab=L(cfg); l,t,w,h = box
    gs = cfg.get("breakthrough_goals",[])[:5]
    rh = h/max(len(gs),1)
    for i,g in enumerate(gs):
        y = t + i*rh
        if i % 2 == 0: rect(slide,l,y,w,rh,BAND,None)
        flag = g.get("flag")
        col = GOOD if flag in ("done","closed") else (BAD if flag=="stalled" else PALE)
        rect(slide,l,y+Inches(0.03),Inches(0.045),rh-Inches(0.06),col,None)
        tf = tbox(slide,l+Inches(0.08),y,w-Inches(0.10),rh,pad=0.05)
        p = P(tf,first=True)
        if g.get("theme"):
            R(p,f"{i+1}.  ",T_NAME,True,MUTED)
            R(p,clamp(g["theme"],CAP["theme"]).upper(),11,True,NAVY)
        else:
            R(p,f"{i+1}.  ",T_NAME,True,MUTED)
            R(p,clamp(g.get("goal",""),CAP["goal"]),T_NAME,True,NAVY)
        if flag in ("done","closed"):
            R(p,"   "+lab["done"],T_LBL,True,GOOD)
        elif flag=="stalled":
            R(p,"   "+lab["stuck"].format(m=g.get("stalled_months","2")),T_LBL,True,BAD)
        if g.get("theme"):
            for b in g.get("bullets",[])[:2]:
                line(tf,"\u2022  "+clamp(b,CAP["how"]),T_META,color=MUTED,
                     before=1,indent=0.22)
        elif g.get("status"):
            line(tf,clamp(g["status"],CAP["goal_status"]),T_BODY,color=MUTED,
                 before=2,indent=0.22)

# ---------- quadrant iii : status, then the strategies box ----------
def q3(slide,box,cfg):
    """Sherpa order: accomplishments, shortfalls, the process question, and the
       numbered Core Strategies in a boxed strip at the foot of the quadrant."""
    l,t,w,h = box
    cw = (w - Inches(0.12))/2
    H_STAT, H_PROC, H_STRAT = Inches(1.06), Inches(0.36), Inches(0.86)
    lab=L(cfg)
    su = cfg.get("strategy_status",{})
    for c,(hd,key,col) in enumerate([(lab["wins"],"accomplishments",GOOD),
                                     (lab["short"],"shortfalls",BAD)]):
        x = l+c*(cw+Inches(0.12))
        yy = sect(slide,x,t,cw,hd,col)
        tf = tbox(slide,x,yy,cw,H_STAT-Inches(0.18),pad=0.05)
        first=True
        for i_a,a in enumerate(su.get(key,[])[:3]):
            line(tf,"\u2022  "+clamp(a,CAP["bullet"]),T_BODY,
                 before=0 if first else 3,first=first); first=False
        if first:
            for j in range(3):
                line(tf,"\u2022  "+"\u00a0"*30,T_BODY,color=RULE,
                     before=0 if j==0 else 3,first=(j==0))
    yp = sect(slide,l,t+H_STAT,w,lab["process"],MUTED)
    tf = tbox(slide,l,yp,w,H_PROC-Inches(0.18),pad=0.05)
    line(tf,clamp(su.get("process") or "\u00a0"*60,CAP["process"]),T_BODY,
         color=MUTED if su.get("process") else RULE,first=True)
    ys = t+H_STAT+H_PROC
    rect(slide,l,ys,w,H_STRAT,BAND,RULE)
    yy = sect(slide,l+Inches(0.04),ys+Inches(0.03),w-Inches(0.08),lab["strategies"],NAVY)
    sts = cfg.get("core_strategies",[])[:6]
    for c in (0,1):
        tf = tbox(slide,l+Inches(0.04)+c*(cw+Inches(0.04)),yy,cw,
                  H_STRAT-Inches(0.24),pad=0.05)
        first=True
        for i in range(c*3, c*3+3):
            st = sts[i] if i < len(sts) else ""
            txt = st if isinstance(st,str) else st.get("text","")
            p = P(tf,before=0 if first else 3,first=first); first=False
            R(p,f"{i+1}.  ",T_BODY,True,MUTED)
            R(p,clamp(txt,CAP["strategy"]) if txt else "\u00a0"*22,T_BODY,False,
              INK if txt else RULE)
            if isinstance(st,dict) and st.get("flag")=="stalled":
                R(p,"   "+lab["stuck_short"],T_LBL,True,BAD)

# ---------- quadrant iv : stacked blocks + topics line ----------
def q4(slide,box,cfg):
    lab=L(cfg); l,t,w,h = box
    o = cfg.get("other",{})
    BH = Inches(0.52)
    blocks=[(lab["think"],"think"),(lab["questions"],"questions"),
            (lab["decisions"],"decisions"),(lab["actions"],"actions")]
    for i,(hd,key) in enumerate(blocks):
        y = t + i*BH
        yy = sect(slide,l,y,w,hd)
        tf = tbox(slide,l,yy,w,BH-Inches(0.18),pad=0.05)
        items = o.get(key,[])[:2]
        if not items:
            # Quadrant iv is the owner's own thinking. Ship it blank with
            # writing lines rather than generating plausible-sounding content.
            for j in range(2):
                line(tf,"\u2022  "+"\u00a0"*46,T_BODY,color=RULE,
                     before=0 if j==0 else 2,first=(j==0))
        first=True
        for it in items:
            line(tf,"\u2022  "+clamp(it,CAP["other"]),T_BODY,
                 before=0 if first else 2,first=first); first=False
    ys = t + 4*BH
    rect(slide,l+Inches(0.04),ys,w-Inches(0.08),Inches(0.008),RULE,None)
    tf = tbox(slide,l,ys+Inches(0.02),w,Inches(0.22),pad=0.05)
    p = P(tf,first=True)
    R(p,lab["topics"].upper()+"    ",T_LBL,True,NAVY)
    topics=(o.get("call_topics") or [])+["","",""]
    for i,t2 in enumerate(topics[:3],1):
        R(p,f" {i}.  ",T_BODY,True,MUTED)
        R(p,(clamp(t2,30) if t2 else "\u00a0"*14)+"    ",T_BODY,False,
          INK if t2 else RULE)

# ---------- validation ----------
LIMITS = [("kpis",5),("breakthrough_goals",4),("core_strategies",6)]

def validate(cfg):
    """Say what will be dropped rather than dropping it quietly."""
    for key,mx in LIMITS:
        n=len(cfg.get(key) or [])
        if n>mx: WARN.append(f"{key}: {n} supplied, only the first {mx} render")
    su=cfg.get("strategy_status",{}) or {}
    for key in ("accomplishments","shortfalls"):
        n=len(su.get(key) or [])
        if n>3: WARN.append(f"strategy_status.{key}: {n} supplied, only the first 3 render")
    o=cfg.get("other",{}) or {}
    for key in ("think","questions","decisions","actions"):
        n=len(o.get(key) or [])
        if n>2: WARN.append(f"other.{key}: {n} supplied, only the first 2 render")
    if len(o.get("call_topics") or [])>3:
        WARN.append("other.call_topics: only the first 3 render")
    if any(o.get(k) for k in ("think","questions","decisions","actions")):
        WARN.append("quadrant iv has content. It is meant to be the owner's own "
                    "writing; ship it blank unless they wrote this themselves.")
    for k in (cfg.get("kpis") or [])[:5]:
        if k.get("actual") is None or k.get("target") is None:
            WARN.append(f"KPI '{k.get('name')}' is missing an actual or a target")

# ---------- page ----------
def build(cfg,out):
    prs=Presentation(); prs.slide_width, prs.slide_height = W,H
    slide=prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide,0,0,W,HDR,NAVY,None)
    t=tbox(slide,M,0,W-2*M,HDR,pad=0.02,anchor=MSO_ANCHOR.MIDDLE)
    p=P(t,first=True)
    R(p,f"Quad Report {cfg.get('year','')}",T_TITLE,True,WHITE)
    R(p,f"       {cfg.get('theme','')}",13,False,PALE,italic=True)
    p2=P(t,before=3)
    R(p2,cfg.get('report_by',''),T_META,True,WHITE)
    R(p2,f"      {cfg.get('period','')}",T_META,False,PALE)
    R(p2,f"      {cfg.get('date','')}",T_META,False,PALE)
    if cfg.get("vision"):
        R(p2,f"      \u2192  {clamp(cfg['vision'],90)}",T_META,False,PALE,italic=True)

    top=HDR+Inches(0.10); left2=M+QW+GUT; top2=top+QH_TOP+GUT
    lab=L(cfg)
    # Sherpa layout: iv top-left, iii top-right, i bottom-left, ii bottom-right.
    # Headings sit on the outer edge of the page, numerals pointing inward.
    q4(slide,panel(slide,M,    top, QW,QH_TOP,"iv", *lab["q4"],edge="top",   side="left"), cfg)
    q3(slide,panel(slide,left2,top, QW,QH_TOP,"iii",*lab["q3"],edge="top",   side="right"),cfg)
    q1(slide,panel(slide,M,    top2,QW,QH_BOT,"i",  *lab["q1"],edge="bottom",side="left"), cfg)
    q2(slide,panel(slide,left2,top2,QW,QH_BOT,"ii", *lab["q2"],edge="bottom",side="right"),cfg)

    f=tbox(slide,M,H-FOOT-Inches(0.02),W-2*M,FOOT,pad=0.02)
    fp=P(f,first=True)
    R(fp,"\u00a9 Sherpa Alliance, 2004",T_LBL,False,MUTED)
    R(fp,"            "+lab["foot"],T_LBL,False,MUTED)
    prs.save(out); return out

if __name__=="__main__":
    if len(sys.argv)<3:
        sys.exit("usage: python3 build_quad.py <config.json> <out.pptx>")
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    validate(cfg)
    build(cfg, sys.argv[2])
    if WARN:
        print("Warnings:", file=sys.stderr)
        for w in dict.fromkeys(WARN): print("  - "+w, file=sys.stderr)
    print(f"wrote {sys.argv[2]}  ({len(dict.fromkeys(WARN))} warning(s))")
