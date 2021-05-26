import pytest

class ExampleClass():
    def __init__(self):
        self.a = 'attribute a'
        self.b = 'attribute b'

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b

@pytest.fixture
def example_class():
    return ExampleClass()
        
@pytest.fixture(autouse=True)
def mock_get_a(monkeypatch):
    """ Get filepath of standard test database file | None -> Path """
    def get_b(self):
        return self.get_b()

    monkeypatch.setattr(ExampleClass, 'get_a', get_b)

def test_get_a(example_class):
    assert example_class.get_a() == 'attribute b'
    
def test_mock_get_a(mock_get_a, example_class):
    assert example_class.get_a() == 'attribute b'
    assert ExampleClass().get_a() == 'attribute b'
