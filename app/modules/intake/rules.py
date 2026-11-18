from .reader import read_source
FIELDS=['id', 'member', 'type', 'points', 'at', 'expires', 'ref', 'rule', 'version']
def apply(state):read_source(state,FIELDS,{'编号':'id'})
