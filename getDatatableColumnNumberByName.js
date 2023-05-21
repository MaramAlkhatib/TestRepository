 function getColumnNumberByName(name) {
        var Tableheaders = $("#dataTable thead th");
        var counter = 0;
        var colindex = -1; // set default value
        $.each(Tableheaders, function (key, Value) {
          counter += 1;
          // console.log(counter)
          // console.log(Value.innerText)
          if (Value.innerText === name) {
            // console.log(Value.innerText)
            colindex = Value.dataset.columnIndex;
            // console.log("colindex",colindex)
            return false; // stop iterating
          }
        });
        return colindex; // returns -1 if column not found
      }
      
     
getColumnNumberByName("Office")
