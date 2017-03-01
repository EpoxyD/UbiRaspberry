
/*
 *  Function to play the song
 */

function play(){
    var audio = document.getElementById("audio");
    var icon = document.getElementById("play-button");

    if (audio.getAttribute("playing") == "False") {
        audio.play();
        audio.setAttribute("playing", "True");

        icon.className = "fa fa-pause";
    }
    else {
        audio.pause();
        audio.setAttribute("playing", "False");

        icon.className = "fa fa-play";
    }


}



/*
 *  Adding the sun and moon
 */


function init_svg() {
    var parentWidth = document.getElementById('day-night').offsetWidth;

    var svg = d3.select('#day-night').append('svg')
        .attr('width', parentWidth-26-26)
        .attr('height', (parentWidth-26-26)/2)
        .attr('id', "svg");

    console.log((parentWidth-26-26)/2);

    svg.append("circle")
        .style("stroke", "white")
        .style("fill", "none")
        .attr("r", svg.attr('width') * 0.4)
        .attr("cx", svg.attr('width') * 0.5)
        .attr("cy", svg.attr('height'));

    var sun = svg.append('image')
        .attr('xlink:href', 'img/sun.png')
        .attr("width", 50)
        .attr("height", 50)
        .attr("x", 0)
        .attr("y", 0)
        .attr("id", "sun");

    var moon = svg.append('image')
        .attr('xlink:href', 'img/moon.png')
        .attr("width", 50)
        .attr("height", 50)
        .attr("x", 0)
        .attr("y", 0)
        .attr("id", "moon");
}

/*
 *  Getting the sunrise and sunset times
 */

var sunrise; //Time in hours
var sunset; //Time in hours

function init_sun_moon(){
    jQuery.ajax({
        url: "https://api.darksky.net/forecast/a22f23bee010f3976f614a0460d1ccf6/50.87296604411913,4.697816732888441",
        type: "GET",
        dataType: "jsonp",
        beforeSend: function() {

        },
        complete: function() {

        },
        success: function(resultData) {
            var todaySunRise = new Date(resultData.daily.data[0].sunriseTime*1000);
            var todaySunSet = new Date(resultData.daily.data[0].sunsetTime*1000);
            var tomorrowSunRise = new Date(resultData.daily.data[1].sunriseTime*1000);
            var now = new Date();

            if (now >= todaySunSet && now <= tomorrowSunRise) {
                sunrise = tomorrowSunRise;
                sunset = todaySunSet;
            }
            else if (now <= todaySunSet && now >= todaySunRise) {
                sunrise = todaySunRise;
                sunset = todaySunSet;
            }
            else if (now <= todaySunRise) {
                sunrise = todaySunRise;
                sunset = todaySunSet;
            }

            sunrise = sunrise.getHours() + sunrise.getMinutes()/60;
            sunset = sunset.getHours() + sunset.getMinutes()/60;
            move_time(now);
            initTimer(sunrise, sunset);

        },
        error : function(jqXHR, textStatus, errorThrown) {
            console.log(textStatus)
        },

        timeout: 120000
    });
}



/*
 *  Function to move the sun and moon according to current time
 */


var move_time = function (hours) {
    hours = hours.getHours() + hours.getMinutes()/60;

    var moon = d3.select("#moon");
    var svg = d3.select("#svg");
    var sun = d3.select("#sun");

    if (hours <= sunset && hours >= sunrise) {
        //Sun is shining, move to appropriate position

        moon.attr('visibility', 'hidden');
        //get position in radians
        //half circle is devided in N pieces
        var dayHours = sunset - sunrise;
        var radians = Math.PI - (hours - sunrise)/dayHours * Math.PI; //Nr of radians to move to the right
        var x = Math.cos(radians) * svg.attr('width')* 0.4 + svg.attr('width') * 0.5;
        var y = svg.attr('height') - Math.sin(radians) * svg.attr('width') * 0.4;

        sun.attr("transform", "translate(" + (x - sun.attr('width')/2) + "," + (y - sun.attr('height')/2)+ ")");
        sun.attr('visibility', 'visible');
    }

    else {
        //Nighttime, move the moon to the appropriate position
        sun.attr('visibility', 'hidden');

        var nightHours = sunrise + (24 - sunset);
        if (hours <= 24 && hours >= sunset) {
            hours = hours - sunset;
        }
        else {
            hours = hours + (24 - sunset);
        }

        var radians = Math.PI - hours/nightHours * Math.PI; //Nr of radians to move to the right


        var x = Math.cos(radians) * svg.attr('width')* 0.4 + svg.attr('width') * 0.5;
        var y = svg.attr('height') - Math.sin(radians) * svg.attr('width') * 0.4;

        moon.attr("transform", "translate(" + (x - sun.attr('width')/2) + "," + (y - sun.attr('height')/2)+ ")");
        moon.attr('visibility', 'visible');
    }
};


