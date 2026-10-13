library(dplyr)
library(fpp3)
library(lubridate)
library(ggplot2)
library(stringr)
library(purrr)
library(gridExtra)

#####################################################
#  ANALYSIS OF CHECK-IN FLOW
#
# TWO DATA SOURCES: 1. CHECK-IN DESK (via tailscale SSH and ultimate command wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01)
# 2. vori sales data (by cart) <- to gauge total number of shoppers, potentially providing accuracy on # of "guests" per day
# NOTE: Vori data is limited to Sept '23

#my note to the Board written on Aug 10, 2025: 
#Still digging into July's large decline. This is what I got: we should have started open shopping in July. On the chart below, you see the weekly counts of shopping visits by shopper type. I highlighted in orange the weeks of July '25. You can see how the ghfc cohort (member-owners) fell off a cliff. visitor and deviance (a weird catch-all offset figure) fell as well but by much less... it even looks like there was a upspike in visitor on the 2nd-to-last week of July that counter-balanced the ghfc decline.
#It may have not been feasible or popular, but to maintain our cash flow, opening in July would have given us some support
#########################################################

setwd('/home/candela/pCloudDrive/pCloud Backup/mofongo-HP-EliteBook-840-G8-Notebook-PC/Documents/ghfc')

#############
# VORI DATA  #
##############
#GRAB ALL FILES IN FOLDER <- this code mostly comes from vori_sales_analysis.R
file_array <- list.files('./salesAnalysis/vori_sales_data')
compiled_df_list <- list()
#store and index all files located in ./vori_sales_data - both csv and excel
for (file in file_array) {
  file_path <- file.path('./salesAnalysis/vori_sales_data', file)  # Construct path correctly
  if (str_detect(file, "\\.csv$")) {  # Match against file name
    compiled_df_list[[length(compiled_df_list) + 1]] <- read.csv(file_path)
  } 
  else if (str_detect(file, "\\.xlsx$")) {  # Fix elif to else if
    compiled_df_list[[length(compiled_df_list) + 1]] <- read_xlsx(file_path)
  } 
  else {
    print(paste0("File ", file, " is not a CSV or XLSX file"))
  }
}


#this code, originally form 
normalize_df2 <- function(df, return_type = 'tsibble') {
  #replace Value..1. with just Value and remmove the first Value
  #ensure that the df contains an Order_Day and Value field
  if(!all(list('Order.Day','Order.ID') %in% names(df))) {
    stop("expected column names are not found in the passed DF")
  }
  #convert column headers
  names(df) <- gsub('\\.','_',names(df))
  
  # Main logic
  df |>
    mutate(date = as.Date(df$Order_Day,'%a, %b %d, %Y')) -> df.1
  
  #isolate the only columns I care about
  df.1 |>
    group_by(date) |>
    summarize(order_cnt = n_distinct(Order_ID)) -> sales.vori
  
  #output 
  sales.vori |>
    as_tsibble(index = date) -> vori.t
  
  if(!nrow(vori.t)>0){
    stop("transformed df has 0 rows")
  }
  
  if(return_type == 'df'){
    return(sales.vori)
  }
  else {
    # Return the result
    return(vori.t)
  }
}

#apply the normalize_df function to ea element of the list of dataframes
result_list <- purrr::map(compiled_df_list,normalize_df2,return_type = 'df')

#working with dataframes
combined_df <- bind_rows(result_list)

#selection criteria for dupes
combined_df |> 
  mutate(Date = date) |>
  group_by(Date) |>
  summarize(order_cnt = max(order_cnt)) -> combined_df2


#plot to visualize data thus far
combined_df2 |>
  ggplot(aes(x=Date,y=order_cnt)) +
  geom_line() +
  labs(title='Daily Count of Shoppers')
  
###################
# CHCEK IN DESK DATA 
######################
checkin <- read.csv('./check-in_desk/front_desk_logs/07012023-08082025stats.csv')
#/home/candela/pCloudDrive/pCloud Backup/mofongo-HP-EliteBook-840-G8-Notebook-PC/Documents/ghfc/check-in_desk
head(checkin)

checkin |>
  mutate(date = as.Date(date,'%Y-%m-%d')) |>
  rowwise() |>
  mutate(total_shop = sum(ghfc,trial,psfc,cbfc,visitor)) -> checkin

#check the disparity btwn checkin$total_shop and combined_df$order_cnt
merged.df <- merge(combined_df2,checkin,by.x='Date',by.y='date')
tail(merged.df)

#make an explicit 'deviance' field
merged.df |>
  mutate(deviance = total_shop-order_cnt, weekday = weekdays(Date)) -> merged.df

#trials look low; plotting
merged.df |>
  ggplot(aes(x=Date,y=trial)) +
  geom_line() +
  labs(title='trial shopping')

plt.1 <- merged.df |>
  filter(weekday != 'Sunday' & deviance < 60) |>
  ggplot(aes(x=Date,y=deviance)) +
  geom_line() +
  labs(title='non-Sunday deviance',subtitle = 'negative values = register orders > check in logs')

#isolate Sundays
plt.2 <- merged.df |>
  filter(weekday == 'Sunday') |>
  ggplot(aes(x=Date,y=deviance)) +
  geom_line() +
  labs(title='Sunday deviance')

gridExtra::grid.arrange(plt.1,plt.2,ncol=2,nrow=1)

#plot weekly shopping to discern what happened in July '25
#weeks of July '25 = week 27 - 31
band_start <- tsibble::yearweek("2025-07-01")
band_end <- tsibble::yearweek("2025-07-31")

merged.df |>
  mutate(yr_wk = tsibble::yearweek(Date)) |> 
  mutate(deviance = abs(deviance)) |>
  select(-c(weekday,cbfc,Date)) |>
  pivot_longer(cols=c(ghfc,trial,psfc,visitor,deviance),names_to=c('shopper_type'),values_to ='shopper_cnt') |>
  group_by(yr_wk,shopper_type) |>
  summarize(shopper_cnt = sum(shopper_cnt)) |>
  select(yr_wk,shopper_type,shopper_cnt) |>
  ggplot(aes(x=yr_wk,y=shopper_cnt,color=shopper_type)) +
  annotate("rect", 
           xmin = band_start, xmax = band_end, 
           ymin = -Inf, ymax = Inf, 
           alpha = 0.3, fill = "orange") +
  geom_line() +
  labs(title="Weekly shopping visits by shopper type (check-in desk)", x="year week", y ="shopper count")
