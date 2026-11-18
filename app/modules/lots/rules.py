from app.coerce import instant
from app.errors import BusinessError
from app.reasons import reject

def build_lots(rows):
    lots=[];bad=[]
    for row in rows:
        if row['type']!='EARN':continue
        try:
            expiry=instant(row['expires'])
            if expiry<=instant(row['at']):raise BusinessError('INVALID_EXPIRY','到期时刻不晚于发放')
            lots.append({'id':row['id'],'member':row['member'],'issued':row['points'],'remaining':row['points'],'expires':expiry.isoformat(),'at':row['at'],'line':row['_line']})
        except BusinessError as e:bad.append((row,e.code,e.message))
    return sorted(lots,key=lambda r:(r['member'],r['expires'],r['at'],r['id'])),bad

def apply(state):
    lots,bad=build_lots(state['records']);bad_ids={r['id'] for r,_,_ in bad}
    for row,code,detail in bad:reject(state,row,code,detail)
    state['records']=[r for r in state['records'] if r['id'] not in bad_ids];state['lots']=lots
    state['views']['lots']={'title':'积分批次','rows':lots,'metrics':{'发放批':len(lots),'发放积分':sum(r['issued'] for r in lots)}}
