from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io

# Create your views here.

df = pd.read_pickle("submit2.pkl")

def show(pref=None):
    fig, ax = plt.subplots(figsize=(10, 8))
    if pref is None:
        show_all_pref= df.pivot_table(index="eng_region",columns="year",values="population",aggfunc="sum").sort_values(2019,ascending=False).T
    else:
        show_all_pref = df[df.eng_region.str.contains(f"{pref}")].pivot_table(index="eng_region",columns="year",values="population",aggfunc="sum").sort_values(2019,ascending=False).T
    show_all_pref.plot(kind="bar", stacked=True,ax=ax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=9)
    plt.show()

def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf,format="svg",bbox_inches="tight")
    s = buf.getvalue()
    buf.close()
    return s


def home(request):
    # html = df.to_html(
    #     classes=["table", "table-bordered", "table-hover"],
    #     escape=False
    # )
    show()
    svg = plt2svg()
    plt.cla()
    response = HttpResponse(svg,content_type="image/svg+xml")
    return response

def prefecture(request):
    jp_region = df.region.unique()
    eng_region = df.eng_region.unique()
    html = ""
    for en,jp in zip(eng_region,jp_region):
        html += f'<a href="{en}">{jp}</a><br>'
    return HttpResponse(html)

def prefectures(request,pref):
    show(pref)
    svg = plt2svg()
    plt.cla()
    response = HttpResponse(svg,content_type="image/svg+xml")
    return response