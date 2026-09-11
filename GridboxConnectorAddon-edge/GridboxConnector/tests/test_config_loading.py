import importlib.util
from pathlib import Path


def _load_addon_main():
    main_path = Path(__file__).parents[1] / "__main__.py"
    spec = importlib.util.spec_from_file_location("addon_main_for_test", main_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_load_gridbox_config_from_connector_package():
    config = _load_addon_main().load_gridbox_config()

    assert config["login"]["audience"] == "https://api.gridx.de"
