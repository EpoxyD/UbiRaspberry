/*
 *  Initialize website
 */

$.getJSON("php/get_all_chicks.php",
    function (result) {
        console.log(result);
        for (i = 0; i < result.length; i++) {
            appendChick(result[i]);
        }
});

function appendChick(chick) {
    var demoCard = document.getElementById('demoChick');
    var wrapper = demoCard.parentNode;
    var newCard = demoCard.cloneNode(true);

    newCard.setAttribute('id', 'chick' + chick.id);
    newCard.style.visibility = '';
    newCard.style.display = '';


    var new_name = newCard.querySelector("#demo_name");
    new_name.setAttribute('id', 'chick' + chick.id + '_name');
    if (chick.name != null) {
        new_name.innerText = chick.name;
    }
    else {
        new_name.innerText = "Nameless Chick";
    }


    var new_race = newCard.querySelector("#demo_race");
    new_race.setAttribute('id', 'chick' + chick.id + '_race');
    if (chick.race != null) {
        new_race.innerText = chick.race;
    }
    else {
        new_race.innerText = "Race unknown";
    }


    var new_age = newCard.querySelector("#demo_age");
    new_age.setAttribute('id', 'chick' + chick.id + '_age');
    if (chick.age != null) {
        new_age.innerText = chick.age;
    }
    else {
        new_age.innerText = "Forever young";
    }

    var new_img = newCard.querySelector("#demo_img");
    new_img.setAttribute('id', 'chick' + chick.id + '_img');
    if (chick.imagepath != null && chick.imagepath != '') {
        new_img.setAttribute('src', chick.imagepath);
    }
    else {
        new_img.setAttribute('src', "img/no_chick.jpg");
    }

    wrapper.appendChild(newCard);
    wrapper.insertBefore(newCard, document.getElementById('addButton'));
}





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

var sunriseDT; //Date object
var sunsetDT; //Date object
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
                sunriseDT = tomorrowSunRise;
                sunsetDT = todaySunSet;

                var svg = d3.select("#svg");
                svg.append('text')
                    .attr("x", svg.attr('width') * 0.12 )
                    .attr("y", svg.attr('height') * 0.99)
                    .text( ('0' + sunsetDT.getHours()).slice(-2) + 'h' + ('0' + sunsetDT.getMinutes()).slice(-2))
                    .attr("font-size", "14px")
                    .attr("font-family", 'sans-serif')
                    .attr("fill", "white");

                svg.append('text')
                    .attr("x", svg.attr('width') * 0.88 )
                    .attr("y", svg.attr('height')* 0.99)
                    .text( ('0' + sunriseDT.getHours()).slice(-2) + 'h' + ('0' + sunriseDT.getMinutes()).slice(-2))
                    .attr("text-anchor", "end")
                    .attr("font-size", "14px")
                    .attr("font-family", 'sans-serif')
                    .attr("fill", "white");
            }
            else if (now <= todaySunSet && now >= todaySunRise) {
                sunriseDT = todaySunRise;
                sunsetDT = todaySunSet;

                var svg = d3.select("#svg");
                svg.append('text')
                    .attr("x", svg.attr('width') * 0.12 )
                    .attr("y", svg.attr('height')* 0.99)
                    .text( ('0' + sunriseDT.getHours()).slice(-2) + 'h' + ('0' + sunriseDT.getMinutes()).slice(-2))
                    .attr("font-size", "14px")
                    .attr("font-family", 'sans-serif')
                    .attr("fill", "white");

                svg.append('text')
                    .attr("x", svg.attr('width') * 0.88 )
                    .attr("y", svg.attr('height')* 0.99)
                    .text( ('0' + sunsetDT.getHours()).slice(-2) + 'h' + ('0' + sunsetDT.getMinutes()).slice(-2))
                    .attr("text-anchor", "end")
                    .attr("font-size", "14px")
                    .attr("font-family", 'sans-serif')
                    .attr("fill", "white");
            }
            else if (now <= todaySunRise) {
                sunriseDT = todaySunRise;
                sunsetDT = todaySunSet;

                var svg = d3.select("#svg");
                svg.append('text')
                    .attr("x", svg.attr('width') * 0.12 )
                    .attr("y", svg.attr('height')* 0.9)
                    .text( ('0' + sunsetDT.getHours()).slice(-2) + 'h' + ('0' + sunsetDT.getMinutes()).slice(-2))
                    .attr("font-size", "14px")
                    .attr("font-family", 'sans-serif')
                    .attr("fill", "white");

                svg.append('text')
                    .attr("x", svg.attr('width') * 0.88 )
                    .attr("y", svg.attr('height') * 0.9)
                    .text( ('0' + sunriseDT.getHours()).slice(-2) + 'h' + ('0' + sunriseDT.getMinutes()).slice(-2))
                    .attr("text-anchor", "end")
                    .attr("font-size", "14px")
                    .attr("font-family", 'sans-serif')
                    .attr("fill", "white");
            }

            sunrise = sunriseDT.getHours() + sunriseDT.getMinutes()/60;
            sunset = sunsetDT.getHours() + sunsetDT.getMinutes()/60;
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

    var stop = false;
    function updateClock() {
        var t = getTimeRemaining(endtime);

        hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
        minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
        secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

        move_time(new Date());

        if (t.total <= 0) {
            //setTimeout(initTimer, 10000);
            stop = true;
        }
    }

    if (stop) {
        setTimeout(init_sun_moon(), 10000);
    }
    else {
        updateClock();
        var timeinterval = setInterval(updateClock, 1000);
    }

}

