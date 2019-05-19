from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,jwt_required

api_lzh=Blueprint('api_lzh',__name__)

import API_lizhuohuan.lizhuohuan_check as checker

users={}
class Lizhuohuan(object):
    def __init__(self,consumername,costamount):
        self.consumer=consumername
        self.costamount=costamount

@api_lzh.route('/lizhuohuan_pay',methods=['POST'])
def lizhuohuan_pay():
    if not request.is_json:
        return jsonify({"错误":"不是JSON格式！"}),400
    consumer=request.json.get('consumer',None)
    costamount=request.json.get('costamount',None)
    if not consumer:
        return jsonify({"错误":"未写入顾客名！"}),400
    if not costamount:
        return jsonify({"错误":"未写入消费额！"}),400
    if consumer in users:
        return jsonify({"提示":"用户已存在！"}),203
    users[consumer]=Lizhuohuan(consumer,costamount)
    return jsonify({"提示":"保存成功！"}),200

@api_lzh.route('/lizhuohuan_paid',methods=['POST'])
def lizhuohuan_paid():
    if not request.is_json:
        return jsonify({"错误":"不是JSON格式！"}),400
    consumer=request.json.get('consumer',None)
    costamount=request.json.get('costamount',None)
    if (not consumer) or (not costamount):
        return jsonify({"错误":"没有该顾客或者尚未消费！"}),401
    VIPuser=users.get(consumer,None)
    if not VIPuser:
        return jsonify({"错误":"该顾客不是VIP！"}),401
    elif VIPuser and VIPuser.costamount==costamount:
        return jsonify(客户信息=create_access_token(identity=consumer))
    else:
        return jsonify({"错误":"顾客名或者消费额错误！"}),401

@api_lzh.route('/lizhuohuan_check',methods=['GET'])
@jwt_required
def lizhuohuan_check():
    if not request.is_json:
        return jsonify({"错误":"不是JSON格式！"}),400
    number=request.json.get('checkNo')
    return jsonify({"编号":checker.check(number)},
                   {"提示":"验证成功！"}),200