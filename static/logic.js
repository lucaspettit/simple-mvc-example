
const activation_dropdown_id = '#selActivation'

// Attach the on-change-handler for the activation dropdown
d3.selectAll(activation_dropdown_id).on('change', updatePlot);

function updatePlot() {
  /*
   * This function updates the lineplot's data & title
   * with the values that are currently selected in the
   * #selActivation dropdown list.
   */

  // Get the selected dropdown's "value" attribute
  var activation = d3.select(activation_dropdown_id).property('value');
  // Get the selected dropdown's inner text. Note we add "option:checked" this time.
  var name = d3.select(`${activation_dropdown_id} option:checked`).text();

  // Build a href to get the activation data selected
  var dataUrl = `/data/${activation}?from=-5&to=5`;
  console.log(dataUrl);

  // Make a query to get the data, then update the graph 
  // with whatever data get's returned.
  d3.json(dataUrl).then(data => {
    let layout = {
      title: `This is a ${name} activation curve`
    };
    
    Plotly.newPlot("plot", [data], layout);
  });
}

// initialize graph
updatePlot();
