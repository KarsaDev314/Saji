from flask import request, jsonify, render_template, redirect, url_for, flash, abort
from core.db import db
from core.db_models import BugReport
from flask_login import current_user, login_required
import config

def register(app):
    @app.route("/api/lapor-bug", methods=["POST"])
    def lapor_bug():
        pesan = request.form.get("pesan_bug", "").strip()
        if not pesan:
            return jsonify({"status": "error", "message": "Pesan tidak boleh kosong."}), 400
        user_id = int(current_user.id) if current_user.is_authenticated else None
        new_report = BugReport(user_id=user_id, message=pesan)
        db.session.add(new_report)
        db.session.commit()
        return jsonify({"status": "ok", "message": "Laporan diterima. Terima kasih!"})

    @app.route("/admin/bugs")
    @login_required
    def admin_bugs():
        if current_user.username != config.ADMIN_USERNAME:
            abort(403)
        reports = BugReport.query.order_by(BugReport.created_at.desc()).all()
        return render_template("admin_bugs.html", reports=reports)

    @app.route("/admin/bugs/<int:bug_id>/resolve", methods=["POST"])
    @login_required
    def resolve_bug(bug_id):
        if current_user.username != config.ADMIN_USERNAME:
            abort(403)
        report = BugReport.query.get_or_404(bug_id)
        report.status = "resolved"
        db.session.commit()
        flash("Laporan bug berhasil ditandai selesai.", "sukses")
        return redirect(url_for("admin_bugs"))