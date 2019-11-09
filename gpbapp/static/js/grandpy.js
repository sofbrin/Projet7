$(document).ready(function () {

  // hide the spinner when launching the page
  $("#loader").hide();

  // launche the search with enter key
  $("textarea").keyup(function(ev) {
    if (ev.which == 13) {
      $("#getQuestion").click();
    }
  });
  // launche the search with click button
  $("#getQuestion").click(function(e) {
    e.preventDefault();

    var user_question = $("textarea[id='question']").val();

    // process the user's question and dealing with the answer's cases
    $.ajax({

      type: 'POST',
      url: '/grandpyAnswer/',
      data: JSON.stringify({question:user_question}),
      contentType: 'application/json',
      beforeSend: function() { $("#loader").show()},

      success: function(data) {
        $("#loader").hide();
        $("div[id='history']").append("<p class='user_question'>" + user_question + "</p>");
        $("textarea[id='question']").val("");

        // case 1: enter/click without any question
        if (data == "") {
          $("div[id='history']").append("<p class='wiki_error'>Hé ! tu n'as posé aucune question. Réessaye :)</p>");
        }
        // case 2: unclear question
        else if (data == "error") {
          $("div[id='history']").append("<p class='wiki_error'>Je n'ai pas compris, reformule ta question ou sois plus précis !</p>");
        }
        // case 3: incomprehensible question
        else if ((data['search'] == null) && (data['address'] == null)) {
          $("div[id='history']").append("<p class='wiki_error'>Comment ??? Repose ta question.</p>");
        }
        else {
          if (data['search'] != null) {

            // case 4: question ok --> address, wikipedia infos and map localization available and printed
            if (data['address'] != null) {
              $("div[id='history']").append("<p class='address'>Tiens, voici l'adresse : " + data['address'] + ". Et regarde la localisation sur la carte dessous :)</p>");

              $("#map").css("display", "block");
              $("#map_error").css("display", "none");

              var map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: data['latitude'], lng: data['longitude']},
                zoom: 14
              });
              var marker = new google.maps.Marker({position:{lat: data['latitude'], lng: data['longitude']}, map: map});

              $("div[id='history']").append("<p class='more_wiki'>Est-ce que je t'ai déjà raconté que... " +
              data['summary'] + " " + "[<a href=" + data['url'] + ">En savoir plus</a>]</p>");
            }

            // case 5: question ok --> wikipedia info available but no address
            else {
              $("div[id='history']").append("<p class='address'>Ah, là, j'ai des infos mais pas d'adresse, ni de carte :)</p>");
              $("div[id='history']").append("<p class='more_wiki'>Savais-tu que... " +
              data['summary'] + " " + "[<a href=" + data['url'] + ">En savoir plus</a>]</p>");

              $("#map").css("display", "none");
              $("#map_error").css("display", "block");
            }
          }

          // case 6: question ok --> address and map localization available but no wikipedia info
          else {
            $("div[id='history']").append("<p class='address'>Pour cette entrée, j'ai une adresse, une carte, mais pas d'infos particulières ! Voici l'adresse : " + data['address'] + "</p>");

            $("#map").css("display", "block");
            $("#map_error").css("display", "none");

            var map = new google.maps.Map(document.getElementById('map'), {
              center: {lat: data['latitude'], lng: data['longitude']},
              zoom: 14
            });
            var marker = new google.maps.Marker({position:{lat: data['latitude'], lng: data['longitude']}, map: map});
          }
        }
      }
    })
  })
})

// print a standard map when launching the page
function initMap(){
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -3.0665, lng: 37.3507},
    zoom: 10
  })
}
