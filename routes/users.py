import os
import uuid
from flask import render_template, request, redirect, url_for, abort, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from services import user_service, recipe_service
from core.models import to_public_dict
from utils import validators
import config

def register(app):
    # UBAH /profil/ JADI /users/
    @app.route("/users/<username>")
    def profil(username):
        target = user_service.find_by_username(username)
        if not target: abort(404)
        
        resep_user = recipe_service.by_owner(recipe_service.all(), target["id"])
        
        return render_template(
            "profil.html", 
            user_pub=to_public_dict(target), 
            resep_list=resep_user,
            total_resep=len(resep_user),
            follower_count=0,
            following_count=0,
            following_users=[],
            sudah_follow=False,
            user_id=target["id"], 
            user_idku=int(current_user.id) if current_user.is_authenticated else None
        )

    # UBAH /pengguna JADI /users
    @app.route("/users")
    @login_required
    def daftar_pengguna():
        return render_template("pengguna.html", daftar_user=user_service.list_other_users(int(current_user.id)))

    # UBAH /follow/ JADI /users/<id>/follow
    @app.route("/users/<int:target_id>/follow", methods=["POST"])
    @login_required
    def toggle_follow(target_id):
        res = user_service.toggle_follow(target_id)
        if res:
            if res.get("status") == "error":
                flash(res.get("message"), "danger")
            else:
                flash("Berhasil memperbarui status mengikuti.", "sukses")
        return redirect(request.referrer or url_for("index"))

    # UBAH /pengaturan JADI /settings
    @app.route("/settings", methods=["GET", "POST"])
    @login_required
    def pengaturan():
        user_data = user_service.find_record_by_id(current_user.id)
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            bio = request.form.get("bio", "").strip()
            
            error = validators.validate_username_format(username)
            if not error:
                other = user_service.find_by_username(username)
                if other and other["id"] != int(current_user.id):
                    error = "Username sudah dipakai user lain."
            if error:
                return render_template("pengaturan.html", error=error, user_data=user_data), 400

            # --- LOGIKA UPLOAD FOTO PROFIL ---
            file = request.files.get("profile_pic")
            filename = None
            
            if file and file.filename != '':
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                if ext not in config.ALLOWED_EXTENSIONS:
                    return render_template("pengaturan.html", error="Format gambar harus JPG, PNG, atau GIF.", user_data=user_data), 400
                
                filename = f"user_{current_user.id}_{uuid.uuid4().hex[:6]}.{ext}"
                filepath = os.path.join(current_app.root_path, config.UPLOAD_FOLDER, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)

                                # Hapus foto lama
                old_pic = user_data.get("profile_pic")
                if old_pic and old_pic != "default_avatar.png":
                    old_filepath = os.path.join(
                        current_app.root_path, config.UPLOAD_FOLDER, old_pic
                    )
                    try:
                        if os.path.exists(old_filepath):
                            os.remove(old_filepath)
                    except OSError as e:
                        current_app.logger.warning(
                            f"Gagal hapus foto lama {old_filepath}: {e}"
                        )

            user_service.update_profile(int(current_user.id), username, bio, filename)
            flash("Profil berhasil diperbarui.", "sukses")
            return redirect(url_for("profil", username=username))
            
        return render_template("pengaturan.html", user_data=user_data)