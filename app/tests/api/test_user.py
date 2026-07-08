from typing import Sequence

import pytest
import sqlalchemy as sa
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import models
from tests import factory as data_factory

pytestmark = pytest.mark.anyio


async def test_get_user_me(
    user_client: AsyncClient, async_session: AsyncSession
):
    users = await async_session.scalars(sa.select(models.User))
    user = users.unique().one()
    response = await user_client.get("/users/me/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert all(
        value == getattr(user, key) for key, value in response_data.items()
    )
    assert "password" not in response_data


async def test_dublicate_email(
    user_client: AsyncClient,
    factory: data_factory.FactoryCallback,
    faker: Faker,
):
    email = faker.email()
    await factory(data_factory.UserFactory, email=email)
    data = {
        "name": faker.name(),
        "email": email,
        "password": faker.password(),
    }
    response = await user_client.post("/users/", json=data)

    assert response.status_code == status.HTTP_409_CONFLICT
    message = f"User with {data['email']} already exist"
    assert response.json()["detail"] == message


async def test_invalid_password(user_client: AsyncClient):
    data = {
        "name": "Bobik",
        "email": "e@example.com",
        "password": "123привет",
    }
    response = await user_client.post("/users/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_login(
    client: AsyncClient, factory: data_factory.FactoryCallback, faker: Faker
):
    password = faker.password()
    email = faker.email()
    user = await factory(
        data_factory.UserFactory, email=email, password=password
    )
    assert not isinstance(user, Sequence)
    response = await client.post(
        "/users/login/", json={"email": user.email, "password": password}
    )
    assert response.status_code == status.HTTP_200_OK


async def test_login_with_wrong_password(
    client: AsyncClient, factory: data_factory.FactoryCallback, faker: Faker
):
    email = faker.email()
    await factory(data_factory.UserFactory, email=email)
    response = await client.post(
        "/users/login/",
        json={"email": email, "password": faker.password()},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_logout(
    client: AsyncClient, factory: data_factory.FactoryCallback, faker: Faker
):
    password = faker.password()
    email = faker.email()
    user = await factory(
        data_factory.UserFactory, email=email, password=password
    )
    assert not isinstance(user, Sequence)
    response = await client.post(
        "/users/login/", json={"email": user.email, "password": password}
    )
    assert response.status_code == status.HTTP_200_OK
    response = await client.post("/users/logout/")
    assert response.status_code == status.HTTP_200_OK
    response = await client.get("/users/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
