import random

from faker import Faker
from sqlalchemy import delete

from app.extensions import db
from app import app
from app.models import (
    Offer,
    Request,
    RequestStatus,
    SessionFormat,
    Skill,
    SkillCategory,
    User,
    UserSkill,
    SkillLevel,
)

faker = Faker()
session = db.session

USER_COUNT = 8
SKILL_COUNT = 10
REQUEST_COUNT = 12
OFFER_COUNT = 15


def audit_fields(user=None):
    return {
        "created_by": user.email if hasattr(user, 'email') else 'system',
        "updated_by": user.email if hasattr(user, 'email') else 'system',
        "version": 1,
    }


def clear_data():
    session.execute(delete(Offer))
    session.execute(delete(Request))
    session.execute(delete(UserSkill))
    session.execute(delete(Skill))
    session.execute(delete(SkillCategory))
    session.execute(delete(User))


def create_users(count):
    users = []
    for index in range(count):
        user = User(
            email=f"user{index + 1}_{faker.unique.slug()}@example.com",
            password="password123",
            name=faker.name(),
            bio=faker.text(max_nb_chars=120),
            address=faker.address(),
            avatar=faker.image_url(),
            **audit_fields(),
        )
        users.append(user)

    session.add_all(users)
    session.flush()
    return users


def create_skills(count):
    category_names = ["Programming", "Design", "Writing", "Business"]
    categories = [
        SkillCategory(name=name, **audit_fields())
        for name in category_names
    ]
    session.add_all(categories)
    session.flush()

    skills = []
    for _ in range(count):
        skill = Skill(
            name=f"{faker.job()} {faker.word().title()}",
            category_id=random.choice(categories).id,
            **audit_fields(),
        )
        skills.append(skill)

    session.add_all(skills)
    session.flush()
    return skills


def create_user_skills(users, skills):
    user_skills = []
    levels = list(SkillLevel)

    for user in users:
        assigned_skills = random.sample(skills, k=min(3, len(skills)))
        for skill in assigned_skills:
            user_skill = UserSkill(
                user_id=user.id,
                skill_id=skill.id,
                level=random.choice(levels),
            )
            user_skills.append(user_skill)

    session.add_all(user_skills)
    session.flush()
    return user_skills


def create_requests(count, users, user_skills):
    requests = []
    statuses = list(RequestStatus)
    formats = list(SessionFormat)

    for _ in range(count):
        owner = random.choice(users)
        owner_skill_options = [
            user_skill for user_skill in user_skills if user_skill.user_id == owner.id
        ]
        request = Request(
            owner_id=owner.id,
            owner_skill_id=random.choice(owner_skill_options).id if owner_skill_options else None,
            status=random.choice(statuses),
            format=random.choice(formats),
            title=faker.sentence(nb_words=6),
            description=faker.text(max_nb_chars=200),
            duration=random.choice(["30 mins", "1 hour", "2 hours"]),
            availability=faker.day_of_week(),
            **audit_fields(owner),
        )
        requests.append(request)

    session.add_all(requests)
    session.flush()
    return requests


def create_offers(count, users, requests):
    offers = []

    for _ in range(count):
        request = random.choice(requests)
        offer_candidates = [user for user in users if user.id != request.owner_id]
        if not offer_candidates:
            continue

        skills = random.choice(offer_candidates).skills
        offerer = random.choice(skills)
        offer = Offer(
            offerer_id=offerer.id,
            request_id=request.id,
            message=faker.paragraph(nb_sentences=3),
            **audit_fields(offerer.user),
        )
        offers.append(offer)

    session.add_all(offers)
    session.flush()
    return offers


def main():
    try:
        clear_data()
        users = create_users(USER_COUNT)
        skills = create_skills(SKILL_COUNT)
        user_skills = create_user_skills(users, skills)
        requests = create_requests(REQUEST_COUNT, users, user_skills)
        offers = create_offers(OFFER_COUNT, users, requests)
        session.commit()
        print(
            f"Seeded {len(users)} users, {len(skills)} skills, "
            f"{len(requests)} requests, and {len(offers)} offers."
        )
    except Exception as exc:
        session.rollback()
        print(f"Something happened while seeding data: {exc}")


with app.app_context():
    main()
