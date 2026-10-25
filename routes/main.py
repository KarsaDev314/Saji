"""Route beranda dan detail resep."""
from flask import abort, render_template, request

import config
from services import recipe_service, user_service # <-- Ada from services
from utils.permissions import can_edit_recipe, can_moderate_comment, current_id # <-- Ada from utils


def register(app):
    @app.route("/")
    def index():
        users = user_service.all()
        all_recipes = recipe_service.all()

        keyword = request.args.get("q", "").strip()
        kategori = request.args.get("kategori", "").strip()
        only_favorite = request.args.get("favorit") == "1"
        if kategori not in config.KATEGORI_VALID:
            kategori = ""

        me_id = current_id()
        requested_mode = request.args.get("mode")

        if me_id and requested_mode == config.MODE_SAYA:
            mode = config.MODE_SAYA
            base = recipe_service.by_owner(all_recipes, me_id)
        elif me_id and requested_mode in (None, config.MODE_FEED):
            mode = config.MODE_FEED
            base = recipe_service.feed(users, all_recipes, me_id)
        else:
            mode = config.MODE_EXPLORE
            base = all_recipes

        favorite_ids = []
        if me_id:
            record = user_service.find_record_by_id(me_id)
            if record:
                favorite_ids = record.get("favorit_ids", [])

        results = recipe_service.filter_(
            base, keyword, kategori, only_favorite, favorite_ids
        )
        users_map = {u["id"]: u["username"] for u in users}

        return render_template(
            "index.html",
            resep_list=results,
            kata_kunci=keyword,
            kategori_aktif=kategori,
            kategori_list=config.KATEGORI_VALID,
            hanya_favorit=only_favorite,
            total_semua=len(all_recipes),
            total_favorit=len(favorite_ids),
            users_map=users_map,
            mode=mode,
            feed_count=len(base),
            favorit_ids=favorite_ids,
        )

    # UBAH URL JADI PLURAL (RESOURCE-BASED)
    @app.route("/recipes/<int:resep_id>")
    def detail(resep_id):
        resep = recipe_service.find(resep_id)
        if resep is None:
            abort(404)
        return render_template(
            "detail.html",
            resep=resep,
            pemilik=recipe_service.owner_public(resep),
            boleh_edit=can_edit_recipe(resep),
            boleh_moderasi_komentar=can_moderate_comment,
            is_favorit=recipe_service.is_favorite(resep_id),
        )