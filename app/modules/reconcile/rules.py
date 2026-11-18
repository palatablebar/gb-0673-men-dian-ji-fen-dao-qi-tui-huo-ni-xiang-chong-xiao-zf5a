def reconcile(state):
    l=state['point_ledger'];issued=sum(r['issued'] for r in l['lots']);remaining=sum(r['remaining'] for r in l['lots']);spent=sum(r['points'] for r in l['spends']);refunded=sum(r['points'] for r in l['refunds']);expired=l['expired']+sum(r['expired_refund'] for r in l['refunds'])
    c=state['counts'];explained=len(state['records'])+len(state['quarantine'])+c['blank']+c['duplicate']+c['repeated_header']
    return {'input':c['input'],'accepted':len(state['records']),'quarantined':len(state['quarantine']),'row_balanced':c['input']==explained,'issued':issued,'remaining':remaining,'spent':spent,'refunded':refunded,'expired':expired,'points_balanced':issued==remaining+spent-refunded+expired}
def apply(state):
    state['balance']=reconcile(state);state['views']['reconcile']={'title':'积分余额对账','rows':[state['balance']],'metrics':{'发放':state['balance']['issued'],'净消费':state['balance']['spent']-state['balance']['refunded'],'到期':state['balance']['expired']}}
