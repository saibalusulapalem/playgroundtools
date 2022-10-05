from ..playground import metadata


class TestMetadata:
    """Verifies whether the package metadata is correct."""

    def test_get_metadata(self):
        meta = metadata.get_metadata()
        assert meta == {
            "Name": "playgroundtools",
            "Author": "saibalusulapalem",
            "Summary": (
                "A command-line interface for managing playground projects."
            ),
            "Version": "0.7.0",
            "License": "MIT License",
        }
