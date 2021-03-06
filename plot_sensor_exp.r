

rm(list=ls())
# ======================================================================
library(plotly)  
# ======================================================================


# ======================================================================
read_exp_report <- function(file_path) {
  report <- read.table(file=file_path, 
                       header = FALSE, 
                       sep = ",",
                       blank.lines.skip = TRUE, 
                       fill = TRUE)
  
  names(report) <- as.matrix(report[1, ])
  report <- report[-1, ]
  report[] <- lapply(report, function(x) type.convert(as.character(x)))
  report
}
# ======================================================================

# ======================================================================
plot_4_surfaces <- function(dataf) {
  myplot <- plot_ly(
    x = dataf$outer_loop_n,
    y = dataf$obs,
    showscale = TRUE
  ) %>%
    add_trace(
      z = log(dataf$sensor_mediation_hid_wtloc),opacity=.3,
      type = 'mesh3d',facecolor = rep("blue",1000)
    ) %>%
    add_trace(
      z = log(dataf$sensor_mediation_hid_noloc),opacity=.3,
      type = 'mesh3d',facecolor = rep("green",1000)
    ) %>%
    add_trace(
      z = log(dataf$sensor_mediation_sim_wtloc),opacity=.3,
      type = 'mesh3d',facecolor = rep("orange",1000)
    ) %>%
    add_trace(
      z = log(dataf$sensor_mediation_sim_noloc),opacity=.3,
      type = 'mesh3d',facecolor = rep("red",1000)
    )%>%
    layout(title = "",
           scene = list(xaxis = list(title = "loop instances"), 
                        yaxis = list(title = "observation"), 
                        zaxis = list(title = "time (log10)")))
  myplot 
}
# ======================================================================

# ======================================================================
plot_3_surfaces <- function(dataf) {
  myplot <- plot_ly(
    x = dataf$outer_loop_n,
    y = dataf$obs,
    showscale = TRUE
  ) %>%
    add_trace(
      z = dataf$sensor_mediation_hid_wtloc,opacity=.5,
      type = 'mesh3d',facecolor = rep("blue",1000)
    ) %>%
    add_trace(
      z = dataf$sensor_mediation_hid_noloc,opacity=.5,
      type = 'mesh3d',facecolor = rep("green",1000)
    ) %>%
    add_trace(
      z = dataf$sensor_mediation_sim_wtloc,opacity=.5,
      type = 'mesh3d',facecolor = rep("orange",1000)
    )%>%
    layout(title = "",
           scene = list(xaxis = list(title = "loop instances"), 
                        yaxis = list(title = "observation"), 
                        zaxis = list(title = "time")))
  myplot 
}
# ======================================================================

# ======================================================================
plot_2_surfaces_loc <- function(dataf) {
  myplot <- plot_ly(
    x = dataf$outer_loop_n,
    y = dataf$obs,
    showscale = TRUE
  ) %>%
    add_trace(
      z = dataf$sensor_mediation_hid_wtloc,opacity=.5,
      type = 'mesh3d',facecolor = rep("blue",1000)
    ) %>%
    add_trace(
      z = dataf$sensor_mediation_sim_wtloc,opacity=.5,
      type = 'mesh3d',facecolor = rep("orange",1000)
    )%>%
    layout(title = "",
           scene = list(xaxis = list(title = "loop instances"), 
                        yaxis = list(title = "observation"), 
                        zaxis = list(title = "time")))
  myplot 
}
# ======================================================================

# ======================================================================
plot_4_lines <- function(dataf) {
  myplot <- plot_ly(type = 'scatter', 
                    mode = 'lines') %>%
    add_trace(x = dataf$obs, 
              y=log(dataf$sensor_mediation_hid_wtloc),
              line = list(color = 'blue', width = 4, dash = 'dash'),
              name = "hiding with local analyses") %>%
    add_trace(x = dataf$obs, 
              y=log(dataf$sensor_mediation_hid_noloc), 
              line = list(color = 'green', width = 4, dash = 'dash'),
              name = "hiding without local analyses") %>%
    add_trace(x = dataf$obs, 
              y=log(dataf$sensor_mediation_sim_wtloc), 
              line = list(color = 'orange', width = 4, dash = 'dot'),
              name = "simulation with local analyses") %>%
    add_trace(x = dataf$obs, 
              y=log(dataf$sensor_mediation_sim_noloc), 
              line = list(color = 'red', width = 4, dash = 'dot'),
              name = "simulation without local analyses") %>%
    layout(title = "", 
           xaxis = list(title = "observation"), 
           yaxis = list(title = "time (log10)"))
  myplot 
}
# ======================================================================



mydata <- read_exp_report("./sensor_exp_hibou/sensor_mediation.csv")

pass_mus <- mydata[mydata$isPass == "True",]

fail_mus <- mydata[mydata$isPass == "False",]


plot_3_surfaces(pass_mus)

plot_4_surfaces(pass_mus)

plot_4_surfaces(fail_mus)

plot_2_surfaces_loc(fail_mus)


plot_4_lines(pass_mus[pass_mus$outer_loop_n == 8, ])

plot_4_lines(fail_mus[fail_mus$outer_loop_n == 8, ])
