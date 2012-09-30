


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
    $(".player-search").keyup(this.keyup_handler);
    
    $(".player-prev").click(this.prev);
    $(".player-next").click(this.next);
    this.button_label = $(".player-finder").attr("data-button-label");
    this.url = $(".player-finder").attr("data-url");
    this.update();
  },
  set_type: function(type) {
    this.player_type = type;
    this.update();
    $(".player-search").val("");
  },
  keyup_handler: function() {
    clearTimeout(search.timeout);
    search.timeout = setTimeout(search.update, 200);
    
  },
  update: function() {
    console.log("updatin'")
    var term =  $(".player-search").val();
    $.ajax({
      
      url: search.url + "?type=" + search.player_type + "&search=" + term + "&page=" + search.page,
      success: function(data) {
        console.log(data);
        $(".player-results").html("");
        for (var i=0; i< data.data.length; i++) {
          var d = data.data[i];
            $(".player-results").append("<li><img src='"+ d.photo +"'> "+ d.name +"\
              <button id='" + d.id + "' class='btn btn-small btn-success pull-right'>" +search.button_label + "</button></li>");
          
        }
        if (data.data.length == 0) {
          $(".player-results").html("<li>Sorry, no matching results</li>");
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
  }
  
  
  
}

$(document).ready(function() {
    roster_ui.init();
    if ($(".player-finder").length == 1) {
      search.init();
    }
})

