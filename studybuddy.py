import tkinter as tk
from tkinter import messagebox
import json, os

FILE = "cards.json"
cards = json.load(open(FILE)) if os.path.exists(FILE) else []
save = lambda: json.dump(cards, open(FILE,"w"))
ri=[0]; ts=[1500]; tr=[False]; tj=[None]

BG,FG,DIM,GRAY = "#111111","#EEEEEE","#2A2A2A","#888888"
F=("Courier New",11)

root=tk.Tk(); root.title("[ STUDYBUDDY ]"); root.geometry("750x520"); root.configure(bg=BG)

nav=tk.Frame(root,bg="#000000",height=44); nav.pack(fill="x"); nav.pack_propagate(False)
tk.Label(nav,text="[ STUDYBUDDY ]",bg="#000000",fg=FG,font=("Courier New",14,"bold")).pack(side="left",padx=10)
tk.Label(nav,text="D=Dash  C=Create  R=Review  T=Timer",bg="#000000",fg=GRAY,font=("Courier New",9)).pack(side="right",padx=10)

area=tk.Frame(root,bg=BG); area.pack(fill="both",expand=True)
cur=[None]

def show(f):
    if cur[0]: cur[0].destroy()
    cur[0]=f; f.pack(fill="both",expand=True,padx=18,pady=12)

def L(p,t,fg=None,fs=11,bold=False):
    tk.Label(p,text=t,bg=BG,fg=fg or FG,font=("Courier New",fs,"bold"if bold else"normal"),
             wraplength=680,justify="left").pack(anchor="w",pady=1)

def B(p,t):
    tk.Label(p,text=t,bg=DIM,fg=FG,font=("Courier New",9),pady=4).pack(fill="x",pady=(2,6))

def btn(p,t,cmd,dim=False,side=None):
    b=tk.Button(p,text=f"[{t}]",bg=DIM if dim else FG,fg=BG if not dim else FG,
                font=F,relief="raised",padx=8,pady=3,command=cmd)
    b.pack(side=side,padx=3) if side else b.pack(anchor="w",pady=2)
    return b

def fmt(s): return f"{s//60:02d}:{s%60:02d}"

# DASHBOARD
def dash():
    f=tk.Frame(area,bg=BG)
    L(f,"MY CARDS",fs=20,bold=True)
    B(f,">> Flashcards + spaced repetition = study smarter. (IH#1)")
    B(f,"HOW TO: 1)Create  2)Review  3)Rate  4)Repeat  (IH#6)")
    for i,c in enumerate(cards):
        r=tk.Frame(f,bg=DIM,bd=2,relief="ridge"); r.pack(fill="x",pady=2)
        tk.Label(r,text=f"Q: {c['front'][:65]}",bg=DIM,fg=FG,font=F,anchor="w").pack(side="left",padx=8,pady=5)
        btn(r,"DEL",lambda i=i:delete(i),side="right")  # IH#8
    L(f,f"Total: {len(cards)} cards",GRAY); show(f)

def delete(i):
    if messagebox.askyesno("DELETE","Delete this card?\nCannot be undone."):  # IH#8 IH#2
        cards.pop(i); save(); dash()

# CREATE
def create():
    f=tk.Frame(area,bg=BG)
    L(f,"CREATE CARD",fs=20,bold=True)
    B(f,">> Write a question (front) and answer (back). (IH#1)")
    B(f,"STEPS: 1)Question  2)Answer  3)Save  (IH#6)")
    widgets={}
    for k in("FRONT","BACK"):
        L(f,f"{k}:",bold=True)
        t=tk.Text(f,height=3,font=F,bg=DIM,fg=FG,insertbackground=FG,relief="ridge",bd=2)
        t.pack(fill="x",pady=(1,8)); widgets[k]=t

    def do_save():
        q,a=widgets["FRONT"].get("1.0","end").strip(),widgets["BACK"].get("1.0","end").strip()
        if not q or not a: messagebox.showwarning("!","Both fields required."); return
        cards.append({"front":q,"back":a}); save()
        for w in widgets.values(): w.delete("1.0","end")
        messagebox.showinfo("OK","Saved!"); widgets["FRONT"].focus()

    r=tk.Frame(f,bg=BG); r.pack(anchor="w")
    btn(r,"SAVE",do_save,side="left")
    btn(r,"SAVE+ANOTHER",do_save,side="left")         # IH#7
    btn(r,"CLEAR",lambda:[w.delete("1.0","end")for w in widgets.values()],dim=True,side="left")  # IH#5
    btn(r,"CANCEL",dash,dim=True,side="left")          # IH#5
    show(f); widgets["FRONT"].focus()

# REVIEW
def review():
    if not cards: messagebox.showinfo("!","No cards yet!"); return
    ri[0]=0; show_card()

