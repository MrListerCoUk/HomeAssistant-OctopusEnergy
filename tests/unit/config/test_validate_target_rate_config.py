import pytest

from homeassistant.util.dt import (as_utc, parse_datetime)
from custom_components.octopus_energy.config.target_rates import validate_target_rate_config
from custom_components.octopus_energy.const import CONFIG_TARGET_END_TIME, CONFIG_TARGET_HOURS, CONFIG_TARGET_MPAN, CONFIG_TARGET_NAME, CONFIG_TARGET_OFFSET, CONFIG_TARGET_START_TIME

now = as_utc(parse_datetime("2023-08-20T10:00:00Z"))
mpan = "selected-mpan"

def get_account_info(tariff_code: str = "E-1R-SUPER-GREEN-24M-21-07-30-C", is_active_agreement = True):
  return {
    "electricity_meter_points": [
      {
        "mpan": mpan,
        "agreements": [
          {
            "start": "2023-08-01T00:00:00+01:00" if is_active_agreement else "2023-01-01T00:00:00+01:00",
            "end": "2023-09-01T00:00:00+01:00" if is_active_agreement else "2023-02-01T00:00:00+01:00",
            "tariff_code": tariff_code,
            "product": "SUPER-GREEN-24M-21-07-30"
          }
        ]
      }
    ]
  }

@pytest.mark.asyncio
@pytest.mark.parametrize("name",[
  (""),
  ("Test"),
  ("test@"),
])
async def test_when_config_has_invalid_name_then_errors_returned(name):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: name,
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: "00:00",
    CONFIG_TARGET_END_TIME: "00:00",
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_NAME in errors
  assert errors[CONFIG_TARGET_NAME] == "invalid_target_name"
  
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("hours",[
  (""),
  ("-1.0"),
  ("s"),
  ("1.01"),
  ("1.49"),
  ("1.51"),
  ("1.99"),
])
async def test_when_config_has_invalid_hours_then_errors_returned(hours):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: hours,
    CONFIG_TARGET_START_TIME: "00:00",
    CONFIG_TARGET_END_TIME: "00:00",
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_HOURS in errors
  assert errors[CONFIG_TARGET_HOURS] == "invalid_target_hours"

  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("start_time",[
  (""),
  ("s"),
  ("24:00"),
  ("-0:01"),
  ("00:000"),
  ("00:60"),
])
async def test_when_config_has_invalid_start_time_then_errors_returned(start_time):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: start_time,
    CONFIG_TARGET_END_TIME: "00:00",
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_START_TIME in errors
  assert errors[CONFIG_TARGET_START_TIME] == "invalid_target_time"
  
  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("end_time",[
  (""),
  ("s"),
  ("24:00"),
  ("-0:01"),
  ("00:000"),
  ("00:60"),
])
async def test_when_config_has_invalid_end_time_then_errors_returned(end_time):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: "00:00",
    CONFIG_TARGET_END_TIME: end_time,
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_END_TIME in errors
  assert errors[CONFIG_TARGET_END_TIME] == "invalid_target_time"
  
  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("offset",[
  (""),
  ("s"),
  ("00"),
  ("-00"),
  ("00:00"),
  ("-00:00"),
  ("24:00:00"),
  ("-24:00:00"),
  ("00:60:00"),
  ("-00:60:00"),
  ("00:00:60"),
  ("-00:00:60"),
])
async def test_when_config_has_invalid_end_time_then_errors_returned(offset):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: "00:00",
    CONFIG_TARGET_END_TIME: "00:00",
    CONFIG_TARGET_OFFSET: offset,
  }
  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_OFFSET in errors
  assert errors[CONFIG_TARGET_OFFSET] == "invalid_offset"
  
  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("start_time,end_time",[
  ("01:00","02:00"),
  ("23:00","00:00"),
])
async def test_when_hours_exceed_selected_time_frame_then_errors_returned(start_time, end_time):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: start_time,
    CONFIG_TARGET_END_TIME: end_time,
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_HOURS in errors
  assert errors[CONFIG_TARGET_HOURS] == "invalid_hours_time_frame"

  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
async def test_when_mpan_not_found_then_errors_returned():
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: "00:00",
    CONFIG_TARGET_END_TIME: "00:00",
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info(is_active_agreement=False)

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_MPAN in errors
  assert errors[CONFIG_TARGET_MPAN] == "invalid_mpan"

  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("start_time,end_time",[
  ("00:00","00:00"),
  ("15:59","15:59"),
  ("15:59","23:01"),
])
async def test_when_select_mpan_agile_tariff_and_invalid_hours_picked_not_found_then_errors_returned(start_time, end_time):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
    CONFIG_TARGET_START_TIME: start_time,
    CONFIG_TARGET_END_TIME: end_time,
    CONFIG_TARGET_OFFSET: "-00:00:00",
  }
  account_info = get_account_info("E-1R-AGILE-FLEX-22-11-25-B")

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_END_TIME in errors
  assert errors[CONFIG_TARGET_END_TIME] == "invalid_end_time_agile"

  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("start_time,end_time,offset",[
  ("00:00","00:00","00:00:00"),
  (None, None, None),
])
async def test_when_config_is_valid_and_not_agile_then_no_errors_returned(start_time, end_time, offset):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
  }

  if start_time is not None:
    data[CONFIG_TARGET_START_TIME] = start_time

  if end_time is not None:
    data[CONFIG_TARGET_END_TIME] = end_time
  
  if offset is not None:
    data[CONFIG_TARGET_OFFSET] = offset

  account_info = get_account_info()

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors

@pytest.mark.asyncio
@pytest.mark.parametrize("start_time,end_time,offset",[
  ("00:00","23:00","00:00:00"),
  ("00:00","16:00","00:00:00"),
  ("23:00","16:00","00:00:00"),
  ("16:00","16:00","00:00:00"),
  ("16:00","00:00","00:00:00"),
  (None, "23:00", None),
  ("16:00", None, None),
  ("10:00","23:00","00:00:00"),
  ("16:30","23:30","00:00:00"),
  ("17:00","14:00","00:00:00"),
])
async def test_when_config_is_valid_and_agile_then_no_errors_returned(start_time, end_time, offset):
  # Arrange
  data = {
    CONFIG_TARGET_NAME: "test",
    CONFIG_TARGET_MPAN: mpan,
    CONFIG_TARGET_HOURS: "1.5",
  }

  if start_time is not None:
    data[CONFIG_TARGET_START_TIME] = start_time

  if end_time is not None:
    data[CONFIG_TARGET_END_TIME] = end_time
  
  if offset is not None:
    data[CONFIG_TARGET_OFFSET] = offset

  account_info = get_account_info("E-1R-AGILE-FLEX-22-11-25-B")

  # Act
  errors = validate_target_rate_config(data, account_info, now)

  # Assert
  assert CONFIG_TARGET_NAME not in errors
  assert CONFIG_TARGET_MPAN not in errors
  assert CONFIG_TARGET_HOURS not in errors
  assert CONFIG_TARGET_START_TIME not in errors
  assert CONFIG_TARGET_END_TIME not in errors
  assert CONFIG_TARGET_OFFSET not in errors