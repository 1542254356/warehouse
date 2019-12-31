from django import forms
class UserForm(forms.Form):
    username = forms.CharField(label='账号:')
    password = forms.CharField(label='密码:', widget= forms.PasswordInput)


class UserInfoForm(forms.Form):
    username = forms.CharField(label='用户名:')
    name = forms.CharField(label='姓名:')
    password = forms.CharField(label='密码:',widget= forms.PasswordInput)
    job_num = forms.IntegerField(label='工号:')
    sex_choice = {('male', '男'), ('female', '女'), }
    job_choice = {('普通员工', '普通员工'), ('仓库主管','仓库主管'),('用户','用户')}
    sex = forms.ChoiceField(label='性别:', choices= sex_choice)
    job = forms.ChoiceField(label='职位:', choices= job_choice)


class InfoChange(forms.Form):
    password = forms.CharField(label='请输入新密码:',widget= forms.PasswordInput)
    password_again = forms.CharField(label='再次输入新密码:',widget= forms.PasswordInput)
    sex_choice = {('male', '男'), ('female', '女'), }
    sex = forms.ChoiceField(label='性别:', choices= sex_choice)

class StoreIn(forms.Form):
    goods_name = forms.CharField(label='货物名称:')
    goodsID = forms.IntegerField(label='货物编号')
    sup_name = forms.CharField(label='供应商:')
    op_price = forms.FloatField(label='操作单价:')
    op_amount = forms.IntegerField(label='操作数量:')
    op_ps = forms.CharField(label='备注:')

class StoreOut(forms.Form):
    goods_name = forms.CharField(label='货物名称:')
    goodsID = forms.IntegerField(label='货物编号')
    sup_name = forms.CharField(label='供应商:')
    op_price = forms.FloatField(label='建议售价:')
    op_amount = forms.IntegerField(label='操作数量:')
    op_ps = forms.CharField(label='备注:')
