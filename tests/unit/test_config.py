from semiconductor_rag.config import Settings


def test_settings_defaults():
    config = Settings()
    assert config.environment == "dev"
    assert config.log_level == "INFO"
