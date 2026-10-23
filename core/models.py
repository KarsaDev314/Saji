def to_public_dict(record):
    return {
        "id": record.id if hasattr(record, 'id') else record.get('id'),
        "username": record.username if hasattr(record, 'username') else record.get('username'),
        "bio": record.bio if hasattr(record, 'bio') else record.get('bio', ''),
        "profile_pic": record.profile_pic if hasattr(record, 'profile_pic') else record.get('profile_pic', 'default_avatar.png'),
        "join_date": str(record.created_at)[:10] if hasattr(record, 'created_at') else record.get('join_date', ''),
    }