/*
 *  Functions for the countdown timer
 */


function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));
    return {
        'total': t,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    };
}

function initializeClock(id, endtime) {
    var clock = document.getElementById(id);
    var hoursSpan = clock.querySelector('.hours');
    var minutesSpan = clock.querySelector('.minutes');
    var secondsSpan = clock.querySelector('.seconds');

    function updateClock() {
        var t = getTimeRemaining(endtime);

        hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
        minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
        secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

        move_time(new Date());

        if (t.total <= 0) {
            clearInterval(timeinterval);
        }
    }

    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
}

function initTimer(sunrise, sunset) {
    var now = new Date();
    var hours = now.getHours();
    console.log(sunrise);
    console.log(sunset);
    var timeDiff = 0;
    if (hours < 24 && hours > sunset) {
        timeDiff += (60 - now.getSeconds()) * 1000; //seconds
        timeDiff += (59 - now.getMinutes()) * 60 * 1000; //minutes
        timeDiff += (23 - now.getHours() + sunrise) * 60 * 60 * 1000;//hours
    }
    else if(hours < sunrise) {
        timeDiff += (60 - now.getSeconds()) * 1000; //seconds
        timeDiff += (59 - now.getMinutes()) * 60 * 1000; //minutes
        timeDiff += (sunrise - 1 - now.getHours()) * 60 * 60 * 1000;
    }
    else if (hours >= sunrise && hours <= sunset) {
        timeDiff += (60 - now.getSeconds()) * 1000; //seconds
        timeDiff += (59 - now.getMinutes()) * 60 * 1000; //minutes
        timeDiff += (sunset - 1 - now.getHours()) * 60 * 60 * 1000;//hours
    }

    var deadline = new Date(Date.parse(new Date()) + timeDiff);
    initializeClock('clockdiv', deadline);
}


/*
 *  Functions to display the daily recipe
 */

function init_recipe(){
    jQuery.ajax({
        url: "https://api.edamam.com/search?q=egg&app_id=a8f2a628&app_key=7f84264a24ce3ab457a4e97e5837dc6e&from=0&to=100",
        type: "GET",

        contentType: 'application/json; charset=utf-8',
        beforeSend: function() {
            //... your initialization code here (so show loader) ...
        },
        complete: function() {
            var loading = document.getElementById('loading');
            loading.setAttribute('style', 'visibility: hidden; display: none');

            var dailyRecipe = document.getElementById('dailyRecipe');
            dailyRecipe.setAttribute('style', 'visibility: visible;');
        },
        success: function(resultData) {
            var totalRecipees = resultData.hits.length;
            var randID = Math.floor(Math.random() * (totalRecipees));

            var randRecipee = resultData.hits[randID].recipe;

            var img = document.getElementById("recipeImg");
            img.setAttribute("src", randRecipee.image);

            var label = document.getElementById("recipeLabel");
            label.innerText = "Recipe of the day - " + randRecipee.label;

            var ingredients = randRecipee.ingredientLines;
            var list = document.getElementById("ingrediënts");

            for (var i = 0; i < ingredients.length; i++) {
                var listItem = document.createElement("li");
                listItem.appendChild(document.createTextNode(ingredients[i]));
                list.appendChild(listItem);
            }

            var tags = randRecipee.healthLabels;
            var taglist = document.getElementById("tags");

            var html = '';
            for (i = 0; i < tags.length; i++) {
                html += '<div class="chip">' + tags[i] + '</div>';
            }
            taglist.innerHTML = html;

        },
        error : function(jqXHR, textStatus, errorThrown) {
            console.log(textStatus)
        },

        timeout: 120000
    });
}








$( document ).ready(function() {
    init_svg();
    init_sun_moon();
    init_recipe();
});