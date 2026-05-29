import  pytest
import requests

url_agent = "https://playground.learnqa.ru/ajax/api/user_agent_check"

test_data = [
    (
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mobile", "No", "Android"
    ),
    (
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "Mobile", "Chrome", "iOS"
    ),
    (
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Googlebot", "Unknown", "Unknown"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "Web", "Chrome", "No"
    ),
    (
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Mobile", "No", "iPhone"
    ),
]

@pytest.mark.parametrize(
    "ua,exp_platform,exp_browser,exp_device", 
    test_data,
    ids=["Android_Galaxy", "iPad_Chrome", "Googlebot", "Windows_Edge", "iPad_iPhone"]
    )
def test_ua(ua, exp_platform, exp_browser, exp_device):
    response = requests.get(url_agent, headers={"User-Agent": ua })
    response1 = response.json()

    assert response1["platform"] == exp_platform, \
        f"Platform mismatch. UA: '{ua[:60]}...'. Expected: '{exp_platform}', got: '{response1['platform']}'"

    assert response1["browser"] == exp_browser, \
        f"Browser mismatch. UA: '{ua[:60]}...'. Expected: '{exp_browser}', got: '{response1['browser']}'"

    assert response1["device"] == exp_device, \
        f"Device mismatch. UA: '{ua[:60]}...'. Expected: '{exp_device}', got: '{response1['device']}'"

