function countPatients() {
  var filteredPatientNumber;
  var patientNumber;

  const allRows = document.getElementById("data-rows").children;
  const headRow = document.getElementById("head-row").children;

  var patientIndex;
  for (let i = 0; i < headRow.length; i++) {
    var value = headRow[i].getAttribute("name");
    if (value == JSON.parse(document.getElementById('patient_identifier_name_script').textContent)) {
      patientIndex = i;
      break;
    }
  }
  let columnNumber = patientIndex;
  const filteredPatients = new Set();
  const patients = new Set();
  for (let i = 0; i < allRows.length; i++) {
    if (allRows[i].children[columnNumber]){
      let patientID = allRows[i].children[columnNumber].innerHTML;
      if (allRows[i].style.display != "none") {
        filteredPatients.add(patientID);
      }
      patients.add(patientID);
    }
    }
    

  filteredPatientNumber = document.getElementById("id-filtered-patient-number");
  filteredPatientNumber.innerHTML = filteredPatients.size;
  patientNumber = document.getElementById("id-patient-number");
  patientNumber.innerHTML = patients.size;
}