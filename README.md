# About 
In case you need the count of EU member states for each year between
1952 and 2021, this is what the csv table in this repository provides.

The yearly counts are adjusted for the fact that some accessions did
not happen at the beginning of the year. For example, the 2004 Eastern
enlargement happened at first of May 2004, and the EU was not founded
on first of January either. As a result, in 2004, the EU had 21.7
member states -- 15 before and 25 after the first Eastern
enlargement; and it had 2.7 members in the year of its inception.

Lap years are also taken into account. Brexit is included.

# Variables
- year (1952 until 2021)
- new_member_count (count of new members in the given year)
- membership (count of members in the given year)
- accession_date (date of EU enlargement)
- remaining_accession_year (duration of the remaining enlargement year
  in days)
- year_length (length of the year taking into account lap years)
- accession_adjustment (remainder of the accession year in days,
  divided by length of the year) 
- membership_adjusted: count of EU member states adjusted for the
  length of the remaining year
  
# Files
- membership_adjusted.csv : dataset
- EU-membership-adjustments.py : python script used to calculate the
  dataset based on the source below
- README.md : this file

# Sources and Credits
The accession dates are taken from Josh Fjelstul's useful EU member
state [dataset](https://github.com/jfjelstul/eums/tree/master).
