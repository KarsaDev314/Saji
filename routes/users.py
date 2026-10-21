"""Route profil, follow, pengaturan, daftar pengguna."""
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

import config
import recipe_service
import user_service
import validators
from models import to_public_dict
from permissions import current_id


def register(app):
    @app.route("/profil/<username>")
    def profil(username):
        users = user_service.all()
        target = user_service.find_by_username(username)
        if not target:
            abort(404)

        resep_user = recipe_service.by_owner(recipe_service.all(), target["id"])
        follower_count, following_count, following_users = user_service.follow_stats(
            users, target["id"]
        )

        me_id = current_id()
        sudah_follow = False
        if me_id:
            me = user_service.find_record_by_id(me_id)
            if me and target["id"] in me.get("following", []):
                sudah_follow = True

        return render_template(
            "profil.html",
            user_pub=to_public_dict(target),
            resep_list=resep_user,
            total_resep=len(resep_user),
            follower_count=follower_count,
            following_count=following_count,
            following_users=following_users,
            sudah_follow=sudah_follow,
            user_id=target["id"],
            user_idku=me_id,
        )

    @app.route("/follow/<int:target_id>", methods=["POST"])
    @login_required
    def toggle_follow(target_id):
        result = user_service.toggle_follow(target_id)
        if result is None:
            abort(404)
        flash(*result)
        return redirect(request.referrer or url_for("index"))

    @app.route("/pengaturan", methods=["GET", "POST"])
    @login_required
    def pengaturan():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            bio = request.form.get("bio", "").strip()

            error = validators.validate_username_format(username)
            if not error:
                other = user_service.find_by_username(username)
                if other and other["id"] != int(current_user.id):
                    error = "Username sudah dipakai user lain."
            if not error:
                error = validators.validate_bio(bio)
            if error:
                return render_template("pengaturan.html", error=error), 400

            user_service.update_profile(int(current_user.id), username, bio)
            flash("Profil berhasil diperbarui.", config.FLASH_SUKSES)
            return redirect(url_for("profil", username=username))

        return render_template("pengaturan.html")

    @app.route("/pengguna")
    @login_required
    def daftar_pengguna():
        return render_template(
            "pengguna.html",
            daftar_user=user_service.list_other_users(int(current_user.id)),
        )