function increaseClicks() {
    currentClicks = parseInt($("#currentClicks").text())
    $.ajax({url: "inc_clicks", success: function(result){
        $("#currentClicks").html(result["clicks"]);
      }});
}

function decreaseClicks() {
    currentClicks = parseInt($("#currentClicks").text())
    $.ajax({url: "dec_clicks", success: function(result){
        $("#currentClicks").html(result["clicks"]);
      }});
}