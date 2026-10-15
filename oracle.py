import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

NOMINAL=0.9

def battery_plan(max_volts,ah):
    if not pos(max_volts): return {"error":"the sticker volts must be above zero"}
    if not pos(ah): return {"error":"the amp-hours must be above zero"}
    nominal=max_volts*NOMINAL
    return {"nominal":r1(nominal),"wh":r1(nominal*ah)}

def render_battery(r,max_volts,ah):
    return ("The "+jsnum(max_volts)+" on the battery names the charge peak, not the running voltage; the pack runs at about "
            +jsnum(r["nominal"])+" volts, so the "+jsnum(ah)+" amp-hour sticker holds about "+jsnum(r["wh"])+" watt-hours.")

def runtime_plan(wh,watts,claimed):
    if not pos(wh): return {"error":"the watt-hours must be above zero"}
    if not pos(watts): return {"error":"the turbo draw must be above zero"}
    if not pos(claimed): return {"error":"the claimed minutes must be above zero"}
    minutes=wh/watts*60
    ratio=minutes/claimed*100
    if ratio>=90: verdict="the box is nearly honest"
    elif ratio>=60: verdict="the box rounds in its own favor"
    else: verdict="the box is marketing first"
    return {"minutes":r1(minutes),"pctOfClaim":r1(ratio),"verdict":verdict}

def render_runtime(r,wh,watts,claimed):
    return ("A pack holding "+jsnum(wh)+" watt-hours feeding "+jsnum(watts)+" turbo watts lasts about "+jsnum(r["minutes"])
            +" minutes, not the "+jsnum(claimed)+" on the box - "+jsnum(r["pctOfClaim"])+"% of the claim, and "+r["verdict"]+".")

def move_plan(cfm,mph):
    if not pos(cfm): return {"error":"the CFM must be above zero"}
    if not pos(mph): return {"error":"the MPH must be above zero"}
    if cfm>=550: band="wet mats and stuck-down leaves"
    elif cfm>=350: band="ordinary yard piles"
    else: band="light sweeping off hard surfaces"
    return {"band":band}

def render_move(r,cfm,mph):
    return ("At "+jsnum(cfm)+" CFM the blower moves "+r["band"]+"; the "+jsnum(mph)
            +" MPH was measured at the tip of the narrowest nozzle, where almost no air flows.")

cases=[]
def add(tool,args):
    if tool=="battery": r=battery_plan(*args); fn=render_battery
    elif tool=="runtime": r=runtime_plan(*args); fn=render_runtime
    else: r=move_plan(*args); fn=render_move
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(40,4),(20,2.5),(60,5),(18,2),(36,6),(56,4)]:
    add("battery",a)
for a in [(144,550,25),(45,400,20),(270,600,28),(201.6,700,20),(194.4,800,15),(32.4,300,15)]:
    add("runtime",a)
for a in [(500,130),(650,150),(300,200),(350,120),(549.9,190),(550,110)]:
    add("move",a)
add("battery",[0,4]); add("battery",[40,0]); add("battery",["lots",4])
add("runtime",[0,550,25]); add("runtime",[144,0,25]); add("runtime",[144,550,0]); add("runtime",[144,550,"ages"])
add("move",[0,130]); add("move",[500,0]); add("move",["some",130])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
