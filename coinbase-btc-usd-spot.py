import os
import requests
from datetime import datetime, timedelta
from csv import writer, DictWriter


##############################
## TIMESERIES
##############################

HOURS = 24
DIRECTORY = "timeseries"


class Time:
    def __init__(self):
        self.start = datetime.utcnow() - timedelta(days=1)
        self.format = "%Y-%m-%dT%H:%M:%S.%f"
        self.hours = self._get_hours()

    def _get_hours(self):
        """Get 24 hours incrementally from start time."""

        hours = [None] * (HOURS + 1)
        for hour in reversed(range(HOURS + 1)):
            curr_hour = self.start + timedelta(hours=hour)
            hours[hour] = curr_hour

        return hours

    def format_iso_to_datetime(iso_date):
        format = "%Y-%m-%dT%H:%M:%S.%f"
        if len(iso_date) > 26:
            iso_date = iso_date[:26]

        return datetime.strptime(iso_date, format)


class Files:
    def __init__(self, hours):
        self.paths = self._create_files(hours)

    def _create_files(self, hours):
        """Create files in specified directory.
        - Create specified directory if one does not exist.
        - The 'files' list holds file paths with index as the hour."""

        curr_path = os.path.dirname(__file__)
        file_paths = [None] * (HOURS + 1)  # index: hour, value: file path
        file_datetime_format = "%Y-%m-%d_T%H:%M"

        # Create directory if one doesn't exist.
        dir_path = os.path.join(curr_path, "timeseries")
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        for i in range(HOURS + 1):
            file_name = f"hour-{str(i).zfill(2)}_{datetime.strftime(hours[i], file_datetime_format)}.csv"
            file_path = os.path.join(curr_path, DIRECTORY, file_name)
            file_paths[i] = file_path

            with open(file_path, "w") as csv_file:
                w = writer(csv_file)

        return file_paths

    def write(self, data, fields):
        """Write parsed data to relevant files"""
        for hour, file in enumerate(self.paths):
            with open(file, "w") as csv_file:
                w = DictWriter(csv_file, fieldnames=fields)
                w.writeheader()
                w.writerows(data[hour])


class API:
    def __init__(self, start_time, hours):
        """Initialize API class and get request to seed data.
        - 'self.data' object holds trades indexed by the hour.
          { hour: [trades] }"""

        self.data = {hour: [] for hour in range(HOURS + 1)}
        self.fields = None
        self._get_data(start_time, hours)

    def _get_data(self, start_time, hours):
        """Send GET request to fetch API data.
        - Parse data by hour into 'self.data' object."""

        BASE_URL = "https://community-api.coinmetrics.io/v4/timeseries/market-trades"
        MARKETS = "coinbase-btc-usd-spot"
        PAGE_SIZE = 10000
        NEXT_URL = "next_page_url"

        # Get initial (first page) response/data.
        initial_response = requests.get(
            f"{BASE_URL}?markets={MARKETS}&start_time={start_time.isoformat()}&page_size={PAGE_SIZE}"
        )
        response_status = initial_response.status_code
        print("~ INTIAL RESPONSE STATUS:", response_status)
        response_json = initial_response.json()

        first_page = response_json.get("data")
        if first_page:
            self.fields = first_page[0].keys()
            self._parse_page(first_page, hours)

        # Get all next pages response/data.
        next_page_url = response_json.get(NEXT_URL)
        while next_page_url:
            next_response = requests.get(next_page_url)
            print("~ NEXT PAGE RESPONSE STATUS:", next_response.status_code)
            next_json = next_response.json()

            next_page = next_json.get("data")
            if next_page:
                self._parse_page(next_page, hours)

            next_page_url = next_json.get(NEXT_URL)

    def _parse_page(self, page_data, hours):
        """Parses page data into 'self.data' dictionary, indexed by hour
        - { hour: [trades] }"""

        for trade in page_data:
            trade_time = Time.format_iso_to_datetime(trade["time"])
            hour = self._get_hour(trade_time, hours)
            self.data[hour].append(trade)

    def _get_hour(self, trade_time, hours):
        for i in range(HOURS - 1):
            if hours[i] <= trade_time < hours[i + 1]:
                return i

        return HOURS - 1


class Main:
    def __init__(self):
        self._run()

    def _run(self):
        time = Time()
        files = Files(time.hours)
        api = API(time.start, time.hours)

        files.write(api.data, api.fields)

        for hour in api.data:
            print("~ hour:", str(hour).zfill(2), "trades:", len(api.data[hour]))


if __name__ == "__main__":
    main = Main()
