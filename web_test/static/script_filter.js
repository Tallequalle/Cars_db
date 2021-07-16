<script type="text/javascript">
//фильтрация по 1 столбцу
   	function filter1 (phrase, _id){
		var words = phrase.value.toLowerCase().split(" ");
		var table = document.getElementById(_id);
		for (var r = 1; r < table.rows.length; r++){ //сколько строк сверху не фильтровать
			var cellsV = table.rows[r].cells[0].innerHTML.replace(/<[^>]+>/g,""); // 1 столбец для фильтрации
			var cellsV = [cellsV].join(" ");
		    var displayStyle = 'none';
		    for (var i = 0; i < words.length; i++) {
			if (cellsV.toLowerCase().indexOf(words[i])>=0)
				displayStyle = '';
			else {
				displayStyle = 'none';
				break;
			}
			}
		table.rows[r].style.display = displayStyle;
		}
	}

//фильтрация по 2 столбцу
	function filter11 (phrase, _id){
		var words = phrase.value.toLowerCase().split(" ");
		var table = document.getElementById(_id);
		for (var r = 1; r < table.rows.length; r++){ //сколько строк сверху не фильтровать
			var cellsV = table.rows[r].cells[1].innerHTML.replace(/<[^>]+>/g,""); // 2 столбец для фильтрации
			var cellsV = [cellsV].join(" ");
		    var displayStyle = 'none';
		    for (var i = 0; i < words.length; i++) {
			if (cellsV.toLowerCase().indexOf(words[i])>=0)
				displayStyle = '';
			else {
				displayStyle = 'none';
				break;
			}
			}
		table.rows[r].style.display = displayStyle;
		}
	}
  </script>
