import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app  # Импорт вашего FastAPI приложения

from app.api.utils.db import get_db
from db.base_class import Base

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц для тестов
Base.metadata.create_all(bind=engine)

# Клиент для тестирования FastAPI
client = TestClient(app)


# Фикстура для базы данных
@pytest.fixture(scope="function")
def db_session():
    """Создаём новую сессию для каждого теста."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Подмена зависимости get_db для использования тестовой базы данных
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    """Подменяем зависимость get_db тестовой сессией."""

    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override


# Тест создания продукта
def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test description", "price": 100.0, "count_in_storage": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 100.0
    assert data["count_in_storage"] == 10


# Тест получения списка товаров
def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# Тест получения одного товара
def test_get_single_product():
    response = client.get("/products/1/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


# Тест обновления товара
def test_update_product():
    response = client.put(
        "/products/1/",
        json={"name": "Updated Product", "description": "Updated description", "price": 120.0, "count_in_storage": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 120.0


# Тест удаления товара
def test_delete_product():
    response = client.delete("/products/1/")
    assert response.status_code == 200


# Тест создания заказа
def test_create_order():
    response = client.post(
        "/orders/",
        json={"items": [{"id_product": 1, "count_in_order": 2}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["order_items"]) == 1


# Тест получения списка заказов
def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# Тест обновления статуса заказа
def test_patch_order_status():
    response = client.patch("/orders/1/status/", json={"status": "DELIVERED"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DELIVERED"
