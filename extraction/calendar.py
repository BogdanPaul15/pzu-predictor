from datetime import date

import holidays
import pandas as pd

from extraction.common import RAW_DIR, date_arg_parser

OUT_PATH = RAW_DIR / "calendar" / "holidays.csv"


def build(start: date, end: date) -> pd.DataFrame:
    years = range(start.year, end.year + 1)
    rows = [
        {"date": d, "name": name}
        for d, name in sorted(holidays.country_holidays("RO", years=years).items())
        if start <= d <= end
    ]
    return pd.DataFrame(rows)


def load() -> pd.DataFrame:
    return pd.read_csv(OUT_PATH, parse_dates=["date"])


def is_holiday(dates: pd.Series) -> pd.Series:
    days = set(load()["date"].dt.date)
    return pd.to_datetime(dates).dt.date.isin(days)


def main():
    p = date_arg_parser(__doc__.splitlines()[0], default_end=date(date.today().year, 12, 31))
    args = p.parse_args()
    df = build(args.start, args.end)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"{len(df)} holidays written to {OUT_PATH}")


if __name__ == "__main__":
    main()
