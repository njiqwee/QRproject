from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        attendee = request.form.get('attendee')#Gets the note from the HTML

        if len(attendee) < 1:
            flash('Name is too short!', category='error')
        else:
            new_attendance = Attendance(owner_id=current_user.id, owner_name=current_user.first_name,
                                        attendee_id="NULL", attendee_name=attendee)  #providing the schema for the note
            db.session.add(new_attendance) #adding the new_attendance to the database
            db.session.commit()
            flash('new_attendance added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-attendance', methods=['POST'])
@login_required
def delete_attendance():
    attendance = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    attendanceId = attendance['attendanceId']
    attendance = Attendance.query.get(attendanceId)
    if attendance:
        if attendance.owner_id == current_user.id:
            db.session.delete(attendance)
            db.session.commit()

    return jsonify({})
