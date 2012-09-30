
var roster_ui = {
	
	init: function() {
		// remove buttons
		$(".remove").click(this.remove)
		
		
		// add roster slots
		$(".fill_slot").click(this.fill_slot)
		
		
    
		$("#add_player_modal").on('show', function (e) {
			//console.log(e)
		})
		
	},
	remove: function() {
		var slot = $($(this).parents(".slot")[0]);
		var id = slot.attr("data-id");
		if (confirm("Are you sure you want to remove " + id + "	?")) {
			//ajax remove, replace row with "empty slot"

			slot.parents(".resuts");
			$.ajax({
				url: "/api/remove",
				error: function() {
					
				}
			})
		}
		return false;
	},
	
	fill_slot: function(e) {
		var group = $($(this).parents(".slot-group")[0]);
		var type = group.attr("data-type");
		
		$("#modal_type").html(type);
		search.set_type(type);
    $("#add_player_modal").modal('show');
		
		
		return false;
	},

}

var search= {
  player_type: "player",
  page: 0,
  init: function() {
    $(".search-box").keyup(this.keyup_handler);
    
    $(".search-prev").click(this.prev);
    $(".search-next").click(this.next);
    this.button_label = $(".search-finder").attr("data-button-label");
    this.action = $(".search-finder").attr("data-action");

    this.url = $(".search-finder").attr("data-url");
    this.update();
  },
  set_type: function(type) {
    this.player_type = type;
    this.update();
    $(".search-search").val("");
  },
  keyup_handler: function() {
    clearTimeout(search.timeout);
    search.timeout = setTimeout(search.update, 200);
    
  },
  update: function() {
    var term =  $(".search-box").val();
    $.ajax({
      url: search.url + "?type=" + search.player_type + "&search=" + term + "&page=" + search.page,
      success: function(data) {
        $(".search-results").html("");
        for (var i=0; i< data.data.length; i++) {
          var d = data.data[i];
            $(".search-results").append("<li><img src='"+ d.photo +"'> "+ d.name +"\
              <button id='" + d.id + "' class='btn search-action btn-small btn-success pull-right'>" +search.button_label + "</button></li>");
          
        }
        $(".search-action").click(search.action_handler);
        if (data.data.length == 0) {
          $(".search-results").html("<li>Sorry, no matching results</li>");
        }
      }
    })
    
  },
  prev: function(e) {
    if (search.page >0) {
      search.page -=1;
    }
    search.update();
      
  },
  next: function(e){
    search.page +=1;
    search.update();  
  },
  
  //this isn't great
  action_handler: function(e) {
    var id = this.id;
    if (search.action == "start_game") {
      start_game(id)
    }
    else if (search.action == "fill_slot") {
      fill_slot(id, search.player_type);
    }
  }
  
  
  
}

$(document).ready(function() {
    roster_ui.init();
    if ($(".search-finder").length == 1) {
      search.init();
    }
})


function start_game(user_id) {
  console.log("Starting game")
  //ajax request to start game. returns id. 
  
  $.ajax({
    url: "/create_game/?opp_id=" + user_id,
    success: function(game_id) {
      //redirect to /games/id (or whatever it ends up being)
      window.location = "/game/" + game_id;
    }
  })
  
  
}

function fill_slot(player_id, player_type) {
  //ajax request
 
  $.ajax({
    url: "/roster/fill_slot/?roster_id=" + roster_id + "&type=" + player_type + "&player_id=" + player_id,
    success: function() {
      //reload the page for now
      window.location = window.location;
    }
  })  
  
  
}