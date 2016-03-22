$("#resultBox").hide();

$("#input").submit(function(event) {
  showStatus(1);

  $.get("https://martyn.pw/projects/steam-profile-background/api", {
      url: $("#inputURL").val()
    })
    .done(function(data) {
      showData(data.imageURL, data.gameName);
    })
    .fail(function() {
      showStatus(2);
    });
  event.preventDefault();
});

function showData(image, game) {
  // Yeah this looks messy...
  $("#resultBox").html('<div class="block"> <a href="' + image + '" target="_blank">' +
    '<img src="' + image + '" alt="Background image">' +
    '</a><span class="game-title">' + game + '</span> <a href="http://steamcommunity.com/market/search?q=' + game + ' background" target="_blank">' +
    '<input type="submit" value="Buy wallpaper" id="buyButton"/></a></div>');
  $("#resultBox").show();
}

function showStatus(status) {
  if (status == 1) {
    $("#resultBox").html('<div class="block">Loading...</div>');
  } else if (status == 2) {
    $("#resultBox").html('<div class="block warning">Invalid URL</div>');
  }
  $("#resultBox").show();
}