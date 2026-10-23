"""Route profil, follow, pengaturan, daftar pengguna."""
from flask import abort, flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required

import config
import recipe_service
import user_service
import validators
from models import to_public_dict
from permissions import current_id

import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid
import config

def register(app):
    @app.route("/profil/<username>")
    def profil(username):
        users = user_service.all()
        target = user_service.find_by_username(username)
        if not target:
            abort(404)

        resep_user = recipe_service.by_owner(recipe_service.all(), target["id"])
        
        # Ambil 4 nilai dari follow_stats (termasuk followers_list)
        follower_count, following_count, following_users, followers_list = user_service.follow_stats(
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
            followers_list=followers_list,
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
            
        pesan, kategori = result
        
        # AJAX Handling
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            users = user_service.all()
            follower_count = sum(1 for u in users if target_id in u.get("following", []))
            me = user_service.current_record()
            is_follow = target_id in me.get("following", [])
            
            return jsonify({
                "status": "ok", 
                "is_follow": is_follow, 
                "follower_count": follower_count
            })
            
        # Fallback redirect
        flash(pesan, kategori)
        return redirect(request.referrer or url_for("index"))
    @app.route("/pengaturan", methods=["GET", "POST"])
    @login_required
    def pengaturan():
        # Tarik data terbaru dari database buat nampilin foto lama
        user_data = user_service.find_record_by_id(int(current_user.id))

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

                # --- LOGIKA HAPUS FOTO LAMA ---
                old_pic = user_data.get("profile_pic")
                if old_pic and old_pic != "default_avatar.png":
                    old_filepath = os.path.join(current_app.root_path, config.UPLOAD_FOLDER, old_pic)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath) # Hapus file lama dari folder

            user_service.update_profile(int(current_user.id), username, bio, filename)
            flash("Profil berhasil diperbarui.", config.FLASH_SUKSES)
            return redirect(url_for("profil", username=username))

        return render_template("pengaturan.html", user_data=user_data)

    @app.route("/pengguna")
    @login_required
    def daftar_pengguna():
        return render_template(
            "pengguna.html",
            daftar_user=user_service.list_other_users(int(current_user.id)),
        )