# app.py
from flask import Flask, render_template, url_for, request, redirect, jsonify
from models import db, Product, Collection, EngagementPost, EngagementPostContent
from sqlalchemy import func
from config import Config
from sqlalchemy import desc
import uuid

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

@app.route("/")
def home():
    return render_template("base.html")

# Route to render form for creating a new product
@app.route("/product/new")
def new_product():
    return render_template("create_product.html")

# Route to create a new product
@app.route('/product', methods=['POST'])
def create_product():
    name = request.form.get("name")
    image_url = request.form.get("image_url")
    sku = request.form.get("sku")
    new_product = Product(name=name, image_url=image_url, sku=sku)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for("home"))

# Route to render form for creating a new collection
@app.route("/collection/new")
def new_collection():
    return render_template("create_collection.html")

# Route to create a new collection without posts
@app.route('/collection', methods=['POST'])
def create_collection():
    name = request.form.get("name")
    new_collection = Collection(name=name)
    db.session.add(new_collection)
    db.session.commit()
    return redirect(url_for("home"))

# Route to render the form for creating a collection with posts
@app.route("/collection-with-posts/new")
def new_collection_with_posts():
    return render_template("create_collection_with_posts.html")

# Route to create a new collection with associated post IDs
@app.route('/collection-with-posts', methods=['POST'])
def create_collection_with_posts():
    name = request.form.get("name")
    post_ids = request.form.get("post_ids").split(',')  # Retrieve and split post IDs

    if not name:
        return jsonify({"error": "Collection name is required"}), 400

    # Create the new collection
    new_collection = Collection(name=name)
    db.session.add(new_collection)

    # Fetch and associate posts with the collection
    posts = EngagementPost.query.filter(EngagementPost.engagement_post_id.in_(post_ids)).all()
    new_collection.posts.extend(posts)

    db.session.commit()
    return redirect(url_for("view_collections"))

# Route to view all collections
@app.route("/collections")
def view_collections():
    collections = Collection.query.all()
    return render_template("view_collections.html", collections=collections)

# Fetch posts with content and products for a given tenant_id
@app.route('/posts-with-content', methods=['GET'])
def fetch_posts_with_content():
    tenant_id = request.args.get('tenant_id')
    if not tenant_id:
        return render_template("posts_with_content.html", posts=[])

    # Fetch posts directly from EngagementPost based on tenant_id
    posts = EngagementPost.query.filter_by(tenant_id=tenant_id).all()
    response_data = []
    
    for post in posts:
        # Fetch post content related to the engagement post
        post_contents = EngagementPostContent.query.filter_by(story_id=post.engagement_post_id).all()

        # Build response data for each post
        response_data.append({
            "thumbnail_title": post.thumbnail_title,
            "thumbnail_url": post.thumbnail_url,
            "description": post.description,
            "content_urls": [{"url": content.url, "file_type": content.file_type} for content in post_contents]
        })

    return render_template("posts_with_content.html", posts=response_data)

@app.route("/top-viewed-posts", methods=['GET'])
def show_top_viewed_posts():
    tenant_id = request.args.get('tenant_id')
    if not tenant_id:
        return render_template("top_viewed_posts.html", posts=[])

    # Assuming `number_of_likes` is used as a proxy for "views"
    top_posts_query = EngagementPost.query.filter_by(tenant_id=tenant_id) \
        .order_by(desc(EngagementPost.number_of_likes)) \
        .limit(5) \
        .all()

    posts = [{"thumbnail_title": post.thumbnail_title, "shopping_url": post.shopping_url} for post in top_posts_query]
    return render_template("top_viewed_posts.html", posts=posts)

@app.route('/top-products', methods=['GET', 'POST'])
def get_top_products():
    tenant_id = request.form.get('tenant_id')
    top_products = []
    
    if tenant_id:
        top_products = db.session.query(
            EngagementPost.description.label("product_name"),
            EngagementPostContent.url.label("post_content_url"),
            (EngagementPost.video_duration).label("duration_watched_hours")
        ).join(
            EngagementPostContent, EngagementPost.engagement_post_id == EngagementPostContent.story_id
        ).filter(
            EngagementPost.tenant_id == tenant_id
        ).order_by(
            EngagementPost.number_of_likes.desc()
        ).limit(5).all()
    
    return render_template('top_products.html', top_products=top_products)

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
