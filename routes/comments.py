from flask import render_template, request, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from services import comment_service, recipe_service
from utils.permissions import can_moderate_comment
import config

def register(app):
    @app.route("/resep/<int:resep_id>/komentar", methods=["POST"])
    @login_required
    def tambah_komentar(resep_id):
        teks = request.form.get("teks", "").strip()
        if not teks:
            return jsonify({"status": "error", "message": "Kosong"}), 400
        
        parent_id = request.form.get("parent_id")
        new_komentar = comment_service.add(resep_id, teks, parent_id)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            resep = recipe_service.find(resep_id)
            html = render_template("_komentar_item.html", k=new_komentar, resep=resep, boleh_moderasi_komentar=can_moderate_comment)
            return jsonify({"status": "ok", "html": html})
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<int:komentar_id>/hapus", methods=["POST"])
    @login_required
    def hapus_komentar(resep_id, komentar_id):
        resep = recipe_service.find(resep_id)
        if not resep: abort(404)
        k = comment_service.find_comment_by_id(komentar_id)
        if k and can_moderate_comment(k, resep):
            comment_service.delete(resep_id, komentar_id)
            
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "ok"})
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<int:komentar_id>/edit", methods=["POST"])
    @login_required
    def edit_komentar(resep_id, komentar_id):
        resep = recipe_service.find(resep_id)
        if not resep: abort(404)
        teks_baru = request.form.get("teks", "").strip()
        k = comment_service.find_comment_by_id(komentar_id)
        if k and can_moderate_comment(k, resep) and teks_baru:
            comment_service.update_text(resep_id, komentar_id, teks_baru)
            
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "ok", "teks": teks_baru})
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<int:komentar_id>/like", methods=["POST"])
    @login_required
    def like_komentar(resep_id, komentar_id):
        comment_service.toggle_reaction(resep_id, komentar_id, "like")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "ok"})
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")

    @app.route("/resep/<int:resep_id>/komentar/<int:komentar_id>/dislike", methods=["POST"])
    @login_required
    def dislike_komentar(resep_id, komentar_id):
        comment_service.toggle_reaction(resep_id, komentar_id, "dislike")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"status": "ok"})
        return redirect(url_for("detail", resep_id=resep_id) + "#komentar")