function increaseClicks() {
    currentClicks = parseInt($("#currentClicks").text())
    $.ajax({url: "clicks/inc_clicks", success: function(result){
        $("#currentClicks").html(result["clicks"]);
      }});
}

function decreaseClicks() {
    currentClicks = parseInt($("#currentClicks").text())
    $.ajax({url: "clicks/dec_clicks", success: function(result){
        $("#currentClicks").html(result["clicks"]);
      }});
}