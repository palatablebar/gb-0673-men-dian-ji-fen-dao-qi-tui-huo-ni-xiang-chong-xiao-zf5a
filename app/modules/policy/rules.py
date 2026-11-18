from app.coerce import number,instant
from app.errors import BusinessError
from app.reasons import reject

def normalize(row,context):
    value=number(row['points']);version=number(row['version'])
    if value<=0 or value%1 or version<1 or version%1:raise BusinessError('INVALID_RANGE','积分与版本须为正整数')
    if row['type'] not in {'EARN','SPEND','REFUND'}:raise BusinessError('BAD_TYPE','积分事件类型无效')
    if not row['member'].strip() or row['rule'] not in context['rules']:raise BusinessError('UNKNOWN_RULE','会员或权益规则不存在')
    at=instant(row['at']);rule=context['rules'][row['rule']]
    if not instant(rule['start'])<=at<instant(rule['end']):raise BusinessError('RULE_EXPIRED','事件不在权益有效窗')
    if at>instant(context['as_of']):raise BusinessError('AFTER_CUTOFF','事件晚于结算时点')
    return {**row,'points':int(value),'version':int(version),'at':at.isoformat()}
def apply(state):
    good=[]
    for row in state['records']:
        try:good.append(normalize(row,state['context']))
        except BusinessError as e:reject(state,row,e.code,e.message)
    state['records']=good;state['views']['policy']={'title':'权益校验','rows':good,'metrics':{'有效事件':len(good),'规则版本':len(state['context']['rules'])}}
