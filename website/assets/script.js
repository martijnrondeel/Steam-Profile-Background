$("#input").submit(function(event) {
    event.preventDefault();

    // Steam profile url's are 2 chars or more
    if ($("#inputURL").val().length < 2) {
        $("#resultBox").html('<div class="block warning">Please fill something in</div>');
        return;
    }

    $("#resultBox").html('<div class="block">Loading...</div>');
    toggleSearch(false);

    $.ajax({
        url: '/projects/steam-profile-background/api',
        type: 'GET',
        data: {
            url: "http://steamcommunity.com/id/" + $("#inputURL").val()
        },
        success: function(data) {
            toggleSearch(true);
            showData(data.imageURL, data.gameName);
        },
        error: function(err) {
            toggleSearch(true);
            showStatus(err.responseJSON);
        }
    });
});

function showData(image, game) {
    // Yeah this looks messy...
    $("#resultBox").html('<div class="block"> <a href="' + image + '" target="_blank" rel="noopener">' +
        '<img src="' + image + '" alt="Background image">' +
        '</a><span class="game-title">' + game + '</span> <a href="http://steamcommunity.com/market/search?q=' + game + ' background" target="_blank" rel="noopener">' +
        '<input type="submit" value="Buy wallpaper" id="buyButton"/></a></div>');
    $("#resultBox").show();
}

function showStatus(data) {
    switch (data.error) {
        case "INVALID_URL":
            $("#resultBox").html('<div class="block warning">ID is invalid</div>');
            break;
        case "RATELIMIT_EXCEEDED":
            toggleSearch(false);
            var duration = 59;
            var timer = setInterval(function() {
                $('#seconds').text(duration);

                if (duration <= 0) {
                    clearInterval(timer);
                    toggleSearch(true);
                    $("#resultBox").fadeOut(); // remove the warning
                } else {
                    duration -= 1;
                }
            }, 1000);
            $("#resultBox").html('<div class="block warning">Limit exceeded, please wait <span id="seconds">60</span> seconds</div>');
            break;
        case "NO_BACKGROUND":
            $("#resultBox").html('<div class="block warning">That profile has no background</div>');
            break;
        case "GAME_NOT_FOUND":
            $("#resultBox").html('<div class="block"> <a href="' + data.imageURL + '" target="_blank">' +
                '<img src="' + data.imageURL + '" alt="Background image"></a></div><div class="block warning">The game that belongs to this wallpaper doesn\'t exist anymore</div>');
            break;
    }
    $("#resultBox").show();
}

function toggleSearch(toggle) {
    if (toggle) {
        $("input").removeClass("disabled");
        $("input").prop('disabled', false);
    } else {
        $("input").addClass("disabled");
        $("input").prop('disabled', true);
    }
}
