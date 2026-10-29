#!/usr/bin/env python3
"""Pobiera publiczne archiwum mbnet; aktualizuje wyłącznie zweryfikowane rekordy."""
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / 'data' / 'draws.json'

class Rows(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_row=False; self.in_cell=False; self.cells=[]; self.rows=[]; self.buf=[]
    def handle_starttag(self, tag, attrs):
        if tag=='tr': self.in_row=True; self.cells=[]
        if self.in_row and tag in ('td','th'): self.in_cell=True; self.buf=[]
    def handle_data(self, data):
        if self.in_cell: self.buf.append(data)
    def handle_endtag(self, tag):
        if tag in ('td','th') and self.in_cell:
            self.cells.append(' '.join(''.join(self.buf).split())); self.in_cell=False
        if tag=='tr' and self.in_row:
            if self.cells: self.rows.append(self.cells)
            self.in_row=False

def parse_page(html):
    parser=Rows(); parser.feed(html); out=[]
    for cells in parser.rows:
        if len(cells)<3: continue
        number=re.fullmatch(r'\d{3,6}',cells[0].strip())
        date=re.search(r'(\d{2})\.(\d{2})\.(\d{4})',cells[1])
        nums=re.findall(r'\d+',cells[2])
        if not number or not date or len(nums)!=6: continue
        nums=list(map(int,nums))
        if len(set(nums))!=6 or any(not 1<=n<=49 for n in nums): continue
        day,month,year=map(int,date.groups())
        try: iso=dt.date(year,month,day).isoformat()
        except ValueError: continue
        out.append({'id':int(number.group()),'date':iso,'nums':sorted(nums)})
    return out

def main():
    old=json.loads(DEST.read_text(encoding='utf-8')) if DEST.exists() else []
    merged={int(x['id']):x for x in old if str(x.get('id','')).isdigit()}
    now=dt.datetime.now(dt.timezone.utc).year
    fetched=[]; errors=[]
    for year in range(now,now-6,-1):
        url=f'https://www.mbnet.com.pl/archiwum/lotto/{year}'
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; LottoLab/2.0)'})
            with urllib.request.urlopen(req,timeout=25) as res:
                html=res.read().decode('utf-8','replace')
            rows=parse_page(html)
            if not rows: raise ValueError('Brak poprawnych wierszy w HTML')
            fetched.extend(rows)
            print(f'{year}: {len(rows)} wyników')
        except Exception as exc:
            errors.append(f'{year}: {exc}')
    if not fetched:
        print('Nie udało się pobrać archiwum; zachowuję istniejące dane. '+ '; '.join(errors),file=sys.stderr)
        sys.exit(1)
    for item in fetched:
        prior=merged.get(item['id'])
        if prior and prior['nums']!=item['nums']:
            print(f'UWAGA: sprzeczne liczby losowania {item["id"]}, zachowuję wcześniejszy rekord',file=sys.stderr)
            continue
        merged[item['id']]=item
    latest=sorted(merged.values(),key=lambda x:x['id'])[-500:]
    # Nie publikuj niepełnego archiwum jako 500 zweryfikowanych rekordów.
    DEST.write_text(json.dumps(latest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Zapisano {len(latest)} losowań, ostatnie {latest[-1]["id"]}. Błędy: {errors}')

if __name__=='__main__': main()
