from django.shortcuts import render, redirect
from data_app.models import Customer, Encryption
import psycopg2
import cryptocode

# Create your views here.

conn = psycopg2.connect(
    database="enc_decrypt", user='postgres', password='sneha123'
# database="mydb", user='postgres', password='sneha123', host='127.0.0.1', port= '5432'
)


# Setting auto commit false

conn.autocommit = True


# Creating a cursor object using the cursor() method

cursor1 = conn.cursor()


def index(request):
    data = {}
    data['s_user'] = request.session.get('user')
    return render(request, 'index.html', data)


def signup(request):
    sign_data = {}
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        name = request.POST.get('fname')
        addr = request.POST.get('add')
        e_mail = request.POST.get('mail')
        mobile = request.POST.get('num')
        user_name = request.POST.get('user')
        pass_word = request.POST.get('pass')
        print(name, addr, e_mail, mobile, user_name, pass_word)

        cursor1.execute("select * from customer where username='" + user_name + "'")
        tempvar = cursor1.fetchall()
        rowcount = len(tempvar)

        cursor2 = conn.cursor()
        cursor2.execute("select * from customer where email='" + e_mail + "'")
        mailvar = cursor2.fetchall()
        rowcount2 = len(mailvar)

        cursor3 = conn.cursor()
        cursor3.execute("select * from customer where mobile='" + mobile + "'")
        mobvar = cursor3.fetchall()
        rowcount3 = len(mobvar)

        if rowcount == 1:
            sign_data['msg'] = 'username allready exist'
            return render(request, 'signup.html', sign_data)
        elif rowcount2 == 1:
            sign_data['emsg'] = 'email allready exist'
            return render(request, 'signup.html', sign_data)
        elif rowcount3 == 1:
            sign_data['pmsg'] = 'mobile allready exist'
            return render(request, 'signup.html', sign_data)
        else:
            savecard = Customer()
            # here fullname , username, password is database field name
            savecard.fullname = name
            savecard.address = addr
            savecard.email = e_mail
            savecard.mobile = mobile
            savecard.username = user_name
            savecard.password = pass_word
            savecard.save()
            print('demo')
            return render(request, 'login.html')






def login(request):

    data = {}

    if request.method == "GET":
        return render(request, 'login.html')
    else:
        if 'log' in request.POST:
            name = request.POST.get('user')
            passw = request.POST.get('pass')
            cursor = conn.cursor()
            cursor.execute("select * from customer where username='" + name + "' and password ='" + passw + "'")
            tempvar = cursor.fetchall()
            rowcount = len(tempvar)
            print(rowcount)

            if rowcount == 1:
                request.session['user'] = name
                data['s_user'] = request.session.get('user')
                print(request.session['user'])
                return render(request, 'index.html', data)
            else:
                data['msg'] = 'enter valid username or password'
                return render(request, 'login.html', data)


def encry(request):
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        return render(request, 'encryption.html', data)
    else:
        info = request.POST.get('data')
        info_key = request.POST.get('key')
        user = request.POST.get('user')
        reci = request.POST.get('rec')
        encoded = cryptocode.encrypt(info, info_key)
        print(user,encoded,info,info_key)
        cursor = conn.cursor()
        cursor.execute("select * from data_app_encryption where key='" + info_key + "'")
        tempvar = cursor.fetchall()
        rowcount = len(tempvar)
        print(rowcount)
        r = 6
        e_id = str(r)

        if rowcount == 0:
            data['ecode'] = encoded

            savecard = Encryption()
            # here fullname , username, password is database field name
            savecard.data = info
            savecard.key = info_key
            savecard.username = user
            savecard.receiver = reci
            savecard.enc_data = encoded
            savecard.save()

            # cursor1.execute("select max(id) from data_app_encryption")
            # data['res'] = cursor1.fetchall()
            return render(request, 'encryption.html', data)
        else:
            data['emsg'] = 'key allready exist try another one'
            return render(request, 'encryption.html', data)


def decry(request):
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        data['result'] = Customer.objects.filter(username=data['s_user'])
        return render(request, 'decryption.html', data)
    else:
        info = request.POST.get('enc')
        info_key = request.POST.get('key')
        user = request.POST.get('user')
        uname = request.POST.get('name')
        cursor1.execute("select * from data_app_encryption where enc_data='" + info + "' and receiver ='" + uname + "'")
        tempvar = cursor1.fetchall()
        rowcount = len(tempvar)
        print(rowcount)

        if rowcount == 1:
            # And then to decode it:
            decoded = cryptocode.decrypt(info, info_key)
            print(decoded, info_key, user)
            data['decode'] = decoded
            return render(request, 'decryption.html', data)
        else:
            data['decode'] = "data not found"
            return render(request, 'decryption.html', data)


def profile(request):
    data = {}
    data['s_user'] = request.session.get('user')
    data['result'] = Customer.objects.filter(username=data['s_user'])
    return render(request, 'profile.html', data)


