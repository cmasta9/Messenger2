from hashlib import blake2b
from flask import Blueprint,request,session,g,url_for,redirect,render_template,flash

fn = 'uzr'

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        un = request.form['un']
        pw = request.form['pw']

        error = None

        if not un or not pw:
            error = 'Username and password are required'
            return redirect(url_for('auth.register'))

        res = getAuth(un,pw)

        if res == -2:
            if appendDic(un,hashPass(pw)) is not False:
                return redirect(url_for('auth.login'))
            else:
                error = 'There was an error registering the new user'
        else:
            error = 'Username already exists'
        
        if error is not None:
            flash(error)
    return render_template('auth/register.html')
            
@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        un = request.form['un']
        pw = request.form['pw']

        error = None

        if not un or not pw:
            error = 'Username and password are required'
            return render_template('auth/login.html')

        res = getAuth(un,pw)

        if res == 1:
            session.clear()
            session['user'] = un
            return redirect(url_for('index'))
        elif res == -2:
            error = 'User does not exist'
        elif res == -1:
            error = 'Incorrect password'

        if error is not None:
            flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def logged():
    u = session.get('user')
    if u is not None:
        g.user = u
    else:
        g.user = None

def getAuth(u,p):
    dic = mkDic()
    if u in dic.keys():
        if dic[u] == str(hashPass(p)):
            print('pass match')
            return 1
        else:
            return -1
    else:
        return -2

def hashPass(p):
    return blake2b(str.encode(p),digest_size=32).digest()

def getSec(fn='secrit'):
    f = open(fn)
    s = f.readline()
    f.close()
    return s

def mkDic(f=fn):
    uz = {}
    fl = open(f,'r')
    l = fl.readline()
    while l is not '':
        l = l.strip().split(',')
        uz[l[0]] = l[1]
        l = fl.readline()
    fl.close()
    return uz

def appendDic(u,p,f=fn):
    uz = mkDic(f)
    if u not in uz.keys():
        fl = open(f,'a')
        fl.write(f'{u},{p}\n')
        fl.close()
        print('appended',u,p)
        return u
    else:
        return False