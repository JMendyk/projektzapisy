var question = "<li class='poll-question-answer'>"+
"<div>"+
"	<input type='text' class='autocomplete' id='poll[question][${id}][answers][]' name='poll[question][${id}][answers][]'>"+
"	<input type='checkbox' style='display:inline' class='hideOnCheckbox' id='poll[question][${id}][hideOn][]' name='poll[question][${id}][hideOn][]' value='${size}'>"+	
"	<label style='display:inline' for='poll[question][${id}][hideOn][]'>Ukryj sekcję</label>"+
"	<img src='/site_media/images/remove-ico.png' class='remove' alt='usuń'>"+
"</div>"+
"</li>"

$.template( "question", question );