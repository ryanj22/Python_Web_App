function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input0 = document.getElementById("myInput0");
  input1 = document.getElementById("myInput1");
  input2 = document.getElementById("myInput2");
  filter0 = input0.value.toUpperCase();
  filter1 = input1.value.toUpperCase();
  filter2 = input2.value.toUpperCase();
  table = document.getElementById("paramtable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td0 = tr[i].getElementsByTagName("td")[0];
    td1 = tr[i].getElementsByTagName("td")[1];
    td2 = tr[i].getElementsByTagName("td")[2];
    if (td0) {
      if ((td0.innerHTML.toUpperCase().indexOf(filter0) > -1) && (td1.innerHTML.toUpperCase().indexOf(filter1) > -1) && (td2.innerHTML.toUpperCase().indexOf(filter2) > -1)) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function getID(element) {
  document.getElementById('myTextarea').value = element.rowIndex;
}
