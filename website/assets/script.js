$("#input").submit(function(event) {
  $("#resultBox").html('<div class="block">Loading...</div>');

  $.ajax({
    url: 'https://martyn.pw/projects/steam-profile-background/api',
    type: 'GET',
    data: {
      url: "http://steamcommunity.com/id/" + $("#inputURL").val()
    },
    success: function(data) {
      showData(data.imageURL, data.gameName);
    },
    error: function(err) {
      showStatus(err.responseJSON);
    }
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

function showStatus(data) {
  if (data.error == "INVALID_URL") {
    $("#resultBox").html('<div class="block warning">Profile URL is invalid</div>');
  } else if (data.error == "RATELIMIT_EXCEEDED") {
    toggleSearch(false);
    var duration = 59;
    var timer = setInterval(function() {
      $('#seconds').text(duration);

      if (duration <= 0) {
        clearInterval(timer);
        toggleSearch(true);
      } else {
        duration -= 1;
      }
    }, 1000);
    $("#resultBox").html('<div class="block warning">Limit exceeded, please wait <span id="seconds">60</span> seconds</div>');
  }
  $("#resultBox").show();
}

function toggleSearch(toggle) {
  if (toggle) {
    $("#resultBox").fadeOut();
    $("input").removeClass("disabled");
    $("input").prop('disabled', false);
  } else {
    $("input").addClass("disabled");
    $("input").prop('disabled', true);
  }
}