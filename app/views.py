import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User

from django.contrib import messages

from app.forms import UserInfoForm, UserForm, InfoChange, StoreIn, StoreOut

from datetime import datetime

from app.models import UserInfo, Supplier, Goods, StockOut, WaveHousing, Storage, SellOut

# Create your views here.
# 改视图函数无意义，只是单纯重定向到登录界面
def index(request):
    return redirect(to= 'login')

def index_login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(to='infomanage')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 判断用户是否存在
            user = authenticate(username= username, password= password)
            print(user)
            if user:
                login(request, user)
                # if user.is_staff: return redirect(to= 'userinfo')
                return redirect(to= 'infomanage')
            else:
                messages.add_message(request, messages.ERROR, "账号或密码错误，请重新输入！")
                return redirect (to='login')
        else:
            return redirect(to='login')
    else:
        form = UserForm()
        return render(request, 'login.html', {'form' : form})


def index_logout(request):
    logout(request)
    messages.add_message (request, messages.ERROR, "退出登录成功,请您重新登陆！")
    return redirect(to='login')


def register(request):
    user = request.user
    if user.is_authenticated:
        return redirect(to='infomanage')
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_exist = User.objects.filter(username= username)
            if user_exist:
                messages.add_message(request, messages.ERROR, "用户名已存在,请更换！")
                return redirect(to= 'register')
            else:
                password = form.cleaned_data['password']
                User.objects.create_user(username=username, password=password)
                try:
                    acc = User.objects.get(username=username)
                    user = UserInfo()
                    user.account = acc
                    user.sex = form.cleaned_data['sex']
                    user.name = form.cleaned_data['username']
                    user.job = form.cleaned_data['job']
                    user.job_num = form.cleaned_data['job_num']
                    user.save()
                except:
                    print('error')
                    pass
                return redirect(to= 'login')

    elif request.method == 'GET':
        form = UserInfoForm
        return render(request, 'register.html', {'form' : form})

# 返回的參數args（商品名稱，公司，價格）
# 根據編號返回信息
def getGoodInfo(request):
    try:
        goodList = Goods.objects.all()
        json_list = []
        for good in goodList:
            json_dict = model_to_dict(good)
            json_list.append(json_dict)
        goodList = json_list

        good = goodList
    except Exception as e:
        print(e)
        good = ["","",0]
    finally:
        jsonArr = json.dumps(good, ensure_ascii=False,cls=DateEncoder)
        return HttpResponse(jsonArr, content_type="application/json") # 返回json数据

