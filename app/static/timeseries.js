const unzip = arr =>
  arr.reduce(
    (acc, val) => (val.forEach((v, i) => acc[i].push(v)), acc),
    Array.from({
      length: Math.max(...arr.map(x => x.length))
    }).map(x => [])
  );

// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
    String.prototype.format = function() {
      var args = arguments;
      return this.replace(/{(\d+)}/g, function(match, number) { 
        return typeof args[number] != 'undefined'
          ? args[number]
          : match
        ;
      });
    };
  }

function addTimeseries() {
    let name = window.prompt("Name of the new timeseries?").trim()
    if(name==null || name.length<1) {
        alert("Please insert a better name")
    } else {
        $.ajax({
            type: 'POST',
            url: '/timeseries/add',
            data: { 
                "name": name
            },
            success: function(result){
            if(result["code"] == 0) {
                console.log(result["result"])
                updateTimeseries()
            } else {
                window.alert(result["result"])
            }
        }});
    }
}

function addTimeseriesValue(series) {
    var val = window.prompt("New Value?").trim()
    if(val.length<1 || isNaN(val)) {
        alert("Please insert a number")
    } else {
        val = parseFloat(val)
        $.ajax({
            type: 'POST',
            url: '/timeseries/addvalue',
            data: { 
                "series": series,
                "value": val
            },
            success: function(msg){
                if(msg["code"] == 0) {
                    console.log(msg["result"])
                    updateTimeseries()
                } else {
                    alert(msg["result"]);
                }
            }
        });
    }
}

function updateTimeseries() {
    const getHTML = name => `
    <div class="row">
        <div class="col">
            <div id='chart-{0}'>
                <h4>{0}</h4>
                <button onclick='addTimeseriesValue("{0}")'>Add Value</button>
                <canvas id='chart-{0}-canvas'></canvas>
            </div>
        </div>
    </div>
        `.format(name)

    const getEmptyHTML = name => `
    <div class="row">
        <div class="col">
            <div id='chart-{0}'>
                <h4>{0}</h4>
                <button onclick='addTimeseriesValue("{0}")'>Add Value</button>
                <p>No data to show yet...</p>
            </div>
        </div>
    </div>
        `.format(name)

    $.ajax({url: "timeseries/data", success: function(result){
        $("#timeseriesContainer").html("")


        $.each(result, function(name, data) {
            if(data.length < 1) {
                $("#timeseriesContainer").append(getEmptyHTML(name))
            } else {
                $("#timeseriesContainer").append(getHTML(name))

                var labels = unzip(data)[0]
                labels = labels.map(x => new Date(x*1000))

                var dataset = unzip(data)[1]
                const tmp_chart = new Chart($("#chart-"+name+"-canvas")[0].getContext("2d"), {
                    type: "line",
                    data: {
                        labels: labels,
                        datasets: [{
                            label: name,
                            data: dataset,
                            borderColor: "#000"
                        }]
                    },
                    options: {
                        scales: {
                            x: {type: "time", time: {unit: "day", displayFormats: {day: "dd. MMM yy"}}},
                            y: {type:"linear", suggestedMin: 0}
                        }
                    }

                })
            }
        })
      }});
}

updateTimeseries()