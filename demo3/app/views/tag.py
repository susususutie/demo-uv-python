from flask import Blueprint, request, jsonify, abort
from app.extensions import db
from app.models import Tag
from app.schemas import tag_schema, tags_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict

bp = Blueprint("tag", __name__, url_prefix="/api/tags")


@bp.get("")
def list_tags():
    query = db.session.query(Tag)
    p = request.args.to_dict()

    query = apply_filter(
        query,
        Tag,
        allowed_cols={
            "name": ("name", "contains"),
        },
        params=p,
    )
    query = apply_sort(
        query,
        Tag,
        allowed_cols={"name", "created_at", "updated_at"},
        default_col="created_at",
        default_dir="desc",
        params=p,
    )
    pager = get_page_params(params=p)

    pagination = query.paginate(error_out=False, **pager)

    return jsonify(
        {
            "list": tags_schema.dump(pagination.items),
            "pagination": to_pagination_dict(pagination),
        }
    )


@bp.post("")
def create_tag():
    data = tag_schema.load(request.json)
    
    # Check if tag name already exists
    existing_tag = db.session.query(Tag).filter_by(name=data["name"]).first()
    if existing_tag:
        return jsonify({"error": "Tag name already exists"}), 400
    
    tag = Tag(**data)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag_schema.dump(tag)), 201


@bp.get("/<int:id>")
def get_tag(id):
    tag = db.session.get(Tag, id) or abort(404)
    return jsonify(tag_schema.dump(tag))


@bp.put("/<int:id>")
def update_tag(id):
    tag = db.session.get(Tag, id) or abort(404)
    data = tag_schema.load(request.json, partial=True)
    
    # Check if new name conflicts with existing tag
    if "name" in data:
        existing_tag = db.session.query(Tag).filter(Tag.name == data["name"], Tag.id != id).first()
        if existing_tag:
            return jsonify({"error": "Tag name already exists"}), 400
    if "name" not in data:
        return jsonify({"error": "Tag name is required"}), 400
    
    tag.name = data["name"]
    db.session.commit()
    return jsonify(tag_schema.dump(tag))


@bp.delete("/<int:id>")
def delete_tag(id):
    tag = db.session.get(Tag, id) or abort(404)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"success": True, "message": "Tag deleted"}), 204