def show_card():
    f=tk.Frame(area,bg=BG); i,n=ri[0],len(cards)
    L(f,f"REVIEW [{i+1}/{n}]",fs=18,bold=True)
    pb=tk.Frame(f,bg=DIM,height=10); pb.pack(fill="x",pady=(4,10)); pb.pack_propagate(False)
    tk.Frame(pb,bg=FG,height=10).place(relwidth=(i+1)/n,relheight=1)  # IH#3 progress
    cf=tk.Frame(f,bg=DIM,bd=3,relief="ridge"); cf.pack(fill="x",ipady=14)
    tk.Label(cf,text=cards[i]["front"],bg=DIM,fg=FG,font=("Courier New",14,"bold"),
             wraplength=680,justify="center").pack(pady=(10,4))
    ans=tk.Label(cf,text="",bg=DIM,fg=FG,font=("Courier New",13),wraplength=680,justify="center"); ans.pack(pady=(0,4))
    hint=tk.Label(cf,text="(click card or [SHOW] to reveal)",bg=DIM,fg=GRAY,font=("Courier New",9)); hint.pack(pady=(0,10))
    rate=tk.Frame(f,bg=BG)

    def reveal(e=None):  # IH#3 hidden until ready, IH#7 two ways
        ans.config(text=f"A: {cards[i]['back']}"); hint.config(text="")
        sb.config(state="disabled"); rate.pack(pady=6)

    cf.bind("<Button-1>",reveal); ans.bind("<Button-1>",reveal)
    sb=btn(f,"SHOW ANSWER",reveal)
    tk.Label(rate,text="HOW WELL?",bg=BG,fg=FG,font=F).pack()
    rr=tk.Frame(rate,bg=BG); rr.pack(pady=3)

    def nxt(): ri[0]+=1; (show_done()if ri[0]>=n else show_card())
    for t in["AGAIN","HARD","GOOD","EASY"]:
        tk.Button(rr,text=f"[{t}]",bg=DIM,fg=FG,font=F,relief="raised",
                  padx=10,pady=5,command=nxt).pack(side="left",padx=3)

    def undo(): ri[0]-=1; show_card()  # IH#5
    tk.Button(rate,text="[UNDO]",bg=DIM,fg=FG,font=F,relief="raised",padx=6,pady=3,
              state="normal"if i>0 else"disabled",command=undo).pack(pady=3)
    btn(f,"END",dash,dim=True); show(f)

def show_done():
    f=tk.Frame(area,bg=BG)
    L(f,"DONE!",fs=22,bold=True); L(f,f"Reviewed {len(cards)} cards.")
    btn(f,"AGAIN",review); btn(f,"DASHBOARD",dash,dim=True); show(f)

# TIMER
def timer():
    f=tk.Frame(area,bg=BG); sm=[25]
    L(f,"FOCUS TIMER",fs=20,bold=True)
    B(f,">> Time-box sessions for max focus. (IH#1)")
    B(f,"NOTE: Timer only runs while window is open. (IH#2)")
    L(f,"DURATION:",bold=True)
    dr=tk.Frame(f,bg=BG); dr.pack(anchor="w",pady=4)
    tl=tk.Label(f,text=fmt(ts[0]),bg=BG,fg=FG,font=("Courier New",52,"bold")); tl.pack(pady=6)
    pb_bg=tk.Frame(f,bg=DIM,height=12); pb_bg.pack(fill="x",padx=50); pb_bg.pack_propagate(False)
    pf=tk.Frame(pb_bg,bg=FG,height=12); pf.place(relwidth=0,relheight=1)
    st=tk.Label(f,text="READY",bg=BG,fg=GRAY,font=F); st.pack(pady=3)
    cr=tk.Frame(f,bg=BG); cr.pack(pady=6)

    def set_dur(m):
        if not tr[0]: sm[0]=m; ts[0]=m*60; tl.config(text=fmt(ts[0])); pf.place(relwidth=0,relheight=1)

    for m in[15,25,30,45]:  # IH#7 multiple options
        tk.Button(dr,text=f"[{m}m]",bg=DIM,fg=FG,font=("Courier New",9),relief="raised",
                  padx=5,pady=2,command=lambda m=m:set_dur(m)).pack(side="left",padx=3)

    def tick():
        if not tr[0]: return
        if ts[0]>0:
            ts[0]-=1; tl.config(text=fmt(ts[0])); pf.place(relwidth=1-ts[0]/(sm[0]*60),relheight=1)
            tj[0]=root.after(1000,tick)
        else:
            tr[0]=False; tl.config(text="00:00"); pf.place(relwidth=1,relheight=1)
            sb.config(state="normal",text="[START]"); pb.config(state="disabled")
            st.config(text="DONE!"); messagebox.showinfo("DONE","Session complete!")

    def start():
        if tr[0]: return
        if ts[0]<=0: ts[0]=sm[0]*60
        tr[0]=True; sb.config(state="disabled"); pb.config(state="normal")
        st.config(text="RUNNING..."); tick()

    def pause():
        tr[0]=False
        if tj[0]: root.after_cancel(tj[0])
        sb.config(state="normal",text="[RESUME]"); pb.config(state="disabled"); st.config(text="PAUSED")

    def reset():  # IH#5 IH#8
        if tr[0] and not messagebox.askyesno("RESET","Timer running. Reset?"): return
        tr[0]=False
        if tj[0]: root.after_cancel(tj[0])
        ts[0]=sm[0]*60; tl.config(text=fmt(ts[0])); pf.place(relwidth=0,relheight=1)
        sb.config(state="normal",text="[START]"); pb.config(state="disabled"); st.config(text="READY")

    sb=tk.Button(cr,text="[START]",bg=FG,fg=BG,font=("Courier New",12,"bold"),relief="raised",padx=12,pady=5,command=start); sb.pack(side="left",padx=4)
    pb=tk.Button(cr,text="[PAUSE]",bg=DIM,fg=FG,font=("Courier New",12),relief="raised",padx=12,pady=5,state="disabled",command=pause); pb.pack(side="left",padx=4)
    tk.Button(cr,text="[RESET]",bg=DIM,fg=FG,font=("Courier New",12),relief="raised",padx=12,pady=5,command=reset).pack(side="left",padx=4)
    show(f)

for label,cmd in[("DASHBOARD",dash),("CREATE",create),("REVIEW",review),("TIMER",timer)]:
    tk.Button(nav,text=f"[{label}]",bg="#000000",fg=FG,font=("Courier New",10,"bold"),
              relief="raised",padx=8,cursor="hand2",command=cmd).pack(side="left",padx=2)

for key,fn in[("d",dash),("c",create),("r",review),("t",timer)]:
    root.bind(key,lambda e,f=fn:f())

dash(); root.mainloop()
