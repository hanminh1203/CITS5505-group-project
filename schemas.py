from database import ma
from models import Offer, Skill, SkillCategory, User, Request, UserSkill

BASE_FIELDS = (
    "id",
)

AUDIT_FIELDS = (
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "version",
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = BASE_FIELDS + (
            "email",
            "name",
            "bio",
            "address",
            "avatar",
        ) + AUDIT_FIELDS
        load_instance = True

class SkillCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SkillCategory
        fields = BASE_FIELDS + (
            "name",
        ) + AUDIT_FIELDS
        load_instance = True

class SkillSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Nested(SkillCategorySchema)
    class Meta:
        model = Skill
        fields = BASE_FIELDS + (
            "name",
            "category",
        ) + AUDIT_FIELDS
        load_instance = True

class UserSkillSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested(UserSchema)
    skill = ma.Nested(SkillSchema)
    class Meta:
        model = UserSkill
        fields = BASE_FIELDS + (
            "level",
            "user",
            "skill",
        )
        load_instance = True

class OfferSchema(ma.SQLAlchemyAutoSchema):
    offerer = ma.Nested(UserSkillSchema)
    class Meta:
        model = Offer
        fields = BASE_FIELDS + (
            "message",
            "offerer",
        ) + AUDIT_FIELDS
        load_instance = True

class RequestSchema(ma.SQLAlchemyAutoSchema):
    offers = ma.Nested(OfferSchema, many=True) 
    owner = ma.Nested(UserSchema)
    class Meta:
        model = Request
        fields = BASE_FIELDS + (
            "status",
            "format",
            "title",
            "description",
            "duration",
            "availability",
            "offers",
            "owner"
        ) + AUDIT_FIELDS
        load_instance = True
