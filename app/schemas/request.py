from app.extensions import ma
from app.models import Offer, Request, Skill, User

BASE_FIELDS = ("id",)

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
            "initials",
        ) + AUDIT_FIELDS
        load_instance = True

    initials = ma.Method("get_initials")

    def get_initials(self, obj):
        return "".join([part[0].upper() for part in obj.name.strip().split(" ")[0:2]])


class SkillSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Skill
        fields = BASE_FIELDS + ("name", "description", "level") + AUDIT_FIELDS
        load_instance = True


class OfferSchema(ma.SQLAlchemyAutoSchema):
    offer_skill = ma.Nested(SkillSchema)

    class Meta:
        model = Offer
        fields = BASE_FIELDS + ("message", "offer_skill") + AUDIT_FIELDS
        load_instance = True


class RequestSchema(ma.SQLAlchemyAutoSchema):
    offers = ma.Nested(OfferSchema, many=True)
    owner = ma.Nested(UserSchema)
    owner_skill = ma.Nested(SkillSchema)

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
            "owner",
            "owner_skill",
        ) + AUDIT_FIELDS
        load_instance = True
