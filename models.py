# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'engagement_post_product'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, image_url, sku):
        self.name = name
        self.image_url = image_url
        self.sku = sku

class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)

    # Relationship to EngagementPost
    posts = relationship('EngagementPost', secondary='collection_post_link', back_populates='collections')

class EngagementPost(db.Model):
    __tablename__ = 'engagement_post'

    engagement_post_id = db.Column(BigInteger, primary_key=True)
    tenant_id = db.Column(BigInteger, nullable=False)
    thumbnail_title = db.Column(db.String(200), nullable=True)
    thumbnail_url = db.Column(db.String(200), nullable=True)
    number_of_likes = db.Column(BigInteger, nullable=True, default=0)
    number_of_shares = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    shopping_url = db.Column(db.String(200), nullable=True)
    video_duration = db.Column(db.Float, nullable=True)

    # Relationship to Collection
    collections = relationship('Collection', secondary='collection_post_link', back_populates='posts')
    
    # Relationship to EngagementPostContent
    contents = relationship('EngagementPostContent', back_populates='engagement_post')

class CollectionPostLink(db.Model):
    __tablename__ = 'collection_post_link'

    collection_id = db.Column(UUID(as_uuid=True), ForeignKey('collection.id'), primary_key=True)
    post_id = db.Column(BigInteger, ForeignKey('engagement_post.engagement_post_id'), primary_key=True)

class EngagementPostContent(db.Model):
    __tablename__ = 'engagement_post_content'

    engagement_post_content_id = db.Column(BigInteger, primary_key=True)
    file_type = db.Column(db.String(50), nullable=True)
    story_id = db.Column(BigInteger, ForeignKey('engagement_post.engagement_post_id'), nullable=False)
    url = db.Column(db.String(200), nullable=True)
    thumbnail_url = db.Column(db.String(200), nullable=True)
    sequence = db.Column(db.Integer, nullable=True)

    # Relationship to EngagementPost
    engagement_post = relationship('EngagementPost', back_populates='contents')
