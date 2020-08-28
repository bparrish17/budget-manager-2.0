_Disclaimer: My Python code is low key garbage I promise I'm better at my job :| _

# Description

I wanted to learn Python and also improve my Budget Manager project so here we are at *2.0*

Instead of having manually make all the organized folders and renaming files and what not that I normally do for each month's expenses using 1.0, I'm gonna use this to do it for me. It's all pretty hard-coded for this specific use case but maybe if I'm feeling _audacious_ later I'll make it a bit more functional. 

Structure below kind of explains what I'm trying to do. This is just to take all of my credit card, checking account, and investment transactions that I download in CSV form and
1. rename them
2. move them to the right folder
3. bring their columns and values to parity
4. write them to my google sheet which does the rest

# Structure

### File Saving

1. read from downloads by known file name
2. rename each file to proper type (amex, usaa, chase)
3. make directory in Budget folder by month
4. add 3 files to budget / month folder

### File Reading

1. Fetch 3 files from Budget folder
2. Read each file individually
3. Convert each file to expected data
   1. Convert individual column headers to sheets headers
   2. Convert individual column values to expected appearance
   3. Add values to either expenses, incomes, or investments
   4. Check for exceptions, like credit card payments doubled from checking account

### Sheets Writing

1. Read from expenses, incomes, and investments values
2. Write values to each sheet
