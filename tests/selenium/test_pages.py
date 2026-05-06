import os
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.extensions import db


pytestmark = pytest.mark.selenium
STEP_DELAY_SECONDS = float(os.environ.get("SELENIUM_STEP_DELAY", "1"))


def wait_for(browser, timeout=10):
    return WebDriverWait(browser, timeout)


def human_pause():
    if STEP_DELAY_SECONDS > 0:
        time.sleep(STEP_DELAY_SECONDS)


def login_through_ui(browser, base_url, email, password):
    browser.get(f"{base_url}/login")
    human_pause()
    wait_for(browser).until(EC.presence_of_element_located((By.ID, "email")))
    browser.find_element(By.ID, "email").send_keys(email)
    human_pause()
    browser.find_element(By.ID, "password").send_keys(password)
    human_pause()
    browser.find_element(By.CSS_SELECTOR, "#loginForm button").click()
    human_pause()
    wait_for(browser).until(EC.url_contains("/dashboard"))


def test_home_page_shows_brand_and_primary_links(browser, server_url):
    browser.get(server_url)
    human_pause()

    assert browser.title == "Skillswap"
    assert "SkillSwap" in browser.find_element(By.CSS_SELECTOR, "nav").text
    assert "Trade what you" in browser.find_element(By.TAG_NAME, "h1").text
    assert browser.find_element(By.LINK_TEXT, "LOGIN").is_displayed()
    assert browser.find_element(By.LINK_TEXT, "SIGN UP").is_displayed()


def test_home_page_shows_how_it_works_sections(browser, server_url):
    browser.get(server_url)
    human_pause()

    page_text = browser.find_element(By.TAG_NAME, "body").text

    assert "How it works" in page_text
    assert "List your skills" in page_text
    assert "Post a request" in page_text
    assert "Accept & connect" in page_text


def test_login_page_shows_form_controls(browser, server_url):
    browser.get(f"{server_url}/login")
    human_pause()

    wait_for(browser).until(
        EC.presence_of_element_located((By.ID, "loginForm"))
    )

    assert browser.find_element(By.ID, "email").is_displayed()
    assert browser.find_element(By.ID, "password").is_displayed()
    submit = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert submit.text == "LOGIN"


def test_login_page_has_skill_swap_navigation(browser, server_url):
    browser.get(f"{server_url}/login")
    human_pause()

    nav = browser.find_element(By.CSS_SELECTOR, "nav")
    page_text = browser.find_element(By.TAG_NAME, "body").text

    assert "SkillSwap" in nav.text
    assert "Log in to continue exploring and sharing skills." in page_text


def test_private_page_redirects_to_login(browser, server_url):
    browser.get(f"{server_url}/dashboard")
    human_pause()

    wait_for(browser).until(EC.url_contains("/login"))
    human_pause()

    assert browser.find_element(By.TAG_NAME, "h4").text == "Login"


def test_user_can_log_in_and_see_dashboard(browser, server_url, user_factory):
    user_factory(email="selenium@example.com", password="password123")

    login_through_ui(
        browser,
        server_url,
        "selenium@example.com",
        "password123",
    )

    assert browser.find_element(By.CSS_SELECTOR, ".page-title").text == (
        "Dashboard"
    )
    assert browser.find_element(By.LINK_TEXT, "LOGOUT").is_displayed()


def test_dashboard_page_shows_quick_actions(browser, server_url, user_factory):
    user_factory(email="dashboard@example.com", password="password123")

    login_through_ui(
        browser,
        server_url,
        "dashboard@example.com",
        "password123",
    )

    body_text = browser.find_element(By.TAG_NAME, "body").text

    assert "My requests" in body_text
    assert "My offering" in body_text
    assert browser.find_element(By.ID, "btnCreateRequest").is_displayed()


def test_profile_shows_authenticated_users_skills(
    browser,
    server_url,
    user_factory,
    skill_factory,
):
    user = user_factory(email="profile@example.com", password="password123")
    skill_factory(user=user, name="Photography")

    login_through_ui(browser, server_url, "profile@example.com", "password123")
    browser.get(f"{server_url}/profile")
    human_pause()

    wait_for(browser).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".skill-row"))
    )
    skills_list = browser.find_element(By.ID, "offer-skills-list")
    skill_count = browser.find_element(By.CSS_SELECTOR, ".section-label")
    assert "Photography" in skills_list.text
    assert "1 SKILLS" in skill_count.text


def test_profile_page_shows_empty_skill_state(
    browser,
    server_url,
    user_factory,
):
    user_factory(email="empty-profile@example.com", password="password123")

    login_through_ui(
        browser,
        server_url,
        "empty-profile@example.com",
        "password123",
    )
    browser.get(f"{server_url}/profile")
    human_pause()

    body_text = browser.find_element(By.TAG_NAME, "body").text

    assert "Skills I Offer" in body_text
    assert "You haven't added any skills yet." in body_text


def test_requests_page_displays_search_and_sample_cards(
    browser,
    server_url,
    user_factory,
):
    user_factory(email="requests@example.com", password="password123")

    login_through_ui(
        browser,
        server_url,
        "requests@example.com",
        "password123",
    )
    browser.get(f"{server_url}/requests/")
    human_pause()

    wait_for(browser).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".requests-card"))
    )
    cards = browser.find_elements(By.CSS_SELECTOR, ".requests-card")
    search = browser.find_element(By.CSS_SELECTOR, ".requests-search-input")

    assert len(cards) == 3
    assert search.get_attribute("placeholder") == "Search requests..."


def test_requests_page_shows_filter_chips(browser, server_url, user_factory):
    user_factory(email="filters@example.com", password="password123")

    login_through_ui(
        browser,
        server_url,
        "filters@example.com",
        "password123",
    )
    browser.get(f"{server_url}/requests/")
    human_pause()

    filters = [
        chip.text
        for chip in browser.find_elements(
            By.CSS_SELECTOR,
            ".requests-filter-chip",
        )
    ]

    assert filters == ["All", "Open", "Beginner", "Online"]


def test_request_detail_page_shows_seeded_request(
    browser,
    server_url,
    user_factory,
    skill_factory,
    request_factory,
):
    user = user_factory(
        email="detail@example.com",
        password="password123",
        name="Riley Owner",
    )
    user.address = "Perth, AU"
    user.bio = "Shares practical lessons."
    db.session.commit()
    skill = skill_factory(user=user, name="Python")
    request = request_factory(
        owner_skill=skill,
        title="Need guitar coaching",
    )

    login_through_ui(browser, server_url, "detail@example.com", "password123")
    browser.get(f"{server_url}/requests/{request.id}")
    human_pause()

    wait_for(browser).until(
        EC.presence_of_element_located((By.ID, "request-data"))
    )
    body_text = browser.find_element(By.TAG_NAME, "body").text

    assert "Need guitar coaching" in body_text
    assert "Request Details" in body_text
    assert "Looking for beginner lessons." in body_text
    assert "Python" in body_text
    assert "About Riley Owner" in body_text
    assert "Session Preferences" in body_text
    assert browser.find_element(By.ID, "btn-cancel-request").is_displayed()
