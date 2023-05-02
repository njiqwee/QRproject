from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db

QR = Blueprint('QR', __name__)


@QR.route('/QRtoDB', methods=['GET', 'POST'])
@login_required
def qr_to_db():
    if request.method == 'POST':
        data = request.get_json()
        text = data['text']
        owner_id = int(text.split("-")[0])
        owner = db.session.query(User).filter_by(id=owner_id).first()
        attendee_exists = db.session.query(Attendance).filter_by(attendee_id=current_user.id).first() is not None
        if attendee_exists:
            print("An attendee with this ID already exists")
            flash("An attendee with this ID already exists", category='success')
            return jsonify()
        else:
            if text == owner.token:
                new_attendee = Attendance(owner_id=int(text.split("-")[0]), owner_name=owner.first_name,
                                          attendee_id=current_user.id, attendee_name=current_user.first_name)
                db.session.add(new_attendee)
                db.session.commit()
                flash("success add", category='success')
                print("success add")
                return jsonify()
            else:
                flash("wrong token. try again", category='error')
                print("wrong token. expected " + owner.token + " got " + text)
                return jsonify()

    return render_template("scan.html", user=current_user)


@QR.route('/genQR', methods=['GET', 'POST'])
@login_required
def gen_qr():
    if request.method == 'POST':
        data = request.get_json()
        text = data['text']
        owner = db.session.query(User).filter_by(id=current_user.id).first()
        owner.token = text
        db.session.commit()

    return render_template("generate.html", user=current_user, idtoqr=current_user.id)
