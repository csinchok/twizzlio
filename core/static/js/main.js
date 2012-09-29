


var roster_ui = {
	
	init: function() {
		// register events 
			
			
			
		// remove buttons
		
		$(".remove").click(this.show_remove_dialog)
		
		
		// add roster slots
		
	},
	show_remove_dialog: function() {
		if (confirm("Are you sure you want to remove?")) {
			//ajax remove, replace row with "empty slot"
			var slot = $($(this).parents(".slot")[0]);
			slot.attr("data-id");
			slot.parents(".resuts")
			$.ajax({
				url: "/api/remove",
				error: function() {
					
				}
			})			
		}
	}
	
	
	
}