function initTimer(sunrise, sunset) {
    var now = new Date();
    var hours = now.getHours();

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


/*
 *  Functions to fill modal on edit
 */

function fillModal(button) {
    chickPassport = button.parentNode.parentNode.parentNode;

    var modal = document.getElementById("modal");

    var image = document.getElementById("image");
    var name = document.getElementById("name");
    var race = document.getElementById("race");
    var age = document.getElementById("age");
    var id = document.getElementById("chickid");

    var chick = chickPassport.getAttribute("id");
    id.innerHTML = chick;

    name.placeholder = document.getElementById(chick + "_name").innerText;
    race.placeholder = document.getElementById(chick + "_race").innerText;
    age.placeholder = document.getElementById(chick + "_age").innerText;
    image.setAttribute("src", document.getElementById(chick + "_img").getAttribute("src"));
}

function saveEdit(chickid) {

    console.log(chickid);
    var imageModal = document.getElementById("image");
    var nameModal = document.getElementById("name");
    var raceModal = document.getElementById("race");
    var ageModal = document.getElementById("age");

    if (nameModal.value != null && nameModal.value != "") {
        document.getElementById(chickid + "_name").innerText = nameModal.value;
    }
    if (raceModal.value != null && raceModal.value != "") {
        document.getElementById(chickid + "_race").innerText = "Race: " + raceModal.value;
    }
    if (ageModal.value != null && ageModal.value != "") {
        document.getElementById(chickid + "_age").innerText = "Age: " + ageModal.value;
    }

    document.getElementById(chickid + "_img").setAttribute("src", imageModal.getAttribute("src"));

    //Clear input fields
    var form = document.getElementById("editform");
    form.reset();


    //TODO: Store new image in local folder

    //TODO: Store Chicks in database
}

function removeChicks(button) {
    var id = button.parentNode.parentNode.parentNode.getAttribute("id");

    $("#"+id).remove();


    $.getJSON("php/remove_chick.php",{
            id: id.substr(5)
        });
}

var insertID = 5;
function addChicks(card){
    //TODO: add form validation on age (only ints)

    $.getJSON("php/add_chick.php",{
        name: document.getElementById('addname').value,
        race: document.getElementById('addrace').value,
        age: document.getElementById('addage').value
    },
    function (result) {
        console.log(result);
    });

    var demoCard = document.getElementById('demoChick');
    var wrapper = demoCard.parentNode;
    var newCard = demoCard.cloneNode(true);

    newCard.setAttribute('id', 'chick' + insertID);
    newCard.style.visibility = '';
    newCard.style.display = '';

    //TODO: Change chick image and its id

    var new_name = newCard.querySelector("#demo_name");
    new_name.setAttribute('id', 'chick' + insertID + '_name');
    new_name.innerText = document.getElementById('addname').value;

    var new_race = newCard.querySelector("#demo_race");
    new_race.setAttribute('id', 'chick' + insertID + '_race');
    new_race.innerText = document.getElementById('addrace').value;

    var new_age = newCard.querySelector("#demo_age");
    new_age.setAttribute('id', 'chick' + insertID + '_age');
    new_age.innerText = document.getElementById('addage').value;

    wrapper.appendChild(newCard);
    wrapper.insertBefore(newCard, document.getElementById('addButton'));

    insertID ++;
}



$( document ).ready(function() {
    init_svg();
    init_sun_moon();
    init_recipe();
});