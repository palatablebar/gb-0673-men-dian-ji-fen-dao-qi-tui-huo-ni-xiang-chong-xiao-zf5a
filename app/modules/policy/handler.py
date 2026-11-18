from fastapi import APIRouter, Request, Body
from app.engine import evaluate
from app.web import render
router=APIRouter()
@router.get('/policy')
def page(request:Request):
    return render(request,'policy')
@router.post('/api/policy')
def calculate(payload:dict=Body(default={})):
    return evaluate(payload,until=2)
