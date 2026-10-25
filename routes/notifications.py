from flask import render_template
from flask_login import login_required, current_user
from services import notification_service

def register(app):
    # UBAH /notifikasi JADI /notifications
    @app.route("/notifications")
    @login_required
    def notifikasi():
        notifs = notification_service.fetch_and_mark_read(int(current_user.id))
        return render_template("notifikasi.html", notif_list=notifs)