import pandas as pd

# load Josh Fjelstul's EU member state data.
ms_data = pd.read_csv("https://raw.githubusercontent.com/jfjelstul/eums/master/data-raw/member_states_raw.csv")

# raw count of membership at each accession year
membership = (ms_data
              .copy()
              .filter(["accession_year"])
              .value_counts()
              .to_frame(name="new_member_count")
              .reset_index(names=["year"])
              .sort_values(by="year")
              .reindex()
              .assign(membership = lambda x: x["new_member_count"].cumsum())
             )

# raw membership counts for each year from 1952 to 2021
membership = (membership
              .merge(pd.DataFrame({"year": [i for i in range(1952, 2022)]}),
                     how="right")
              .fillna(method="ffill")
              )   

# add variable for remainder of accession/exit year
membership = (membership
                        .merge(ms_data[["accession_year", "accession_date"]],
                               left_on="year", right_on="accession_year", how="left")
                        .drop(columns=["accession_year"])
                        .drop_duplicates()
                        .assign(accession_date = lambda x: pd.to_datetime(x["accession_date"]))
                        .assign(remaining_accession_year = lambda x: x["accession_date"] + pd.tseries.offsets.YearEnd() + pd.DateOffset(1) - x["accession_date"])
             )

# adjust membership count for accessions that did not take place at the beginning of the year
membership = (membership
              .assign(year_length = lambda x: x["year"].apply(
                  lambda x: pd.Timestamp(x, 12, 31).dayofyear))  # find the length of the year (b/c lapyears) 
              .assign(accession_adjustment = lambda x: x["remaining_accession_year"].dt.days / x["year_length"])
              .assign(membership_adjusted = lambda x:
                      x["membership"].shift(1) + x["new_member_count"] * x["accession_adjustment"])  # adjust membership for length of year
              .assign(membership_adjusted = lambda x: 
                      x["membership_adjusted"].fillna(membership["membership"]))  # propagate missing values for non-adjusted
              )

# adjust membership count for Brexit
brexit = pd.to_datetime("2020-01-31")
brexit_year_lenth = pd.Timestamp(brexit.year, 12, 31).dayofyear  # 366, lapyear
remaining_brexit_year = brexit + pd.tseries.offsets.YearEnd() + pd.DateOffset(1) - brexit  # 336 days
brexit_adjustment = remaining_brexit_year.days / brexit_year_lenth

membership.loc[membership["year"] >= 2020, "new_member_count"] = -1
membership.loc[membership["year"] == 2020, "accession_date"] = brexit
membership.loc[membership["year"] == 2020, "accession_adjustment"] = brexit_adjustment
membership.loc[membership["year"] == 2020, "membership_adjusted"] = membership.loc[membership["year"] == 2020]["new_member_count"] * \
                                            brexit_adjustment + membership.loc[membership["year"] == 2020]["membership"]
membership.loc[membership["year"] > 2020, "membership"] = 27
membership.loc[membership["year"] > 2020, "membership_adjusted"] = 27

# save to csv file
membership.to_csv("./membership_adjusted.csv", index=False)
