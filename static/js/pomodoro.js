// Value store

var transaction;

$(document).ready(function () {

 	// Global variables
	
	var pomodoro = 25, currentTime = Date.parse(new Date()), deadline, timeInterval, breakTime = 5, longBreakTime = 15, i = 0, reward = 5

  	// Clock setup

	var clock = document.getElementById("clock-timer");
	var minutesSpan = clock.querySelector(".minutes");
	var secondsSpan = clock.querySelector(".seconds");

	minutesSpan.innerHTML = ("0" + pomodoro).slice(-2);
	secondsSpan.innerHTML = "00";

	// Calculates the time remaining

	function getTimeLeft (end) {
		var total = Date.parse(end) - Date.parse(new Date());
		var seconds = Math.floor((total/1000) % 60);
		var minutes = Math.floor((total/1000/60) % 60);

		return {
			"total": total,
			"minutes": minutes,
			"seconds": seconds
		};
	}

	// Initializes the timer

		function startClock () {
		timeInterval = setInterval(function () {
			var t = getTimeLeft(deadline);
			minutesSpan.innerHTML = ("0" + t.minutes).slice(-2);
			secondsSpan.innerHTML = ("0" + t.seconds).slice(-2);
			if (t.total <= 0) {
        document.getElementById('coin-sound').play();
				clearInterval(timeInterval);

        if (i === 7) {
          transaction = reward;
          update_coins();
          $(".reset, .start-pomodoro").addClass('hidden');
          $(".start-break2").removeClass('hidden');
        }

				else if ((i % 2) === 1) {
          transaction = reward;
          update_coins();
				  $(".reset, .start-pomodoro").addClass('hidden');
          $(".start-break1").removeClass('hidden');
				}

				else {
          $(".start-pomodoro").removeClass('hidden');
				}
			}
		}, 1000);
	}

	// Functions for pomodoro, breaks and reset

	function startPomodoro () {
		minutesSpan.innerHTML = ("0" + pomodoro).slice(-2);
		secondsSpan.innerHTML = "00";
		$(".start-pomodoro, .start-break1, .start-break2").addClass('hidden');
		$(".reset").removeClass('hidden');
		deadline = new Date(Date.parse(new Date()) + (pomodoro * 60 * 1000));
		i += 1;
		startClock();
		$(".start-break1, .start-break2").removeClass('disabled');
		$(".start-break1, .start-break2").prop("disabled", false);
	}

	function startBreak () {
		minutesSpan.innerHTML = ("0" + breakTime).slice(-2);
		secondsSpan.innerHTML = "00";
		$(".start-break1").addClass('disabled');
		$(".start-break1").prop("disabled", true);
		deadline = new Date(Date.parse(new Date()) + (breakTime * 60 * 1000)); //Set deadline
		i += 1;
		startClock();
	}

	function startLongBreak () {
		minutesSpan.innerHTML = ("0" + longBreakTime).slice(-2);
		secondsSpan.innerHTML = "00";
		$(".start-break2").addClass('disabled');
		$(".start-break2").prop("disabled", true);
		deadline = new Date(Date.parse(new Date()) + (longBreakTime * 60 * 1000)); //Set deadline
		i = 0;
		startClock();
	}

	function resetClock () {
		$(".btn-count").prop("disabled", false);
		$("body").css('background-color', '#F1C40F');
		$(".start-pomodoro").removeClass('hidden');
		$(".reset").addClass('hidden');
		$(".minutes-count").html(pomodoro);
		$("title").html("Pomodoro")
		clearInterval(timeInterval);
		minutesSpan.innerHTML = ("0" + pomodoro).slice(-2);
		secondsSpan.innerHTML = "00";
		i -= 1;
	}

	// Start Pomodoro

	$(".start-pomodoro").click(function() {
		startPomodoro();
	});

	// Start a break

	$(".start-break1").click(function () {
		startBreak();
	});

	$(".start-break2").click(function () {
		startLongBreak();
	});

	// Reset the clock

	$(".reset").click(function () {
		resetClock();
	});

});

// CSRF token

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Update coins

function update_coins() {
  $.ajax({
    method: "POST",
    url: "/coins/",
    data: {"coins": transaction},
    success: function(data) {
      $(".status" ).contents()[0].textContent = "Balance: " + data.coins;
      $("#shopmodal").modal("hide");
    }
  })
};

// Shop modal

function modalPrice(itemPrice){
  $("#broke").addClass("hidden");
  transaction = itemPrice;
  document.getElementById("price").innerHTML = itemPrice;
};

// Gets user's coin balance

function fetchCoins(coinBalance) {
if (coinBalance - transaction >= 0) {
    transaction = -transaction;
    update_coins();
    $("#shopModal").modal("hide");
  } else {
    $("#broke").removeClass("hidden");
  }
};

function getCoins(coinFn) {
  var coins;
  $.ajax({
    method: "GET",
    dataType: 'json',
    url: "/coins/",
    success: function(data) {
      coins = data.coins;
      coinFn(coins);
    }
  })
};

// Purchase an item

function buyItem() {
  getCoins(fetchCoins);
};

// Prevents modal from closing

$('#prModal').modal({
  backdrop: 'static',
  keyboard:false
});
