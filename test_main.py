from httpx import AsyncClient
import pytest
from main import app, fake_db, get_key_from_value, generate_shortened_url


@pytest.fixture(autouse=True)
def setup_db():
    from main import fake_db
    fake_db.clear()  # clear previous entries
    # Add entry into db
    fake_db['https://short.url/lba8tuXU'] ='this-is-a-really-long-url-that-needs-to-be-shortened'

    yield
    fake_db.clear()  # tear down after test


@pytest.mark.anyio
async def test_url_shortener():
    long_url = "this-is-a-really-long-url-that-needs-to-be-shortened"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # call the url shortener endpoint
        response = await ac.get(f'/shorten/{long_url}')
    # turn the response into json to test
    shortened_url = response.json()['url']

    assert response.status_code == 200
    assert shortened_url.startswith("https://short.url/")
    assert len(fake_db) != 0

@pytest.mark.anyio
async def test_redirect_to_longer():
    short_url = 'https://short.url/lba8tuXU'
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # call the redirect_to_longer endpoint
        response = await ac.get(f"/redirect/{short_url}")

    # test the response is a redirect
    assert response.status_code == 307

@pytest.mark.anyio
async def test_redirect():
    short_url = 'https://short.url/lba8tuXU'
    long_url = 'this-is-a-really-long-url-that-needs-to-be-shortened'

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # call the initial redirect
        initial_response = await ac.get(f"/redirect/{short_url}")
        # check it redirected
        assert initial_response.status_code == 307
        redirect_location = initial_response.headers['location']

        # call the redirect endpoint we want
        final_response = await ac.get(redirect_location)
    # turn the response into json to test
    response_data = final_response.json()

    assert response_data['message'] == "You have been redirected to long_url from short_url."
    assert response_data['long_url'] == f'0.0.0:8000/{long_url}'
    assert response_data['short_url'] == short_url


@pytest.mark.anyio
def test_get_key_from_value():
    value = 'this-is-a-really-long-url-that-needs-to-be-shortened'
    expected_key = 'https://short.url/lba8tuXU'
    key = get_key_from_value(value)
    assert key == expected_key
    assert key != "false_key"


@pytest.mark.anyio
def test_generate_shortened_url():
    shortened_url = generate_shortened_url()
    assert shortened_url is not None