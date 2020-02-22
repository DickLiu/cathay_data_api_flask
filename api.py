# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 23:52:41 2020

@author: Dick
"""
import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, pymongo
#from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


def pagination(page, limit):
    if not page:
        _p = 1
        _start = 0
    else:
        try:
            _p = int(page)
        except ValueError as e:
            return jsonify({"result": str(e)})
        if _p < 1:
            _start = 0
        else:
            _start = (_p-1)*limit
    return _start, _p

def query_user_gender_lastname(search_dict, userGender, userLastName):
    if userGender is not None:
        if userGender == "男":
            if userLastName is not None:
                search_dict["kfCallName"] = {'$regex': '^.*?{}先生.*?$'.format(userLastName)}
            else:
                search_dict["kfCallName"] = {'$regex': '^.*?先生.*?$'}
        elif userGender == "女":
            if userLastName is not None:
                search_dict["kfCallName"] = {'$regex': '^.*?{}小姐.*?$'.format(userLastName)}
            else:
                search_dict["kfCallName"] = {'$regex': '^.*?小姐.*?$'}
    else:
        if userLastName is not None:
            search_dict["kfCallName"] = {'$regex': '^.*?{}.*?$'.format(userLastName)}
        else:
            pass
    return search_dict

@app.route('/', methods=['GET'])
def home():
    
    p = request.args.get('page', None)
    limit = 10
    output = []
    
    _start, p = pagination(p, limit)
    
    _rents = mongo.db.rent.find().sort('rent_id', pymongo.DESCENDING).limit(limit).skip(_start)
    
    for _rent in _rents:
        output.append({"rent_id": _rent["rent_id"],
                       "region": _rent["region"],
                       "userInfo": _rent["userInfo"],
                       "kfCallName": _rent["kfCallName"],
                       "dialPhoneNum": _rent["dialPhoneNum"],
                       "type": _rent["type"],
                       "status": _rent["status"],
                       "genderRestrict": _rent["genderRestrict"],
                       "updated": _rent["updated"] or "",
                       "created": _rent["created"] or "",})
    print(request.url)
    _prev_url = "{}?page={}".format(request.base_url, p-1 if p > 1 else "1")
    _next_url = "{}?page={}".format(request.base_url, p+1 )
    return jsonify({'result' : output, 'prev_url': _prev_url, 'next_url': _next_url})


@app.route('/rent_detail', methods=['GET'])
def rent_detail():
    search_dict = dict()
    genderRestrict = request.args.get("genderrestrict", None)
    region = request.args.get("region", None)
    dialPhoneNum = request.args.get("dialphonenum", None)
    userInfo = request.args.get("userinfo", None)
    userGender = request.args.get("usergender", None)
    userLastName = request.args.get("userlastname", None)
    
    p = request.args.get('page', None)
    limit = 10
    _start, p = pagination(p, limit)
    
    if genderRestrict == "男":
        search_dict["$or"] = [{'genderRestrict':{'$regex': '^.*?男.*?$'}}, {'genderRestrict':""}]
    elif genderRestrict == "女":
        search_dict["$or"] = [{'genderRestrict':{'$regex': '^.*?女.*?$'}}, {'genderRestrict':""}]
    else:
        pass
    
    if region in ["台北市", "臺北市"]:
        search_dict["region"] = {'$regex': '^.*?台北市.*?$'}
    elif region == "新北市":
        search_dict["region"] = {'$regex': '^.*?新北市.*?$'}
    else:
        pass
    
    if dialPhoneNum is not None:
        search_dict["dialPhoneNum"] = {'$regex': '^.*?{}.*?$'.format(dialPhoneNum)}
        
    if userInfo == "屋主":
        search_dict["userInfo"] = {'$regex': '^.*?屋主.*?$'}       
        search_dict = query_user_gender_lastname(search_dict, userGender, userLastName)
    elif userInfo == "非屋主":
        search_dict["userInfo"] = {"$not": {'$regex': '^.*?屋主.*?$'}}
        search_dict = query_user_gender_lastname(search_dict, userGender, userLastName)
    else:
        search_dict = query_user_gender_lastname(search_dict, userGender, userLastName)                
    
    output = []
    search_q = [{key: value} for key, value in search_dict.items()]
    _rent_details = mongo.db.rent.find({"$and": search_q}).sort('rent_id', pymongo.DESCENDING).limit(limit).skip(_start)
    #_rent_details = mongo.db.rent_2.find(search_dict).sort('rent_id', pymongo.DESCENDING).limit(limit).skip(_start)
    try:
        for _rent in _rent_details:
            output.append({"rent_id": _rent["rent_id"],
                           "region": _rent["region"],
                           "userInfo": _rent["userInfo"],
                           "kfCallName": _rent["kfCallName"],
                           "dialPhoneNum": _rent["dialPhoneNum"],
                           "type": _rent["type"],
                           "status": _rent["status"],
                           "genderRestrict": _rent["genderRestrict"],
                           "updated": _rent["updated"] or "",
                           "created": _rent["created"] or "",})
    except (pymongo.errors.AutoReconnect, pymongo.errors.OperationFailure) as e:
        print(e) # to-do: logging
    
    _q = '&'.join(["{}={}".format(key, value) for key, value in request.args.items() if key != 'page'])
    _prev_url = "{}?page={}&".format(request.base_url, p-1 if p > 1 else "1") + _q
    _next_url = "{}?page={}&".format(request.base_url, p+1 ) + _q
    return jsonify({'result' : output, 'prev_url': _prev_url, 'next_url': _next_url})


#app.run()