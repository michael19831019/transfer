result_ = httpRequest(url,httpdata)
    result = result_['data']
    result = {"code":1,"mobile":"15383110077","bank_":"PSBC",'password':"vip17965290",'spassword':'861690','money':'20.50','cardnumber':'6217000130021964340','hm':'孟峰峰','deviceid':'8HT4DEQODUAQNFMJ'}
    print(result)
    # deivce online set
    onlineSet(sn)
    #check mobile sn
    myredis.delete("device-"+sn)
    device_list = adb_obj.getdevicelist()
    print(device_list)
    if len(device_list)<=0:
        print("###No mobile found!###")
    else:
        for name in device_list: 
            myredis.hset("device-"+sn,name,1)
        if result['code'] ==0:
            print("------###No transferorder found! Pulling order...in 3 seconds###------")
        else:
            bank = result['bank_']
            module = importlib.import_module(bank+"."+bank)
            adb_obj_class = getattr(module,bank)
            bank_class = adb_obj_class(result)
            tresult = bank_class.transfer()
            
            if tresult == "101":
                print("------###No device found!###------")
            if tresult == "102":
                url2 = "https://nb.brst.space/api/transfer/changestatus"
                print(bank_class.errmsg)
                data2 = {'username':username,'status':3,'id':result['id'],'failedreason':bank_class.errmsg}
                httpRequest(url2,data2)
            if tresult == "10000":
                url_success = "https://nb.brst.space/api/transfer/changestatus"
                data_success  = {'username':username,'status':2,'id':result['id'],'failedreason':'Transfer Success!'}
                httpRequest(url_success,data_success)