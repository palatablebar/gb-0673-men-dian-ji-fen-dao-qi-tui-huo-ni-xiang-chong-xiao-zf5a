from fastapi import APIRouter, Request, Body
from app.engine import evaluate
from app.web import render
router=APIRouter()
@router.get('/consumption')
def page(request:Request):
    return render(request,'consumption')
@router.post('/api/consumption')
def calculate(payload:dict=Body(default={})):
    return evaluate(payload,until=4)
