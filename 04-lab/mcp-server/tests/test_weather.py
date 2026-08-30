import os
import unittest
from unittest.mock import AsyncMock, patch

import weather


class WeatherToolsTests(unittest.IsolatedAsyncioTestCase):
    async def test_current_weather_reports_missing_api_key(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            result = await weather.get_current_weather("Hanoi")

        self.assertIn("WeatherAPI key not configured", result)

    async def test_forecast_clamps_days_to_free_tier_range(self) -> None:
        response = {
            "location": {"name": "Hanoi", "region": "", "country": "Vietnam"},
            "forecast": {"forecastday": []},
        }
        request = AsyncMock(return_value=response)

        with patch.object(weather, "make_weather_request", request):
            await weather.get_forecast("Hanoi", days=0)
            request.assert_awaited_once_with(
                "forecast.json",
                {"q": "Hanoi", "days": "1", "aqi": "no", "alerts": "no"},
            )

    async def test_health_check_is_available_without_api_key(self) -> None:
        result = await weather.health_check()

        self.assertIn("running", result)


if __name__ == "__main__":
    unittest.main()
