from fastapi import APIRouter, Request, Body
from app.engine import evaluate
from app.web import render
router=APIRouter()
@router.get('/refund')
def page(request:Request):
    return render(request,'refund')
@router.post('/api/refund')
def calculate(payload:dict=Body(default={})):
    return evaluate(payload,until=5)
