# -*- coding:utf-8 -*-

# for email 
import smtplib
from email.mime.text import MIMEText

from flask import Flask,flash,url_for, render_template,json, request,redirect
#import pymysql as pm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://gm:1027@localhost:3306/Atomy'
app.secret_key = "super secret key"

db = SQLAlchemy(app)

class TblUser(db.Model):
    user_id = Column(db.Integer, nullable=False, primary_key=True)
    user_name = Column(db.String(45), nullable=False, default='')
    user_username = Column(db.String(45), nullable=False, default='')
    user_phone = Column(db.String(45), nullable=False, default='')
    user_address = Column(db.String(45), nullable=False, default='')
    user_bank = Column(db.String(45), nullable=False, default='')
    extra = Column(db.String(45), nullable=False, default='')

def sendMail(me, you, text):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(me, 'jpqyvalaleozqboq')

    msg = MIMEText(text, _charset='euc-kr')
    msg['Subject'] = '[Atomy] 새로운 회원정보 알림'
    msg['From'] = me
    msg['To'] = you

    smtp.sendmail(me, you, msg.as_string())
    smtp.quit()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/showSignUp", methods=['GET'])
def showSignUp():
    return render_template('signup.html')

@app.route("/signUp", methods=['POST'])
def signUp():
    # create user code
    try:
        print("start of try loop")
        # read the posted values from UI
        _name = request.form['inputName']
        _password = request.form['inputPassword'] # extra in db 
        _id = request.form['userId']
        _phone = request.form['phone']
        _address = "({0}) {1} {2}".format(request.form['sample3_postcode'],request.form['sample3_address'], request.form['postDetail'])
        _bankName = request.form['bankName']
        _bankAccount = request.form['bankAccount']
        _bank = _bankName + " " + _bankAccount
        
        new_user = TblUser(user_name = _name, extra = _password, \
                            user_username = _id, user_phone = _phone, \
                            user_address = _address, user_bank = _bank)
        db.session.add(new_user)
        db.session.commit()
        print("user registered")
        msg_list = []
        msg_list.append(" 이름: {0}".format(_name))
        msg_list.append(" ID : {0}".format(_id))
        msg_list.append(" 비밀번호 : {0}".format(_password))
        msg_list.append(" 휴대폰 번호 : {0}".format(_phone))
        msg_list.append(" 주소 : {0}".format(_address))
        msg_list.append(" 계좌번호 : {0}".format(_bank))


        msg = "\n".join(msg_list)
        
         # validate the received values
        if _address:
            sendMail('choigyumin@gmail.com', 'uricom723@nate.com', msg)
            flash("성공적으로 신청되셨습니다.")
            return redirect(url_for('index'))
            # return json.dumps({'html':'<span>All fields good !!</span>'})
        else:
            flash("신청할 수 없습니다. 빠진항목이 없는지 확인해주세요.")
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        print(str(e))
        flash("신청할 수 없습니다. 빠진항목이 없는지 확인해주세요.")
        return json.dumps({'html':'<span>Exception Occurred.</span>'})


#if __name__ == "__main__":
#    app.run(host="0.0.0.0")


