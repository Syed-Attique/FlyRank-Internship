import json, pathlib
R = json.load(open("docs/results.json"))
def pct(x): return f"{x*100:.0f}%" if x>=0.1 else f"{x*100:.1f}%"
def bars(rows, hi):
    out = []
    for name, v, extra in rows:
        cls = " class=hi" if name == hi else ""
        out.append(f'<div class=r><span class=l>{name}</span><span class=b><i{cls} style="width:{v*100:.1f}%"></i></span><b>{extra}</b></div>')
    return "".join(out)
c1 = bars([(m[0], m[2], f"{m[2]:.2f}") for m in R["methods"]], "Random forest")
c2 = bars([(s[0], s[2], f"{s[2]:.2f}") for s in R["split"]], "Grouped by client")
c3 = bars([(a[0], a[1], f"{a[1]*100:.1f}% (n={a[2]:,})") for a in R["age"]], "")
rows = "".join(f"<tr><td>{m[0]}</td><td>{m[1]:.2f}</td><td>{m[2]:.2f}</td><td>{m[3]}</td></tr>" for m in R["methods"])
imp = ", ".join(f"{n} {v:.3f}" for n, v in R["importance"])
a = R["actions"]; tot = sum(a.values()); flagged = a["fix_ctr_snippet"] + a["review_for_refresh"]
T = open("work/paper_template.html").read()
for k, v in {"@@C1@@": c1, "@@C2@@": c2, "@@C3@@": c3, "@@ROWS@@": rows, "@@IMP@@": imp,
             "@@PAGES@@": f"{R['pages']:,}", "@@TESTP@@": f"{R['test_pages']:,}", "@@TOT@@": f"{tot:,}",
             "@@FLAG@@": f"{flagged:,}", "@@FLAGPCT@@": f"{flagged/tot*100:.0f}%", "@@CTR@@": f"{a['fix_ctr_snippet']:,}",
             "@@CTRPCT@@": f"{a['fix_ctr_snippet']/tot*100:.0f}%", "@@REV@@": f"{a['review_for_refresh']:,}"}.items():
    T = T.replace(k, v)
pathlib.Path("docs/index.html").write_text(T)
print("wrote docs/index.html", len(T), "bytes")
