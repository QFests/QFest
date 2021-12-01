from app import db
from app.models import User, Alcohol, Comment, Log, Permission, Tag
from flask import render_template, request
from flask_login import current_user
from . import main
from ..alcohol.forms import SearchForm


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main.route('/')
def index():
    search_form = SearchForm()
    the_alcohols = Alcohol.query

    search_tags = request.args.get('search', None)
    page = request.args.get('page', 1, type=int)
    search_form.search.data = search_tags

    if search_tags:
        tags_list = [s.strip() for s in search_tags.split(',') if len(s.strip()) > 0]
        if len(tags_list) > 0:
            if not current_user.can(Permission.UPDATE_ALCOHOL_INFORMATION):
                the_alcohols = Alcohol.query.filter_by(hidden=0)
            the_alcohols = the_alcohols.filter(
                db.and_(*[Alcohol.tags.any(Tag.name.ilike(word)) for word in tags_list])).outerjoin(Log).group_by(
                Alcohol.id).order_by(db.func.count(Log.id).desc())
            pagination = the_alcohols.paginate(page, per_page=16)
            popular_alcohols = pagination.items
    else:
        popular_alcohols = the_alcohols.outerjoin(Log).group_by(Alcohol.id).order_by(db.func.count(Log.id).desc()).limit(12)
    popular_users = User.query.outerjoin(Log).group_by(User.id).order_by(db.func.count(Log.id).desc()).limit(5)
    recently_comments = Comment.query.filter_by(deleted=0).order_by(Comment.edit_timestamp.desc()).limit(5)
    return render_template("index.html", alcohols=popular_alcohols, users=popular_users, recently_comments=recently_comments,
                           search_form=search_form)
