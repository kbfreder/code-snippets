# most of these don't work!!

library(shiny)
library(shinyjs)
library(bslib)
library(bsicons)
library(shinyBS)


# Define UI
ui <- fluidPage(
  actionButton(
    "btn_tip",
    "Focus/hover here for tooltip"
  ) |>
    tooltip("Tooltip message"),

    ## THIS IS THE ONLY ONE I GOT TO WORK
    ## leverages bootstrap
  checkboxInput("show_example",
                label=(
                  span(
                    "Show Example Output",
                    `data-toggle` = "tooltip",
                    `data-placement` = "right",
                    title = "without submitting a description",
                    icon("question-circle") #"info-circle")
                  )),
                value = FALSE
  ),

  
  bsTooltip("show_example", "without submitting a description",
            placement = "right", trigger = "hover",
            options = list(container = "body")
            ),

  card(
    card_header(
      "Penguin body mass",
      tooltip(
        bsicons::bs_icon("question-circle"),
        "Mass measured in grams.",
        placement = "right"
      ),
    ),
    "Card content goes here",
    card_footer(
      "source: publication",
      popover(
        a("Learn more", href = "#"),
        markdown(
          "Originally published in: Gorman KB, Williams TD, Fraser WR (2014) Ecological Sexual Dimorphism and Environmental Variability within a Community of Antarctic Penguins (Genus Pygoscelis). PLoS ONE 9(3): e90081. [doi:10.1371/journal.pone.0090081](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081)"
        )
      )
    )
  ),... =

  br(), br(),

  span(
    `data-toggle` = "tooltip",
    `data-placement` = "auto",
    title = "I am a tooltip!",
    icon("info-circle",
         style="font-size: 150%;")
  )
)



# Define server logic
server <- function(input, output, session) {

}

# Run the app
shinyApp(ui = ui, server = server)



# ==========================
# ACCORDIONS

# also doesn't work
library(shiny)
library(bslib)
              accordion(
                accordion_panel(
                  "Options",
                  checkboxInput("show_example",
                                  label = span(
                                      "Show Example Output",
                                      `data-toggle` = "tooltip",
                                      `data-placement` = "auto",
                                      title = "without submitting a description",
                                      icon("question-circle")
                                      ),
                                  value = FALSE),
                  checkboxInput("demo_mode", 
                                label = span(
                                  "Run in Demo Mode",
                                  `data-toggle` = "tooltip",
                                  `data-placement` = "right",
                                  title = "call model but indicate that description is not from an actual deviation",
                                  icon("question-circle")
                                ),
                                value = FALSE),
                  )
                )
              )