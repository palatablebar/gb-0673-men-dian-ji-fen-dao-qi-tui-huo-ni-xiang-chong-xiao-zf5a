def audit_refunds(ledger):
    spends={r['id']:r for r in ledger['spends']};issues=[];rows=[]
    for refund in ledger['refunds']:
        original=spends[refund['ref']]
        allocated=sum(x['points'] for x in refund['allocations'])
        valid=allocated==refund['points'] and refund['restored']+refund['expired_refund']==refund['points'] and original['refunded']<=original['points']
        rows.append({k:v for k,v in refund.items() if k!='allocations'} | {'code':'VERIFIED' if valid else 'REFUND_UNBALANCED'})
        if not valid:issues.append(refund['id'])
    return rows,issues

def apply(state):
    rows,issues=audit_refunds(state['point_ledger']);state['refund_audit']=rows;state['refund_issues']=issues
    state['views']['refund']={'title':'退货回拨','rows':rows,'metrics':{'退款笔':len(rows),'恢复积分':sum(x['restored'] for x in rows),'过期不恢复':sum(x['expired_refund'] for x in rows)}}
