


var roster_ui = {
	
	init: function() {
		// remove buttons
		$(".remove").click(this.remove)
		
		
		// add roster slots
		$(".fill_slot").click(this.fill_slot)
		
		
		
		$("#add_player_modal").on('show', function (e) {
			console.log(e)
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
		$("#add_player_modal").modal('show');
		
		
		return false;
	},
}

$(document).ready(function() {
    roster_ui.init();
})

