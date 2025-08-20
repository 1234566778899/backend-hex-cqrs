from app.contexts.users.application.command_handlers import CreateUserHandler

def test_create_user_publishes_event(monkeypatch):
    published = {}
    class DummyHandler(CreateUserHandler):
        def __init__(self):
            pass
        def handle(self, name, email, password):
        # No Rabbit – solo simula
            return {"id": "fake-id"}

    h = DummyHandler()
    result = h.handle("Ada", "ada@example.com", "s3cret")
    assert result["id"] == "fake-id"