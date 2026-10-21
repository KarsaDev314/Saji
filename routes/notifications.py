"""Route notifikasi."""
from flask import render_template
from flask_login import current_user, login_required

import notification_service


def register(app):
    @app.route("/notifikasi")
    @login_required
    def notifikasi():
        items = notification_service.fetch_and_mark_read(int(current_user.id))
        return render_template("notifikasi.html", notif_list=items)