# the following shows a spinner while the data table is loading
# the spinner also shows when the page is initially loading,
# but not after data validation fails

library(shiny)
library(DT)
library(shinycssloaders)



ui <- fluidPage(
    shinyFeedback::useShinyFeedback(),
    #...
    withSpinner(DT::dataTableOutput("prediction_table")),
    #...
)

server <- function(input, output, session) {
    # ...
    get_prediction_data <- eventReactive(input$submit_descr, {
        # check that description is not empty
        cat("Checking description", sep="\n")
        descr_not_blank = nchar(description$text) > 0
        cat(descr_not_blank, sep="\n")
        shinyFeedback::feedbackDanger("description", !descr_not_blank, "Please enter a description!")
        req(descr_not_blank, cancelOutput = TRUE)
        
        ## this doesn't work
        # waiter::Waiter$new(id = "prediction_table", html = waiter::spin_rotate())$show()
        # Sys.sleep(2)
        
        #...
        data
    })


    output$prediction_table <- renderDataTable({
        ## this works, but notification appears in lower right corner & is easy to miss
        # note <- showNotification("Retrieving predictions...", duration = NULL, closeButton = FALSE)
        # on.exit(removeNotification(note), add = TRUE)
        
        ## this works, but entire page is replaced by an image of a spinner and is a little disorienting
        # w <- waiter::Waiter$new()
        # w$show()
        # on.exit(w$hide())
    
        DT::datatable(get_prediction_data(),
        #...
        )
    })

    # ...
}