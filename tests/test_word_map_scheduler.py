from datetime import datetime

from server import _word_map_daily_rebuild_settings, _word_map_should_run_daily_rebuild


def test_word_map_daily_rebuild_settings_require_word_map_enabled():
    disabled = _word_map_daily_rebuild_settings({"word_map": {"enabled": False}})
    enabled = _word_map_daily_rebuild_settings({"word_map": {"enabled": True}})

    assert disabled["enabled"] is False
    assert enabled["enabled"] is True
    assert enabled["hour"] == 4
    assert enabled["minute"] == 30
    assert enabled["include_archive"] is False
    assert enabled["check_interval_seconds"] == 15 * 60


def test_word_map_daily_rebuild_runs_once_after_configured_time():
    settings = _word_map_daily_rebuild_settings(
        {
            "word_map": {
                "enabled": True,
                "daily_rebuild_hour": 4,
                "daily_rebuild_minute": 30,
            }
        }
    )

    before = datetime(2026, 6, 28, 4, 29)
    due = datetime(2026, 6, 28, 4, 30)
    later = datetime(2026, 6, 28, 5, 0)

    assert not _word_map_should_run_daily_rebuild(before, "", settings)
    assert _word_map_should_run_daily_rebuild(due, "", settings)
    assert not _word_map_should_run_daily_rebuild(later, "2026-06-28", settings)
    assert _word_map_should_run_daily_rebuild(later, "2026-06-27", settings)