def up_account(request):
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        data['result'] = Customer.objects.filter(username=data['s_user'])
        return render(request, 'upd_account.html', data)
    else:
        if 'update' in request.POST:
            c_id = request.POST.get('cid')
            name = request.POST.get('fname')
            addr = request.POST.get('add')
            e_mail = request.POST.get('mail')
            mobile = request.POST.get('num')
            user_name = request.POST.get('user')
            pass_word = request.POST.get('pass')
            # Updating the records
            sql = "UPDATE customer SET fullname = '" + name + "',address ='" + addr + "',mobile ='" + mobile + "',email ='" + e_mail + "',username ='" + user_name + "',password ='" + pass_word + "' where id='" + c_id + "'"
            cursor1.execute(sql)
            print("Table updated...... ")
            return redirect("account")



def u_activity(request):
    data = {}
    data['s_user'] = request.session.get('user')
    if request.method == "GET":
        data['result1'] = Encryption.objects.filter(username=data['s_user'])
        return render(request, 'enc_view.html', data)
    else:
        if 'edit' in request.POST:
            name = request.POST.get('en_edit')
            data['result1'] = Encryption.objects.filter(id=name)
            return render(request, 'up_uenc.html', data)
        elif 'del' in request.POST:
            name = request.POST.get('en_del')
            del_stu = Encryption.objects.filter(id=name)
            del_stu.delete()
            return redirect('activity')
        elif 'update' in request.POST:
            e_id = request.POST.get('eid')
            udata = request.POST.get('data')
            ukey = request.POST.get('key')
            u_user = request.POST.get('user')
            urec = request.POST.get('rec')
            encoded = cryptocode.encrypt(udata, ukey)
            print(udata, ukey, u_user, urec, encoded)

            cursor1.execute("select * from data_app_encryption where key='" + ukey + "'")
            tempvar = cursor1.fetchall()
            rowcount = len(tempvar)
            print(rowcount)

            if rowcount == 0:
                # Updating the records
                sql = "UPDATE data_app_encryption SET data = '" + udata + "',key ='" + ukey + "',username ='" + u_user + "',receiver ='" + urec + "',enc_data ='" + encoded + "' where id='" + e_id + "'"
                cursor1.execute(sql)
                print("Table updated...... ")
                return redirect("activity")
            else:
                data['msg'] = 'key allready exist, please try again by menubar'
                return render(request, 'up_uenc.html', data)




def logout(request):
    del request.session['user']
    return redirect('log')

# -----admin section start -----


def a_login(request):
    data = {}

    if request.method == "GET":
        return render(request, 'a_login.html')
    else:
        if 'log' in request.POST:
            name = request.POST.get('user')
            passw = request.POST.get('pass')
            if name == 'admin' and passw == 'admin123':
                request.session['a_user'] = name
                data['ad_user'] = request.session.get('a_user')
                print(request.session['a_user'])
                return render(request, 'admin/a_home.html', data)
            else:
                data['msg'] = 'enter valid username or password'
                return render(request, 'a_login.html', data)


def a_index(request):
    data = {}
    data['ad_user'] = request.session.get('a_user')
    print(request.session['a_user'])
    if request.method == "GET":
        return render(request, 'admin/a_home.html', data)


def ad_profile(request):
    showall = Customer.objects.all()
    data = {}
    data['ad_user'] = request.session.get('a_user')
    data['result'] = showall
    return render(request, 'admin/profile_data.html', data)


def a_endata(request):
    data = {}
    data['ad_user'] = request.session.get('a_user')
    if request.method == "GET":
        showall = Encryption.objects.all()
        data = {}
        data['ad_user'] = request.session.get('a_user')
        data['result1'] = showall
        return render(request, 'admin/a_encrydata.html', data)
    else:
        if 'del' in request.POST:
            info = request.POST.get('en_del')
            cursor1.execute("delete from data_app_encryption where id ='" + info + "'")
            print(info)
            return redirect('a_edata')



def a_logout(request):
    del request.session['a_user']
    return redirect('alog')



"""

def index(request):
    if request.method == "GET":
        showall = Student.objects.all()
        return render(request, 'index.html', {'data': showall})
    else:
        if 'edit' in request.POST:
            name = request.POST.get('sid')
            edit_obj = Student.objects.get(id=name)
            return render(request, 'edit.html', {'stu_edit': edit_obj})
        elif 'del' in request.POST:
            name = request.POST.get('sid')
            del_stu = Student.objects.get(id=name)
            del_stu.delete()
            show_all = Student.objects.all()
            return render(request, 'index.html', {'data': show_all})
        elif 'update' in request.POST:
            uid = request.POST.get('sid')
            upname = request.POST.get('uname')
            upcode = request.POST.get('ucode')
            upnum = request.POST.get('unum')
            print(uid, upname, upcode, upnum)
            # Updating the records
            sql = "UPDATE dataapp_student SET fullname = '" + upname + "',mobile ='" + upnum + "',stu_code ='" + upcode + "' where id='" + uid + "'"
            cursor1.execute(sql)
            print("Table updated...... ")
            return redirect("data")



def insert(request):
    if request.method == "GET":
        return render(request, 'insert.html')
    else:
        name = request.POST.get('fname')
        code = request.POST.get('scode')
        mobile = request.POST.get('num')
        print(name, mobile, code)
        savecard = Student()
        # here fullname , stu_code, mobile is database field name
        savecard.fullname = name
        savecard.stu_code = code
        savecard.mobile = mobile
        savecard.save()
        messages.success(request, "Employee " + savecard.fullname + " is saved successfully")
        return render(request, 'insert.html')

"""
