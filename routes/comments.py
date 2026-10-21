"""Route komentar: tambah, edit, hapus, like, dislike."""
from flask import abort, flash, redirect, request, url_for
from flask_login import login_required

import comment_service
import config
import recipe_service
from permissions import can_moderate_comment


def register(app):
    @app.route("/resep/<int:resep_id>/komentar", methods=["POST"])
    @login_required
    def tambah_komentar(resep_id):
        if recipe_service.find(resep_id) is None:
            abort(404)
        teks = request.form.get("teks", "").strip()
        if not teks:
            flash("Komentar tidak boleh kosong.", config.FLASH_INFO)
            return redirect(url_for("detail", resep_id=resep_id) + "#komentar")
        parent_id = request.form.get("parent_id")
        comment_service.add(resep_id, teks, parent_id)
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<komentar_id>/like", methods=["POST"])
    @login_required
    def like_komentar(resep_id, komentar_id):
        comment_service.toggle_reaction(resep_id, komentar_id, "like")
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<komentar_id>/dislike", methods=["POST"])
    @login_required
    def dislike_komentar(resep_id, komentar_id):
        comment_service.toggle_reaction(resep_id, komentar_id, "dislike")
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<komentar_id>/hapus", methods=["POST"])
    @login_required
    def hapus_komentar(resep_id, komentar_id):
        resep = recipe_service.find(resep_id)
        if resep is None:
            abort(404)
        k = comment_service.find(resep.get("comments", []), komentar_id)
        if k and can_moderate_comment(k, resep):
            comment_service.delete(resep_id, komentar_id)
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<komentar_id>/edit", methods=["POST"])
    @login_required
    def edit_komentar(resep_id, komentar_id):
        resep = recipe_service.find(resep_id)
        if resep is None:
            abort(404)
        k = comment_service.find(resep.get("comments", []), komentar_id)
        teks_baru = request.form.get("teks", "").strip()
        if k and can_moderate_comment(k, resep) and teks_baru:
            comment_service.update_text(resep_id, komentar_id, teks_baru)
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")