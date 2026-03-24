import anyio

from salmon.common import UploadFiles
from salmon.trackers.base import BaseGazelleApi
from salmon.trackers.ops import OpsApi


def test_ops_set_split_choice_marks_prompt_as_handled() -> None:
    tracker = OpsApi()

    tracker.set_split_choice(True)

    assert tracker._use_split is True
    assert tracker._split_prompted is True


def test_ops_split_prompt_ignores_guest_only_second_artist(monkeypatch) -> None:
    tracker = OpsApi()
    confirm_called = False

    def fake_confirm(*_args, **_kwargs):
        nonlocal confirm_called
        confirm_called = True
        return False

    async def fake_upload(self, data, files):
        return 123, 456

    monkeypatch.setattr("salmon.trackers.ops.click.confirm", fake_confirm)
    monkeypatch.setattr(BaseGazelleApi, "upload", fake_upload)

    result = anyio.run(
        tracker.upload,
        {
            "releasetype": tracker.release_types["Single"],
            "artists[]": ["Anna Zak", "Itay Galo"],
            "importance[]": [1, 2],
        },
        UploadFiles(torrent_data=b"torrent"),
    )

    assert result == (123, 456)
    assert confirm_called is False
