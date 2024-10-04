


# `conditionalPanel` vs `renderUI` (or `uiOutput`?)
conditionalPanel is client-side. it creates a JavaScript expression which "listens" for a specific condition, e.g. whether an input is TRUE or FALSE. Nothing needs to happen on the server-side.

renderUI() in contrast is very flexible. Of course, it can mimic the behavior of conditionalPanel but is also capable to output basically anything by creating different HTML (UI) code.

conditionalPanel should almost always be faster. 


ex code:
```R
ui  <- fluidPage(
    ...
    # With the conditionalPanel, the condition is a JavaScript
    # expression. In these expressions, input values like
    # input$n are accessed with dots, as in input.n
    conditionalPanel("input.n >= 50",
      plotOutput("scatterPlot", height = 300)
    )
)
```


# reactive's vs `req`

both are used to handle dependencies and ensure certain conditions are met before proceeding.

- reactives
    - automatically update when their inputs change

- `req`
    - more used to validate inputs or conditions


# `reactlog`
https://mastering-shiny.org/reactive-graph.html?q=reactlog#the-reactlog-package



# `eventReactive` vs `observeEvent`

## `eventReactive`
- a way to use input values without taking a reactive dependency on them
- 2 args:
    1. what to take a dependency on ("eventExpr")
    2. what to compute ("handlerExpr")

- archetypical example:
```R
# server function
x1 <- eventReactive(
    input$submit_button, {
    funcion_to_compute_value_of_x1(input$n1)
})

output$plot <- renderPlot({
    plotting_func(x1(), ...)
})
```

^ here, x1 only get evaluated and plot only gets render once the button is clicked, not when the value for n1 gets updated.

## `observeEvent`
- similar to eventReactive...
- 2 args:
    1. what to take a dependency on ("eventExpr")
    2. code to run ("handlerExpr")
- differs in that...
    - result not assigned to a variable
    - can't refer to it from other reactive consumers
- closely related to outputs
    - outputs have special side effects of updating HTML

## both:
- behind the scenes they are using `isolate()` to access the value of a reactive without taking a dependency on it
- `observeEvent` = observe({x; isolate(y)})
- `eventReactive` = reactive({x; isolate(y)})



# hiding elements until X happens

ex: show text only after actionButton clicked
with data validation

`shinyjs` works nicely here, with its `hidden` and `show` functions:

```
ui <-
  fluidPage(
    shinyFeedback::useShinyFeedback(), # not required but also nice
    useShinyjs(),
    ...
    textInput("text1", ...), # note: default `value` = ""
    actionButton("submit"),
    ...
    hidden(htmlOutput("out_2")),
    ...
  )

server <- function(input, output) {
    observeEvent(input$submit), {
        if (input$text1 == "" ) {
            shinyFeedback::showFeedbackDanger("text1", "Must enter text!")
            return()
        } else {
            shinyFeedback::hideFeedback("text1")
        }
    }
    # alt: can use: `validate(need(...))` but this will fail silently
}
```

**NOTE**: `hidden` doesn't work on some elements, such as `DT::dataTableOutput()`
- best(?)/an option here is to repeat data validation inside code that generates data table