"""Route mutasi resep."""
from flask import abort, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, current_user

import config
import recipe_service
import user_service
import validators
from permissions import can_edit_recipe


def register(app):
    @app.route("/tambah", methods=["GET", "POST"])
    @login_required
    def tambah():
        if request.method == "POST":
            data, error = validators.validate_recipe(request.form)
            if error:
                return render_template("tambah.html", mode="tambah",
                                       error=error,
                                       kategori_list=config.KATEGORI_VALID), 400
            new_id = recipe_service.create(data)
            return redirect(url_for("detail", resep_id=new_id))

        return render_template("tambah.html", mode="tambah",
                               kategori_list=config.KATEGORI_VALID)

    @app.route("/resep/<int:resep_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit(resep_id):
        resep = recipe_service.find(resep_id)
        if resep is None:
            abort(404)
        if not can_edit_recipe(resep):
            abort(403)

        if request.method == "POST":
            data, error = validators.validate_recipe(request.form)
            if error:
                return render_template("tambah.html", resep=resep, mode="edit",
                                       error=error,
                                       kategori_list=config.KATEGORI_VALID), 400
            recipe_service.update(resep_id, data)
            return redirect(url_for("detail", resep_id=resep_id))

        return render_template("tambah.html", resep=resep, mode="edit",
                               kategori_list=config.KATEGORI_VALID)

    @app.route("/resep/<int:resep_id>/hapus", methods=["POST"])
    @login_required
    def hapus(resep_id):
        resep = recipe_service.find(resep_id)
        if resep is None:
            abort(404)
        if not can_edit_recipe(resep):
            abort(403)
        recipe_service.delete(resep_id)
        return redirect(url_for("index"))

    @app.route("/resep/<int:resep_id>/favorit", methods=["POST"])
    @login_required
    def toggle_favorit(resep_id):
        if recipe_service.find(resep_id) is None:
            abort(404)
        recipe_service.toggle_favorite(resep_id)
        
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            record = user_service.current_record()
            is_fav = resep_id in record.get("favorit_ids", [])
            return jsonify({"status": "ok", "is_favorit": is_fav})
            
        return redirect(request.referrer or url_for("index"))

    @app.route("/resep/<int:resep_id>/rating", methods=["POST"])
    @login_required
    def simpan_rating(resep_id):
        if recipe_service.find(resep_id) is None:
            abort(404)
        try:
            rating = int(request.form.get("rating", "0"))
        except (TypeError, ValueError):
            rating = 0
        if rating not in config.RATING_VALID:
            rating = 0
        catatan = request.form.get("catatan", "").strip()[:config.MAX_CATATAN]
        recipe_service.set_rating(resep_id, rating, catatan)
        return redirect(url_for("detail", resep_id=resep_id))

    @app.route("/resep/<int:resep_id>/like", methods=["POST"])
    @login_required
    def toggle_like(resep_id):
        if recipe_service.find(resep_id) is None:
            abort(404)
        recipe_service.toggle_like(resep_id)
        
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            resep_baru = recipe_service.find(resep_id)
            likes = resep_baru.get("likes", [])
            is_liked = int(current_user.id) in likes
            return jsonify({"status": "ok", "likes_count": len(likes), "is_liked": is_liked})
            
        return redirect(url_for("detail", resep_id=resep_id) + "#like-section")