def getSupInfo(request):
    try:
        goodList = Supplier.objects.all()
        json_list = []
        for good in goodList:
            json_dict = model_to_dict(good)
            json_list.append(json_dict)
        goodList = json_list

        good = goodList
    except Exception as e:
        print(e)
        good = ["","",0]
    finally:
        jsonArr = json.dumps(good, ensure_ascii=False,cls=DateEncoder)
        return HttpResponse(jsonArr, content_type="application/json") # 返回json数据

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def infochange(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(to='login')
    if request.method == 'POST':
        form = InfoChange(request.POST)
        if form.is_valid():
            if user:
                password = form.cleaned_data['password']
                password_again = form.cleaned_data['password_again']
                if password == password_again:
                    user.set_password(password)

                    #
                    # acc = User.objects.get(username=user.userinfo.name)
                    # user = UserInfo()
                    # user.account = acc
                    # user.sex = form.cleaned_data['sex']
                    # user.job = form.cleaned_data['job']


                    user.userinfo.sex = form.cleaned_data['sex']
                    user.save()
                    messages.add_message (request, messages.INFO, "信息更改成功，请重新登录！")
                    return redirect(to='login')
                else:
                    messages.add_message(request, messages.ERROR, "两次密码不一致！")
                    return redirect(to= 'infochange')

            else:
                messages.add_message(request, messages.ERROR, "用户名不存在,请先注册！")
                return redirect(to= 'register')

    elif request.method == 'GET':
        form = InfoChange
        return render(request, 'infochange.html', {'form' : form})


# 保持数据一致，出库数量加到商品在售数量；入库数量加到库存
def instore(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(to='login')
    if request.method == 'POST':
        if (request.user.userinfo.job != '仓库主管'):
            messages.add_message(request, messages.ERROR, "你不是仓库主管 ，无权修改入库信息")
            return redirect(to='instore')
        # print(request.POST)
        form = StoreIn(request.POST)
        if form.is_valid():
            sup_name = form.cleaned_data['sup_name']
            goods_name = form.cleaned_data['goods_name']
            op_price = form.cleaned_data['op_price']
            op_amount = form.cleaned_data['op_amount']
            ID = form.cleaned_data['goodsID']
            op_ps = form.cleaned_data['op_ps']
            print(sup_name,goods_name,op_price,op_amount,ID)
            try:
                sup, tmp = Supplier.objects.get_or_create(sup_name=sup_name)
                print('--after get sup--')

                print('---入库 try---')
                print(sup, tmp)
                goods, tmp = Goods.objects.get_or_create(goods_name=goods_name, goods_sup=sup, goodsID=ID)
                print(goods, tmp)
                # goods.goods_cost = goods.goods_cost + op_price * op_amount
                # print(goods.goods_amount, op_amount)
                store, tmp = Storage.objects.get_or_create(goods_name=goods)
                store.storage_amount = store.storage_amount + op_amount
                if (store.storage_amount > 1000):
                    raise Exception('库存大于1000,装不下啦！入库失败！')
                if (op_price > 10000):
                    raise Exception('价格太高了,是不是写错了?')
                goods.goods_price = op_price
                # goods.goods_amount = goods.goods_amount + op_amount
                WaveHousing.objects.create(goods_name=goods, sup_name=sup, res_person=user.userinfo,
                                           in_price=op_price, in_amount=op_amount, in_ps=op_ps, pay_status=False)
                print('---before save---')
                goods.save()
                store.save()
                print('---goods save ok---')

                print('--try after wh create--')
                messages.add_message(request, messages.SUCCESS, '入库成功！')

            except Exception as err:
                print('--入库哪里有错--')
                messages.add_message(request, messages.ERROR, err)

        return redirect(to= 'instore')

    else:
        form = StoreIn
        return render(request, 'instore.html', {'form': form})

def outstore(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(to='login')



    if request.method == 'POST':
        if (request.user.userinfo.job != '仓库主管'):
            messages.add_message(request, messages.ERROR, "你不是仓库主管 ，无权修改出库信息")
            return redirect(to='outstore')
        # print(request.POST)
        form = StoreOut(request.POST)
        if form.is_valid():
            sup_name = form.cleaned_data['sup_name']
            goods_name = form.cleaned_data['goods_name']
            op_price = form.cleaned_data['op_price']
            op_amount = form.cleaned_data['op_amount']
            ID = form.cleaned_data['goodsID']
            op_ps = form.cleaned_data['op_ps']
            print(sup_name,goods_name,op_amount,ID)
            try:
                sup = Supplier.objects.get(sup_name=sup_name)
                print(sup)
                # goods = Goods.objects.get(goods_name=goods_name, goods_sup=sup, goodsID=ID)
                goods = Goods.objects.get(goods_name=goods_name, goods_sup=sup)
                print(goods)
                # goods.goods_revenue = goods.goods_revenue + op_price * op_amount
                store = Storage.objects.get(goods_name=goods)
                store.storage_amount = store.storage_amount - op_amount
                print(store.storage_amount)
                goods.goods_amount = goods.goods_amount + op_amount
                goods.goods_sprice = op_price
                if (store.storage_amount < 0):
                    raise Exception("库存不足！出库失败！")
                if (goods.goods_amount > 1000):
                    raise Exception("正在销售商品超过1000了！出库失败！")
                if (op_price > 10000):
                    raise Exception('价格太高了,是不是写错了?')
                goods.update_date = datetime.now()
                StockOut.objects.create(goods_name=goods, sup_name=sup, res_person=user.userinfo,
                                        out_date=goods.update_date,
                                        out_amount=op_amount, out_ps=op_ps)
                goods.save()
                store.save()
                print('---出库 save ok---')
                print(goods, sup, user, goods.update_date, op_amount)

                print('--出库 ok--')
                messages.add_message(request, messages.SUCCESS, '出库成功！')
            except Exception as err:
                print('--出库哪里有错--')
                messages.add_message(request, messages.ERROR, err)

        return redirect(to= 'outstore')

    else:
        form = StoreOut
        return render(request, 'outstore.html', {'form': form})



#@login_required(login_url='/', redirect_field_name='login')
def infomanage(request):
    user = request.user
    print(request.user)
    if not user.is_authenticated:
        return redirect(to='login')
    print(user.is_staff)
    context = {}
    query = None
    flag = None
    if request.method == 'GET':
        page = request.GET.get('page')
        if request.GET.get('query'):
            query = request.GET.get('query')
            print(query)
        print('--get query--')
        print(query)
        if not query:
            query = 'goods'

        if query == 'supplier':
            context['sup_inver'] = 'layui-this'
            context['name'] = query
            each_object = Supplier.objects.all()
            if not each_object:
                messages.add_message(request, messages.ERROR, '无此类数据记录')
            print(each_object)
            paginator = Paginator(each_object,7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        elif query == 'goods':
            context['goods_inver'] = 'layui-this'
            context['name'] = 'goods'
            each_object = Goods.objects.all()
            if not each_object:
                messages.add_message(request, messages.ERROR, '无此类数据记录')
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        elif query == 'storage':
            if (request.user.userinfo.job == '用户'):
                messages.add_message(request, messages.ERROR, "权限不足查看库存")
                return redirect(to='infomanage')
            context['storage_inver'] = 'layui-this'
            context['name'] = query
            each_object = Storage.objects.all()
            if not each_object:
                messages.add_message(request, messages.ERROR, '无此类数据记录')
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts
            print(dir(context['each_object']))

        # 销售信息
        elif query == 'sellout':
            if (request.user.userinfo.job == '用户'):
                messages.add_message(request, messages.ERROR, "权限不足查看销售")
                return redirect(to='infomanage')
            context['sellout_inver'] = 'layui-this'
            context['name'] = query
            each_object = SellOut.objects.all()
            if not each_object:
                messages.add_message(request, messages.ERROR, '无此类数据记录')
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)
            # 计算总营收
            revenue = 0
            for eo in each_object:
                g1 = eo.goods_name
                r1 = (g1.goods_sprice*(1 - g1.goods_discount) - g1.goods_price) * eo.out_amount
                revenue += r1
                # print(g1.goods_sprice,'kk')
            context['revenue'] = '%.1f' % revenue
            context['each_object'] = contacts
            print(dir(context['each_object']))


        elif query == 'stockout':
            if (request.user.userinfo.job == '用户'):
                messages.add_message(request, messages.ERROR, "权限不足出库记录")
                return redirect(to='infomanage')
            context['stockout_inver'] = 'layui-this'
            context['name'] = query
            each_object = StockOut.objects.all()
            if not each_object:
                messages.add_message(request, messages.ERROR, '无此类数据记录')
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        elif query == 'wavehousing':
            if (request.user.userinfo.job == '用户'):
                messages.add_message(request, messages.ERROR, "权限不足查看库存")
                return redirect(to='infomanage')
            context['wavehouse_inver'] = 'layui-this'
            context['name'] = query
            each_object = WaveHousing.objects.all()
            if not each_object:
                messages.add_message(request, messages.ERROR, '无此类数据记录')
            paginator = Paginator(each_object, 7)
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(Paginator.num_pages)

            context['each_object'] = contacts

        return render(request, 'infomanage.html', context= context)
